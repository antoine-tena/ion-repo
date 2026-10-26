"""Converters of `kiln fix`: what an existing CI lacks, and an `.env` left in git (T-173).

The text of a workflow is edited in place, line by line, as in `ci`; YAML is parsed to find the
lines, never dumped back. A missing job (lint, tests, audit) comes as a workflow of its own, next
to the repo's: its jobs and their setup are left as they are.
"""

import re
from collections.abc import Callable

import yaml  # brought by copier

from kiln.grid import checks
from kiln.grid.detectors import (
    EXPRESSION,
    WORKFLOWS,
    untrusted_expressions,
    workflow_scripts,
)
from kiln.grid.facts import Repo
from kiln.grid.fixers import Fixer, register
from kiln.grid.fixers.ci import _write, write_workflow
from kiln.shell import capture, run
from kiln.stack import PNPM_LENIENT_BUILDS

# A bare context read (`github.event.issue.title`): moved to `env:` as it is. Anything more (a
# function, `||`) is left to judgment.
CONTEXT_PATH = re.compile(r"[\w.\-\[\]'\"*]+")
# The shells where `${NAME}` reads the environment.
POSIX_SHELLS = ("bash", "sh")


def env_name(path: str) -> str:
    """`github.event.pull_request.title` → `PULL_REQUEST_TITLE`."""
    path = re.sub(r"^github\.(event\.)?", "", path)
    return re.sub(r"[^A-Za-z0-9]+", "_", path).strip("_").upper()


def move_to_env(repo: Repo) -> list[str]:
    """An outsider's text expanded in a `run:` (`${{ github.event.issue.title }}`) passed
    through the step's `env:` instead and read as `${ISSUE_TITLE}`: data for the shell, never
    code, as zizmor fixes it. A workflow on a non-POSIX shell (Windows, `shell: pwsh`), an
    expression that is more than a context read and `actions/github-script` stay for judgment."""
    changed = []
    for name in repo.matching(*WORKFLOWS):
        text = repo.text(name)
        try:
            workflow = yaml.safe_load(text)
            scripts = workflow_scripts(text)
        except yaml.YAMLError:
            continue
        if not _posix_shell(workflow):
            continue
        lines = text.splitlines(keepends=True)
        insertions: list[tuple[int, str]] = []
        for step, value in scripts:
            insertion = _step_to_env(lines, step, value)
            if insertion is not None:
                insertions.append(insertion)
        if not insertions:
            continue
        for at, block in sorted(insertions, reverse=True):
            lines.insert(at, block)
        _write(repo, name, "".join(lines))
        changed.append(name)
    return changed


def _posix_shell(workflow: object) -> bool:
    """No Windows runner nor `defaults: run: shell:` other than bash or sh, in the workflow or a
    job."""
    if not isinstance(workflow, dict):
        return False
    jobs = workflow.get("jobs")
    scopes = [workflow, *(jobs.values() if isinstance(jobs, dict) else [])]
    for scope in scopes:
        if not isinstance(scope, dict):
            continue
        if "windows" in str(scope.get("runs-on", "")).lower():
            return False
        defaults = scope.get("defaults")
        shell = defaults.get("run", {}).get("shell") if isinstance(defaults, dict) else None
        if shell is not None and str(shell).split()[0] not in POSIX_SHELLS:
            return False
    return True


def _step_to_env(
    lines: list[str], step: yaml.MappingNode, value: yaml.ScalarNode
) -> tuple[int, str] | None:
    """Rewrites the `run:` of `step` in `lines` and returns the `env:` lines to insert (where,
    what), or None when the step stays as it is."""
    keys = {key.value: (key, node) for key, node in step.value if isinstance(key, yaml.ScalarNode)}
    run_key, run_value = keys.get("run", (None, None))
    if run_value is not value or run_key is None:
        return None  # a `script:`: JavaScript, where the quoting differs
    shell = keys.get("shell", (None, None))[1]
    if isinstance(shell, yaml.ScalarNode) and shell.value.split()[0] not in POSIX_SHELLS:
        return None
    found = untrusted_expressions(value.value)
    paths = {expression["inner"] for expression in found}
    if not paths or not all(CONTEXT_PATH.fullmatch(path) for path in paths):
        return None
    names = {path: env_name(path) for path in sorted(paths)}
    env = keys.get("env", (None, None))[1]
    existing: dict[str, str] = {}
    if env is not None:
        if not isinstance(env, yaml.MappingNode) or env.flow_style or not env.value:
            return None
        existing = {key.value: node.value for key, node in env.value}
        for path, variable in names.items():
            if variable in existing and existing[variable] != f"${{{{ {path} }}}}":
                return None
    first = value.start_mark.line
    last = value.end_mark.line if value.end_mark.column > 0 else value.end_mark.line - 1
    for index in range(first, last + 1):
        lines[index] = EXPRESSION.sub(
            lambda match: (
                f"${{{names[match['inner']]}}}" if match["inner"] in names else match.group(0)
            ),
            lines[index],
        )
    added = [(variable, path) for path, variable in names.items() if variable not in existing]
    if env is not None:
        indent = " " * env.value[0][0].start_mark.column
        at = env.value[0][0].start_mark.line
        block = "".join(f"{indent}{variable}: ${{{{ {path} }}}}\n" for variable, path in added)
        return at, block
    if not lines[last].endswith("\n"):
        lines[last] += "\n"
    indent = " " * run_key.start_mark.column
    entries = "".join(f"{indent}  {variable}: ${{{{ {path} }}}}\n" for variable, path in added)
    return last + 1, f"{indent}env:\n{entries}"


def _github_ci(repo: Repo) -> bool:
    """The repo runs GitHub Actions: a missing job is added next to its workflows. A repo with
    no CI gets one from CI-PRESENT's converter; another forge's is left as it is."""
    return bool(repo.matching(*WORKFLOWS))


def _free(repo: Repo, name: str) -> bool:
    return not (repo.root / name).exists()


def _install(repo: Repo, folder: str, *, python: bool, node: bool) -> list[str]:
    """How CI installs what the checks of `folder` run, from its lock."""
    base = "" if folder == "." else f"{folder}/"
    prefix = "" if folder == "." else f"cd {folder} && "
    names = set(repo.files)
    steps = []
    if python and f"{base}uv.lock" in names:
        steps.append(f"{prefix}uv sync --locked")
    elif python:
        requirements = sorted(
            name[len(base) :]
            for name in repo.matching(f"{base}requirements*.txt")
            if "/" not in name[len(base) :]
        )
        listed = "".join(f"-r {name} " for name in requirements)
        steps.append(f"{prefix}pip install {listed}pytest")
    if node and f"{base}pnpm-lock.yaml" in names:
        steps.append(f"{prefix}pnpm install --frozen-lockfile {PNPM_LENIENT_BUILDS}")
    elif node:
        install = "npm ci" if f"{base}package-lock.json" in names else "npm install"
        steps.append(f"{prefix}{install}")
    return steps


def _ci_command(check: checks.Check) -> tuple[str, str] | None:
    """The check as CI runs it after the install, and its ecosystem (python, node); None for a
    tool CI would have to set up first (yarn, bun)."""
    argv = list(check.argv)
    if argv[0] in ("npm", "pnpm"):
        return " ".join(argv), "node"
    if argv[:2] == ["uv", "run"]:
        return " ".join(argv), "python"
    if argv[0] == "ruff":
        return "uvx " + " ".join(argv), "ruff"
    if argv[0] in ("pytest", "python"):
        command = "python -m pytest -q" if argv[0] == "pytest" else " ".join(argv)
        return command, "python"
    return None


def _job_steps(repo: Repo, wanted: list[checks.Check]) -> list[str]:
    """Install then run `wanted`, folder by folder."""
    steps: list[str] = []
    for folder in dict.fromkeys(check.directory for check in wanted):
        commands = [
            command
            for check in wanted
            if check.directory == folder and (command := _ci_command(check)) is not None
        ]
        if not commands:
            continue
        ecosystems = {ecosystem for _, ecosystem in commands}
        steps += _install(repo, folder, python="python" in ecosystems, node="node" in ecosystems)
        prefix = "" if folder == "." else f"cd {folder} && "
        steps += [f"{prefix}{command}" for command, _ in commands]
    return steps


def _is_lint(check: checks.Check) -> bool:
    return "ruff" in check.argv or check.argv[1:] == ("run", "lint")


def _is_test(check: checks.Check) -> bool:
    return "pytest" in check.argv or "manage.py" in check.argv or check.argv[1:] == ("run", "test")


def _add_job(repo: Repo, name: str, job: str, keep: Callable[[checks.Check], bool]) -> list[str]:
    if not _github_ci(repo) or not _free(repo, name):
        return []
    wanted = [check for check in checks.find(repo.root) if keep(check)]
    steps = _job_steps(repo, wanted)
    if not steps:
        return []
    write_workflow(repo, name, job, steps)
    return [name]


def add_lint_job(repo: Repo) -> list[str]:
    """The linters the repo declares (ruff, a `lint` script), run by a workflow of their own."""
    return _add_job(repo, ".github/workflows/lint.yml", "lint", _is_lint)


def add_test_job(repo: Repo) -> list[str]:
    """The tests the repo declares (pytest, `manage.py test`, a `test` script), run by a
    workflow of their own."""
    return _add_job(repo, ".github/workflows/tests.yml", "tests", _is_test)


def _audit_steps(repo: Repo) -> list[str]:
    steps = []
    for lock in sorted(repo.matching("uv.lock", "*/uv.lock")):
        steps.append(_in(lock, "uv audit --locked --preview-features audit-command"))
    for requirements in sorted(repo.matching("requirements*.txt", "*/requirements*.txt")):
        folder = requirements.rpartition("/")[0]
        if f"{folder}/uv.lock".lstrip("/") not in repo.files:
            steps.append(_in(requirements, f"uvx pip-audit -r {requirements.rpartition('/')[2]}"))
    for lock in sorted(repo.matching("pnpm-lock.yaml", "*/pnpm-lock.yaml")):
        steps.append(_in(lock, "pnpm audit --prod --audit-level high"))
    for lock in sorted(repo.matching("package-lock.json", "*/package-lock.json")):
        steps.append(_in(lock, "npm audit --omit=dev --audit-level=high"))
    return steps


def _in(path: str, command: str) -> str:
    """`command` run in the folder of `path`."""
    folder = path.rpartition("/")[0]
    return f"cd {folder} && {command}" if folder else command


def add_audit(repo: Repo) -> list[str]:
    """Known vulnerabilities of the locked dependencies looked up on each push and every Monday:
    `uv audit`, pip-audit for requirements alone, `pnpm audit` or `npm audit`."""
    name = ".github/workflows/audit.yml"
    if not _github_ci(repo) or not _free(repo, name):
        return []
    steps = _audit_steps(repo)
    if not steps:
        return []
    write_workflow(repo, name, "audit", steps, weekly=True)
    return [name]


ENV_FILES = ("**/.env", "**/.env.local", "**/.env.production", "**/.env.*.local")
ENV_IGNORED = (".env", ".env.local", ".env.production", ".env.*.local")
ENV_LINE = re.compile(r"^\s*(?:export\s+)?(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=")


def untrack_env(repo: Repo) -> list[str]:
    """An `.env` taken out of git (left on disk), ignored from now on, and an `.env.example`
    beside it with its keys and no values. Its secrets stay in the history: rotate them."""
    pathspecs = [f":(glob){pattern}" for pattern in ENV_FILES]
    tracked = capture(["git", "ls-files", "--", *pathspecs], repo.root)
    names = tracked.splitlines()
    if not names:
        return []
    run(["git", "rm", "-q", "--cached", "--", *names], repo.root)
    changed = []
    gitignore = repo.root / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    present = {line.strip() for line in text.splitlines()}
    missing = [pattern for pattern in ENV_IGNORED if pattern not in present]
    if missing:
        ending = "" if not text or text.endswith("\n") else "\n"
        _write(repo, ".gitignore", f"{text}{ending}{chr(10).join(missing)}\n")
        changed.append(".gitignore")
    for name in names:
        folder = name.rpartition("/")[0]
        example = f"{folder}/.env.example" if folder else ".env.example"
        if (repo.root / example).exists() or example in changed:
            continue
        keys = [
            found["key"] for line in repo.text(name).splitlines() if (found := ENV_LINE.match(line))
        ]
        _write(repo, example, "".join(f"{key}=\n" for key in dict.fromkeys(keys)))
        changed.append(example)
    return changed


register(Fixer("move_to_env", move_to_env, "event text passed to scripts through env"))
register(Fixer("add_lint_job", add_lint_job, "the repo's linters run in CI", network=True))
register(Fixer("add_test_job", add_test_job, "the repo's tests run in CI", network=True))
register(
    Fixer("add_audit", add_audit, "dependencies audited for known vulnerabilities", network=True)
)
register(Fixer("untrack_env", untrack_env, ".env out of git, its keys in .env.example"))
