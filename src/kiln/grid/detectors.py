"""How a rule is detected: declarative first, Python only when no pattern can say it.

A detector is the `[detector]` table of a rule file. Its `kind`:
- `file`: `paths` (globs) present, or absent with `expect = "absent"`;
- `regex`: `pattern` searched in `files` (globs); `expect = "none"` (the default) fails on each
  match, with its location, `expect = "match"` passes on the first one; in a Python file,
  `within = "code"` keeps the matches that start outside its strings and comments, `within =
  "comments"` those that start in a comment (a file that does not tokenize is read whole);
- `toml`, `json`, `yaml`: the dotted `key` in each file of `files`, present (or equal to
  `equals`), or absent with `expect = "absent"`;
- `python`: `check`, a function of `PYTHON_CHECKS`, for what no pattern can say.
No file to look at means the rule does not apply (`n/a`), never a pass.
"""

import datetime
import io
import json
import re
import tokenize
import tomllib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import PurePosixPath

import yaml  # brought by copier

from kiln.grid import forge
from kiln.grid.facts import Repo

PASS, FAIL, NOT_APPLICABLE = "pass", "fail", "n/a"
KINDS = ("file", "regex", "toml", "json", "yaml", "python")
# Where a regex match counts in a Python file: an example in a string is not the code itself.
WITHIN = ("code", "comments")
STRING_TOKENS = frozenset({tokenize.STRING, tokenize.FSTRING_MIDDLE, tokenize.TSTRING_MIDDLE})
# Locations kept per rule: enough to act on, not a dump.
MAX_LOCATIONS = 20


@dataclass(frozen=True)
class Outcome:
    status: str  # pass, fail, n/a
    locations: tuple[str, ...] = field(default=())  # `path:line` or `path`, where it fails
    detail: str = ""


class DetectorError(ValueError):
    """A detector that cannot run as written."""


def detect(detector: Mapping[str, object], repo: Repo) -> Outcome:
    kind = detector.get("kind")
    if kind == "file":
        return _file(detector, repo)
    if kind == "regex":
        return _regex(detector, repo)
    if kind in ("toml", "json", "yaml"):
        return _key(str(kind), detector, repo)
    if kind == "python":
        check = PYTHON_CHECKS.get(str(detector.get("check", "")))
        if check is None:
            raise DetectorError(f"unknown python check {detector.get('check')!r}")
        return check(repo)
    raise DetectorError(f"unknown detector kind {kind!r}, expected one of {', '.join(KINDS)}")


def problems(detector: Mapping[str, object]) -> list[str]:
    """What keeps a detector from running: unknown kind, missing field, bad regex."""
    kind = detector.get("kind")
    if kind not in KINDS:
        return [f"detector kind {kind!r} is not one of {', '.join(KINDS)}"]
    required = {
        "file": ("paths",),
        "regex": ("files", "pattern"),
        "toml": ("files", "key"),
        "json": ("files", "key"),
        "yaml": ("files", "key"),
        "python": ("check",),
    }[str(kind)]
    found = [f"detector {kind}: `{name}` missing" for name in required if name not in detector]
    if kind == "regex" and "pattern" in detector:
        try:
            re.compile(str(detector["pattern"]), re.MULTILINE)
        except re.error as error:
            found.append(f"detector regex: {error}")
    if kind == "regex" and detector.get("within", "code") not in WITHIN:
        found.append(f"detector regex: `within` is one of {', '.join(WITHIN)}")
    if kind == "python" and detector.get("check") not in PYTHON_CHECKS:
        found.append(f"detector python: no check named {detector.get('check')!r}")
    return found


def _globs(detector: Mapping[str, object], name: str) -> tuple[str, ...]:
    value = detector.get(name, ())
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value) if isinstance(value, list | tuple) else ()


def _file(detector: Mapping[str, object], repo: Repo) -> Outcome:
    found = repo.matching(*_globs(detector, "paths"))
    if detector.get("expect", "present") == "absent":
        return Outcome(FAIL, tuple(found[:MAX_LOCATIONS])) if found else Outcome(PASS)
    return Outcome(PASS, tuple(found[:1])) if found else Outcome(FAIL, detail="not found")


def _regex(detector: Mapping[str, object], repo: Repo) -> Outcome:
    files = repo.matching(*_globs(detector, "files"))
    if not files:
        return Outcome(NOT_APPLICABLE)
    pattern = re.compile(str(detector["pattern"]), re.MULTILINE)
    wants_match = detector.get("expect", "none") == "match"
    within = str(detector.get("within", ""))
    locations: list[str] = []
    for name in files:
        if not repo.is_code(name):
            continue
        text = repo.text(name)
        for found in _matches(pattern, text, within if name.endswith(".py") else ""):
            if wants_match:
                return Outcome(PASS, (name,))
            locations.append(f"{name}:{text.count(chr(10), 0, found.start()) + 1}")
    if wants_match:
        return Outcome(FAIL, detail="no file matches")
    return Outcome(FAIL, tuple(locations[:MAX_LOCATIONS])) if locations else Outcome(PASS)


def _matches(pattern: re.Pattern[str], text: str, within: str) -> list[re.Match[str]]:
    """The matches of `pattern` in a file; `within` the code or the comments of a Python
    source, tokenized only when something matched (most files have nothing)."""
    found = list(pattern.finditer(text))
    if not within or not found:
        return found
    spans = _python_spans(text)
    if spans is None:
        return found
    strings, comments = spans
    if within == "comments":
        return [match for match in found if _inside(match.start(), comments)]
    return [match for match in found if not _inside(match.start(), strings + comments)]


Spans = list[tuple[int, int]]


def _python_spans(text: str) -> tuple[Spans, Spans] | None:
    """Where the strings and the comments of a Python source lie, as offsets in `text`; None
    when it does not tokenize."""
    line_starts = [0, *(found.end() for found in re.finditer("\n", text))]
    strings: Spans = []
    comments: Spans = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type in STRING_TOKENS or token.type == tokenize.COMMENT:
                (start_row, start_column), (end_row, end_column) = token.start, token.end
                start = line_starts[start_row - 1] + start_column
                end = line_starts[end_row - 1] + end_column
                (comments if token.type == tokenize.COMMENT else strings).append((start, end))
    except tokenize.TokenError, SyntaxError:
        return None
    return strings, comments


def _inside(offset: int, spans: Spans) -> bool:
    return any(start <= offset < end for start, end in spans)


def _key(kind: str, detector: Mapping[str, object], repo: Repo) -> Outcome:
    files = repo.matching(*_globs(detector, "files"))
    if not files:
        return Outcome(NOT_APPLICABLE)
    path = str(detector["key"]).split(".")
    expect_absent = detector.get("expect", "present") == "absent"
    failing: list[str] = []
    for name in files:
        try:
            data = _parse(kind, repo.text(name))
        except OSError, ValueError, yaml.YAMLError:
            failing.append(name)
            continue
        value = _dig(data, path)
        present = value is not _MISSING and (
            "equals" not in detector or value == detector["equals"]
        )
        if present == expect_absent:
            failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


_MISSING = object()


def _parse(kind: str, text: str) -> object:
    if kind == "toml":
        return tomllib.loads(text)
    if kind == "json":
        return json.loads(text)
    return yaml.safe_load(text)


def _dig(data: object, path: list[str]) -> object:
    for part in path:
        if not isinstance(data, dict) or part not in data:
            return _MISSING
        data = data[part]
    return data


# What no declarative pattern can say. Each one is a plain function of the repo.

# A manifest and the lockfiles that pin it, in its folder or, for a workspace, a parent one.
LOCKFILES = {
    "pyproject.toml": ("uv.lock", "poetry.lock", "pdm.lock", "pylock.toml"),
    "Pipfile": ("Pipfile.lock",),
    "package.json": ("pnpm-lock.yaml", "package-lock.json", "yarn.lock", "bun.lock", "bun.lockb"),
}


def lockfiles(repo: Repo) -> Outcome:
    """Each dependency manifest has a lockfile beside it or in a parent folder; a
    `requirements*.txt` is its own lock when every line pins an exact version."""
    present = set(repo.files)
    manifests = [
        name
        for name in repo.files
        if PurePosixPath(name).name in LOCKFILES and _has_deps(repo, name)
    ]
    requirements = repo.matching("**/requirements*.txt")
    if not manifests and not requirements:
        return Outcome(NOT_APPLICABLE)
    unpinned = [name for name in requirements if not _pinned_requirements(repo, name)]
    missing = [
        name
        for name in manifests
        if not any(
            (folder / lock).as_posix().removeprefix("./") in present
            for folder in (PurePosixPath(name).parent, *PurePosixPath(name).parent.parents)
            for lock in LOCKFILES[PurePosixPath(name).name]
        )
    ] + unpinned
    return Outcome(FAIL, tuple(missing[:MAX_LOCATIONS])) if missing else Outcome(PASS)


def _pinned_requirements(repo: Repo, name: str) -> bool:
    """Every requirement of the file is `==` (an `-r` include or an option line aside)."""
    try:
        lines = repo.text(name).splitlines()
    except OSError, UnicodeDecodeError:
        return True
    wanted = [line.split("#")[0].strip() for line in lines]
    return all("==" in line for line in wanted if line and not line.startswith("-"))


def _has_deps(repo: Repo, manifest: str) -> bool:
    """A pyproject.toml of tool settings alone (no dependencies) needs no lockfile."""
    if PurePosixPath(manifest).name != "pyproject.toml":
        return True
    try:
        project = tomllib.loads(repo.text(manifest))
    except OSError, tomllib.TOMLDecodeError:
        return True
    return bool(project.get("project", {}).get("dependencies")) or bool(
        project.get("dependency-groups") or project.get("tool", {}).get("poetry")
    )


CONTAINER_FILES = ("**/Dockerfile", "**/Containerfile", "**/*.Dockerfile", "**/Dockerfile.*")
ROOT_USERS = frozenset({"root", "0", "0:0", "root:root"})


def non_root_containers(repo: Repo) -> Outcome:
    """The last `USER` of each image (the stage that runs) is not root."""
    files = repo.matching(*CONTAINER_FILES)
    if not files:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in files:
        try:
            lines = repo.text(name).splitlines()
        except OSError, UnicodeDecodeError:
            continue
        users = [line.split()[1] for line in lines if re.match(r"\s*USER\s+\S", line, re.I)]
        if not users or users[-1].lower() in ROOT_USERS:
            failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


def _lines(repo: Repo, name: str) -> list[str]:
    return repo.text(name).splitlines()


def images_by_digest(repo: Repo) -> Outcome:
    """Each `FROM` names an image by digest; `scratch`, build arguments and earlier stages
    (`FROM build`) aside."""
    files = repo.matching(*CONTAINER_FILES)
    if not files:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in files:
        stages: set[str] = set()
        for number, line in enumerate(_lines(repo, name), start=1):
            found = re.match(r"\s*FROM\s+(?:--\S+\s+)*(\S+)(?:\s+AS\s+(\S+))?", line, re.I)
            if not found:
                continue
            image = found.group(1)
            if found.group(2):
                stages.add(found.group(2).lower())
            if image.lower() in stages or image == "scratch" or "$" in image:
                continue
            if "@sha256:" not in image:
                failing.append(f"{name}:{number}")
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


WORKFLOWS = (".github/workflows/*.yml", ".github/workflows/*.yaml")


def workflow_permissions(repo: Repo) -> Outcome:
    """Each workflow sets `permissions:`, at its top or on every job."""
    files = repo.matching(*WORKFLOWS)
    if not files:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in files:
        try:
            workflow = yaml.safe_load(repo.text(name))
        except OSError, UnicodeDecodeError, yaml.YAMLError:
            continue
        if not isinstance(workflow, dict) or "permissions" in workflow:
            continue
        jobs = workflow.get("jobs")
        jobs = jobs.values() if isinstance(jobs, dict) else []
        if not jobs or not all(isinstance(job, dict) and "permissions" in job for job in jobs):
            failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


# Shared configurations that set `strict` themselves: extending one is strict.
STRICT_TS_PRESETS = re.compile(
    r'"extends"\s*:\s*"(astro/tsconfigs/(strict|strictest)|@tsconfig/strictest(/tsconfig\.json)?)"'
)


def strict_typescript(repo: Repo) -> Outcome:
    """Each `tsconfig.json` sets `strict`, or extends a strict preset (Astro's `strict` and
    `strictest`, `@tsconfig/strictest`); Nuxt's generated one is strict unless `nuxt.config`
    turns it off."""
    configs = [name for name in repo.matching("**/tsconfig.json") if "node_modules/" not in name]
    if not configs:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in configs:
        text = "\n".join(_lines(repo, name))
        folder = PurePosixPath(name).parent
        nuxt = [
            n
            for n in repo.files
            if PurePosixPath(n).parent == folder
            and PurePosixPath(n).name.startswith("nuxt.config.")
        ]
        if re.search(r'"strict"\s*:\s*true', text):
            continue
        if STRICT_TS_PRESETS.search(text) and not re.search(r'"strict"\s*:\s*false', text):
            continue
        if (
            nuxt
            and ".nuxt/tsconfig" in text
            and not any(re.search(r"strict\s*:\s*false", "\n".join(_lines(repo, n))) for n in nuxt)
        ):
            continue
        failing.append(name)
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


# End of life of each runtime line, from endoflife.date (checked 2026-10-20); bundled so that
# the check stays offline (T-46 refreshes it at release time).
END_OF_LIFE = {
    "python": {
        "3.8": "2024-10-07",
        "3.9": "2025-10-31",
        "3.10": "2026-10-31",
        "3.11": "2027-10-31",
        "3.12": "2028-10-31",
        "3.13": "2029-10-31",
        "3.14": "2030-10-31",
    },
    "node": {
        "16": "2023-09-11",
        "18": "2025-04-30",
        "20": "2026-04-30",
        "22": "2027-04-30",
        "24": "2028-04-30",
    },
}


def supported_runtimes(repo: Repo, today: str = "") -> Outcome:
    """The Python and Node versions a repo names (`.python-version`, `requires-python`,
    `.nvmrc`, `engines.node`, image tags) are still supported upstream."""
    today = today or datetime.date.today().isoformat()
    named: list[tuple[str, str, str]] = []  # runtime, version, where
    for name in repo.matching("**/.python-version"):
        named += [("python", line.strip(), name) for line in _lines(repo, name)[:1]]
    for name in repo.matching("**/.nvmrc", "**/.node-version"):
        named += [("node", line.strip().lstrip("v"), name) for line in _lines(repo, name)[:1]]
    for name in repo.matching("**/pyproject.toml"):
        for line in _lines(repo, name):
            found = re.match(r'\s*requires-python\s*=\s*["\'][^0-9]*(\d+\.\d+)', line)
            if found:
                named.append(("python", found.group(1), name))
    for name in repo.matching("**/package.json"):
        if "node_modules/" in name:
            continue
        try:
            engines = json.loads("\n".join(_lines(repo, name)) or "{}").get("engines", {})
        except ValueError:
            continue
        found = (
            re.search(r"(\d+)", str(engines.get("node", ""))) if isinstance(engines, dict) else None
        )
        if found:
            named.append(("node", found.group(1), name))
    for name in repo.matching(*CONTAINER_FILES):
        for line in _lines(repo, name):
            found = re.match(
                r"\s*FROM\s+(?:--\S+\s+)*(?:\S+/)?(python|node):v?(\d+(?:\.\d+)?)", line, re.I
            )
            if found:
                named.append((found.group(1).lower(), found.group(2), name))
    if not named:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for runtime, version, where in named:
        line = ".".join(version.split(".")[:2]) if runtime == "python" else version.split(".")[0]
        end = END_OF_LIFE[runtime].get(line)
        if end and end < today:
            failing.append(f"{where} ({runtime} {line}, end of life {end})")
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


COMPOSE_FILES = ("**/compose.y*ml", "**/compose.*.y*ml", "**/docker-compose*.y*ml")


def hardened_compose(repo: Repo) -> Outcome:
    """Each compose service runs with a read-only file system, every capability dropped and
    no privilege escalation."""
    files = repo.matching(*COMPOSE_FILES)
    if not files:
        return Outcome(NOT_APPLICABLE)
    failing = []
    for name in files:
        try:
            compose = yaml.safe_load(repo.text(name))
        except OSError, UnicodeDecodeError, yaml.YAMLError:
            continue
        services = compose.get("services") if isinstance(compose, dict) else None
        for service, settings in (services or {}).items():
            if not isinstance(settings, dict):
                continue
            hardened = (
                settings.get("read_only") is True
                and "ALL" in [str(cap).upper() for cap in settings.get("cap_drop") or []]
                and any(
                    "no-new-privileges" in str(opt) for opt in settings.get("security_opt") or []
                )
            )
            if not hardened:
                failing.append(f"{name} ({service})")
    return Outcome(FAIL, tuple(failing[:MAX_LOCATIONS])) if failing else Outcome(PASS)


def committed_migrations(repo: Repo) -> Outcome:
    """Each Django app with models has its `migrations/` package committed."""
    apps = [
        PurePosixPath(name).parent
        for name in repo.matching("**/models.py", "**/models/__init__.py")
        if "site-packages/" not in name
    ]
    apps = [app.parent if app.name == "models" else app for app in apps]
    apps = [app for app in apps if (app / "apps.py").as_posix() in set(repo.files)]
    if not apps:
        return Outcome(NOT_APPLICABLE)
    present = set(repo.files)
    missing = [
        app.as_posix() for app in apps if (app / "migrations/__init__.py").as_posix() not in present
    ]
    return Outcome(FAIL, tuple(missing[:MAX_LOCATIONS])) if missing else Outcome(PASS)


LINTER_FILES = ("**/ruff.toml", "**/.ruff.toml", "**/.flake8", "**/.pylintrc", "**/pylintrc")
LINTER_SECTIONS = re.compile(r"(?m)^\[(tool\.ruff|tool\.pylint|flake8|pylint)")


def python_linter(repo: Repo) -> Outcome:
    """ruff, flake8 or pylint configured: its own file, or its section in a shared one."""
    if repo.matching(*LINTER_FILES):
        return Outcome(PASS)
    for name in repo.matching("**/pyproject.toml", "**/setup.cfg", "**/tox.ini"):
        if LINTER_SECTIONS.search("\n".join(_lines(repo, name))):
            return Outcome(PASS, (name,))
    return Outcome(FAIL, detail="no ruff, flake8 or pylint settings")


# Files of trained weights, by the libraries that write them.
MODEL_FILES = tuple(
    f"**/*.{suffix}"
    for suffix in ("pt", "pth", "ckpt", "joblib", "pkl", "pickle", "onnx", "safetensors", "h5")
)
MODEL_MANIFEST_SUFFIX = ".manifest.json"
MODEL_MANIFEST_KEYS = ("code_sha256", "metrics")


def traced_models(repo: Repo) -> Outcome:
    """Each committed model has its `<model>.manifest.json`, naming its code's hash and metrics."""
    models = [name for name in repo.matching(*MODEL_FILES) if "site-packages/" not in name]
    if not models:
        return Outcome(NOT_APPLICABLE)
    untraced = []
    for name in models:
        try:
            manifest = json.loads(repo.text(name + MODEL_MANIFEST_SUFFIX))
        except ValueError:
            manifest = None
        if not isinstance(manifest, dict) or any(
            key not in manifest for key in MODEL_MANIFEST_KEYS
        ):
            untraced.append(name)
    return Outcome(FAIL, tuple(untraced[:MAX_LOCATIONS])) if untraced else Outcome(PASS)


def _forge(
    repo: Repo, judge: Callable[[forge.Settings], list[str] | None], section: str
) -> Outcome:
    """A setting of the repo's GitHub project: `judge` lists what is missing (empty: met), or
    None when GitHub does not offer it to this repo; a gap ends with its settings page."""
    found = forge.settings(repo.root)
    if found is None:
        return Outcome(NOT_APPLICABLE, detail=forge.UNKNOWN if forge.ENABLED else "")
    missing = judge(found)
    if missing is None:
        return Outcome(NOT_APPLICABLE)
    if not missing:
        return Outcome(PASS)
    return Outcome(FAIL, detail=f"{'; '.join(missing)}: {found.page(section)}")


def protected_branch(repo: Repo) -> Outcome:
    def judge(found: forge.Settings) -> list[str]:
        wanted = {"non_fast_forward": "force pushes allowed", "deletion": "deletion allowed"}
        if not found.merge_commits:
            wanted["required_linear_history"] = "linear history not required"
        branch = found.default_branch
        return [
            f"{branch}: {why}" for rule, why in wanted.items() if rule not in found.branch_rules
        ]

    return _forge(repo, judge, "rules")


def forge_secret_scanning(repo: Repo) -> Outcome:
    def judge(found: forge.Settings) -> list[str] | None:
        if found.secret_scanning is None:
            return None
        return [
            what
            for what, on in (
                ("secret scanning off", found.secret_scanning),
                ("push protection off", found.push_protection),
            )
            if not on
        ]

    return _forge(repo, judge, "security_analysis")


def forge_dependabot_alerts(repo: Repo) -> Outcome:
    def judge(found: forge.Settings) -> list[str] | None:
        if found.vulnerability_alerts is None:
            return None
        if not found.vulnerability_alerts:
            return ["Dependabot alerts off"]
        return [] if found.security_updates else ["Dependabot security updates off"]

    return _forge(repo, judge, "security_analysis")


def forge_private_reporting(repo: Repo) -> Outcome:
    def judge(found: forge.Settings) -> list[str] | None:
        if not found.public or found.private_reporting is None:
            return None
        return [] if found.private_reporting else ["private vulnerability reporting off"]

    return _forge(repo, judge, "security_analysis")


def forge_code_scanning(repo: Repo) -> Outcome:
    def judge(found: forge.Settings) -> list[str] | None:
        if found.code_scanning is None:
            return None
        return [] if found.code_scanning else ["code scanning not set up"]

    return _forge(repo, judge, "security_analysis")


PYTHON_CHECKS: dict[str, Callable[[Repo], Outcome]] = {
    "lockfiles": lockfiles,
    "non_root_containers": non_root_containers,
    "images_by_digest": images_by_digest,
    "workflow_permissions": workflow_permissions,
    "strict_typescript": strict_typescript,
    "supported_runtimes": supported_runtimes,
    "hardened_compose": hardened_compose,
    "committed_migrations": committed_migrations,
    "python_linter": python_linter,
    "traced_models": traced_models,
    "protected_branch": protected_branch,
    "forge_secret_scanning": forge_secret_scanning,
    "forge_dependabot_alerts": forge_dependabot_alerts,
    "forge_private_reporting": forge_private_reporting,
    "forge_code_scanning": forge_code_scanning,
}
