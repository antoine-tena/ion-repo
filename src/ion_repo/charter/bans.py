"""Bans: the rule holds everywhere, any reintroduction fails.

Each rule receives the repo and its parameters (`[bans.<name>]` in charter.toml) and returns its
failures. Common parameters: `id` (identifier of the rule in the repo's instructions, shown in
brackets), `files` (git patterns), `message`.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

from ion_repo.charter.repo import Params, Repo, failure, justified, outside_tests

PYTHON = ["backend/*.py", "backend/**/*.py"]
Ban = Callable[[Repo, Params], list[str]]


def _code(repo: Repo, params: Params) -> list[Path]:
    return outside_tests(repo.tracked(params.get("files", PYTHON)))


SIGNALS = re.compile(r"@receiver\b|from django\.db\.models\.signals import")


def django_signals(repo: Repo, params: Params) -> list[str]:
    """Django signals are banned: hidden side effects, broken determinism."""
    culprits = [
        repo.rel(path) for path in _code(repo, params) if SIGNALS.search(path.read_text("utf-8"))
    ]
    message = params.get("message", "Django signals are banned")
    return [failure(params.get("id", "NO-SIGNALS"), message, culprits)] if culprits else []


def logging(repo: Repo, params: Params) -> list[str]:
    """Structured logging (structlog) is mandatory; `print()` is banned outside tests."""
    stdlib, prints = [], []
    for path in repo.tracked(params.get("files", PYTHON)):
        text = path.read_text("utf-8")
        if "logging.getLogger" in text:
            stdlib.append(repo.rel(path))
        if "tests" not in path.parts and re.search(r"^\s*print\(", text, re.MULTILINE):
            prints.append(repo.rel(path))
    rule = params.get("id", "LOGGING")
    failures = []
    if stdlib:
        failures.append(failure(rule, "logging.getLogger: use structlog", stdlib))
    if prints:
        failures.append(failure(rule, "print() is banned outside a bootstrap script", prints))
    return failures


def django_migrations(repo: Repo, params: Params) -> list[str]:
    """Migrations named `NNNN_name.py`, numbered without gaps; a migration already on the
    integration branch is neither changed nor deleted (production may have applied it)."""
    pattern = params.get("files", "backend/**/migrations/*.py")
    name = re.compile(r"^(\d{4})_\w+\.py$")
    numbers: dict[str, list[int]] = defaultdict(list)
    misnamed = []
    for path in repo.tracked(pattern, excluded=False):
        if path.name == "__init__.py":
            continue
        rel = repo.rel(path)
        if match := name.match(path.name):
            numbers[rel.rsplit("/migrations/", 1)[0]].append(int(match.group(1)))
        else:
            misnamed.append(rel)
    for app, found in numbers.items():
        if sorted(found) != list(range(1, len(found) + 1)):
            misnamed.append(f"{app}/migrations: numbers {sorted(found)}")
    rule = params.get("id", "MIGRATIONS")
    failures = []
    if misnamed:
        message = "migrations named NNNN_name.py, numbered without gaps"
        failures.append(failure(rule, message, misnamed))
    base = repo.git("merge-base", "HEAD", f"origin/{params.get('branch', 'develop')}").strip()
    if base:
        changed = repo.git("diff", "--name-status", "--diff-filter=MDR", base, "--", pattern)
        rewritten = [
            line.split("\t")[1] for line in changed.splitlines() if not line.endswith("__init__.py")
        ]
        if rewritten:
            message = "a merged migration is never changed: add a new one"
            failures.append(failure(rule, message, rewritten))
    return failures


SECRET = re.compile(r"token|secret|digest|signature|hash|otp|api_?key|verification_code", re.I)
CONSTANT_TIME_MARKERS = ("Constant time", "Temps constant")


def _names(node: ast.expr) -> list[str]:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [node.attr, *_names(node.value)]
    if (
        isinstance(node, ast.Subscript)
        and isinstance(node.slice, ast.Constant)
        and isinstance(node.slice.value, str)
    ):
        return [node.slice.value]
    return []


def constant_time(repo: Repo, params: Params) -> list[str]:
    """A secret is never compared with `==`/`!=` (the response time gives it away):
    `hmac.compare_digest`. Exception justified by `# Constant time: <reason>`."""
    culprits = []
    for path in _code(repo, params):
        text = path.read_text("utf-8")
        lines = text.splitlines()
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.Compare) or not any(
                isinstance(operator, (ast.Eq, ast.NotEq)) for operator in node.ops
            ):
                continue
            sides = [node.left, *node.comparators]
            if any(isinstance(side, ast.Constant) for side in sides):
                continue
            if any(SECRET.search(name) for side in sides for name in _names(side)) and not (
                justified(lines, node.lineno, *CONSTANT_TIME_MARKERS)
            ):
                culprits.append(f"{repo.rel(path)}:{node.lineno}  {ast.unparse(node)[:70]}")
    if not culprits:
        return []
    message = "compare a secret with compare_digest"
    return [failure(params.get("id", "CONSTANT-TIME"), message, culprits)]


PERSONAL = re.compile(
    r"^(e_?mail|.*_email|phone|.*_phone|first_name|last_name|full_name|name|ip|ip_address"
    r"|client_ip|address)$"
)
LOGGERS = re.compile(r"^(logger|log|_logger|audit_logger|security_logger|structlog)$")
LOG_METHODS = {"debug", "info", "warning", "warn", "error", "exception", "critical", "bind"}
PERSONAL_DATA_MARKERS = ("Personal data", "Donnée perso")


def _logged_personal_keys(node: ast.Call) -> list[str]:
    keys = [keyword.arg for keyword in node.keywords if keyword.arg and PERSONAL.match(keyword.arg)]
    for value in [*node.args, *(keyword.value for keyword in node.keywords)]:
        if isinstance(value, ast.Dict):
            keys += [
                key.value
                for key in value.keys
                if isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and PERSONAL.match(key.value)
            ]
    return keys


def _is_log_call(node: ast.AST) -> bool:
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in LOG_METHODS
    ):
        return False
    target = node.func.value
    return bool(
        LOGGERS.match(target.id if isinstance(target, ast.Name) else getattr(target, "attr", ""))
    )


def personal_data(repo: Repo, params: Params) -> list[str]:
    """No personal data in a log: the identifier, never the person. Exception justified by
    `# Personal data: <reason>`."""
    culprits = []
    for path in _code(repo, params):
        text = path.read_text("utf-8")
        lines = text.splitlines()
        for node in ast.walk(ast.parse(text)):
            if not _is_log_call(node):
                continue
            assert isinstance(node, ast.Call)
            keys = _logged_personal_keys(node)
            if keys and not justified(lines, node.lineno, *PERSONAL_DATA_MARKERS):
                culprits.append(f"{repo.rel(path)}:{node.lineno}  {', '.join(keys)}")
    if not culprits:
        return []
    return [failure(params.get("id", "PERSONAL-DATA"), "personal data in a log", culprits)]


def vue_style(repo: Repo, params: Params) -> list[str]:
    """No `<style>` tag (at the start of a line) in a `.vue` component."""
    block = re.compile(r"^<style\b", re.MULTILINE)
    culprits = [
        repo.rel(path)
        for path in repo.tracked(params.get("files", "frontend/app/**/*.vue"))
        if block.search(path.read_text("utf-8"))
    ]
    message = params.get(
        "message", "no <style> tag in a .vue file: Tailwind classes or a shared stylesheet"
    )
    return [failure(params.get("id", "STYLE-1"), message, culprits)] if culprits else []


AUDIT_SUFFIXES = [".py", ".ts", ".vue", ".mjs", ".js", ".cjs", ".yml", ".yaml", ".sh"]


def audit_references(repo: Repo, params: Params) -> list[str]:
    """No reference to an audit finding in the code: a comment states the constraint in the
    present, history goes in the commit. `prefixes`: prefixes of the findings (regex)."""
    suffixes = set(params.get("suffixes", AUDIT_SUFFIXES))
    excluded = re.compile(params.get("exclude", r"^docs/"))
    reference = re.compile(
        rf"\b(?:audits?|constats?|findings?)\s[A-Z]{{1,4}}\d|\b(?:{params['prefixes']})-\d{{2}}\b"
        r"|\baudits?\s(?:frontend|backend)\b"
    )
    culprits = []
    for path in repo.tracked([], excluded=False):
        rel = repo.rel(path)
        if path.suffix not in suffixes or excluded.search(rel):
            continue
        for number, line in enumerate(path.read_text("utf-8").splitlines(), start=1):
            if reference.search(line):
                culprits.append(f"{rel}:{number}: {line.strip()[:100]}")
    message = "reference to an audit finding: state the constraint, history goes in the commit"
    return [failure(params.get("id", "AUDIT-REFERENCES"), message, culprits)] if culprits else []


def forbidden_files(repo: Repo, params: Params) -> list[str]:
    """Files that must not (or no longer) exist: `paths`, `message`."""
    present = [path for path in params["paths"] if (repo.root / path).exists()]
    message = params.get("message", "forbidden file")
    return [failure(params.get("id", "FORBIDDEN-FILES"), message, present)] if present else []


def identical_copies(repo: Repo, params: Params) -> list[str]:
    """Copies that must stay identical to their original: `pairs` = [[original, copy], …]."""
    failures = []
    for original, copy in params["pairs"]:
        source, target = repo.root / original, repo.root / copy
        if not (source.exists() and target.exists() and source.read_bytes() == target.read_bytes()):
            message = f"{copy} must be an exact copy of {original}"
            failures.append(failure(params.get("id", "COPIES"), message, [original, copy]))
    return failures


def _yaml(path: Path) -> Params:
    try:
        import yaml
    except ImportError:
        import json
        import subprocess

        code = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1]))))"
        output = subprocess.run(
            ["uv", "run", "--no-project", "--with", "pyyaml", "python", "-c", code, str(path)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        loaded = json.loads(output)
    else:
        loaded = yaml.safe_load(path.read_text("utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def compose_profiles(repo: Repo, params: Params) -> list[str]:
    """Services of a compose file that must sit behind a profile (e.g. a mail catcher that would
    swallow everything): `file`, `services`. Read by PyYAML, or through `uv` without it."""
    compose = _yaml(repo.root / params["file"])
    culprits = [
        name
        for name, service in compose.get("services", {}).items()
        if name in params["services"] and not service.get("profiles")
    ]
    message = params.get("message", "service to put behind a profile (`profiles: [dev]`)")
    return [failure(params.get("id", "COMPOSE"), message, culprits)] if culprits else []


FORBIDDEN_COMMANDS = (
    (re.compile(r"\bpip3?\s+install\b|\bpython3?\s+-m\s+pip\b|\bpipx\s+install\b"), "pip: uv"),
    (
        re.compile(r"\bdocker(?:-compose)?\s+(?:build|run|compose|pull|push|exec|up|save|load)\b"),
        "docker: podman",
    ),
)
FORBIDDEN_NAMES = re.compile(
    r"^(?:requirements[\w.-]*\.txt|Dockerfile[\w.-]*|docker-compose[\w.-]*\.ya?ml)$"
)
WITHOUT_COMMANDS = (".md", ".lock", ".svg", ".png", ".jpg", ".ico", ".csv")
FORBIDDEN_TOOL_MARKERS = ("Forbidden tool", "Outil interdit")


def forbidden_tools(repo: Repo, params: Params) -> list[str]:
    """uv for Python and podman for containers, never pip nor docker: neither a command
    (`pip install`, `docker build`…) outside documentation, nor a file (`requirements.txt`,
    `Dockerfile`, `docker-compose.yml`). Exception justified by `# Forbidden tool: <reason>`."""
    culprits = []
    for path in repo.tracked([], excluded=False):
        rel = repo.rel(path)
        if FORBIDDEN_NAMES.match(path.name):
            culprits.append(f"{rel}  (file)")
            continue
        if path.suffix in WITHOUT_COMMANDS or path.name.endswith("-lock.yaml"):
            continue
        if repo.is_generated(path):
            continue
        try:
            lines = path.read_text("utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, start=1):
            for command, advice in FORBIDDEN_COMMANDS:
                if command.search(line) and not justified(lines, number, *FORBIDDEN_TOOL_MARKERS):
                    culprits.append(f"{rel}:{number}  {advice}  {line.strip()[:80]}")
    message = params.get("message", "uv and podman everywhere: never pip nor docker")
    return [failure(params.get("id", "UV-PODMAN"), message, culprits)] if culprits else []


BANS: dict[str, Ban] = {
    "django-signals": django_signals,
    "logging": logging,
    "django-migrations": django_migrations,
    "constant-time": constant_time,
    "personal-data": personal_data,
    "vue-style": vue_style,
    "audit-references": audit_references,
    "forbidden-files": forbidden_files,
    "identical-copies": identical_copies,
    "compose-profiles": compose_profiles,
    "forbidden-tools": forbidden_tools,
}
