"""The repo's own checks, which judge each converter of `kiln fix`: found, run, told apart.

Found at the root and one folder down (`backend/`, `frontend/`: most repos of the training fleet
keep their code there): `kiln check --all` in a kiln repo; elsewhere the lint, types and tests
the manifests declare (ruff, mypy, pytest, or a Django project's `manage.py test`; the `lint`,
`typecheck` and `test` scripts of a package.json, run by npm, pnpm, yarn or bun, after its lock).
Each one runs with a timeout: a test suite waiting for an absent database never hangs the fix.

Before the first converter each check runs once. One whose tool is missing, already red or timed
out cannot judge, and the summary names it with why; the green ones judge every converter. The
output of a check a converter turned red is kept in the git folder, where `kiln score
--roadmap` hands the gap to Claude with its log.
"""

import json
import os
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

from kiln.shell import INSTALL_HINTS

CHECK_TIMEOUT = 600
# Kept from a failing check's output: its end, where the failure is said.
LOG_TAIL = 20_000
TOOL_HINTS = {
    **INSTALL_HINTS,
    "yarn": "corepack enable yarn",
    "bun": "curl -fsSL https://bun.sh/install | bash",
    "npm": "Node.js 24: https://nodejs.org/en/download",
    "kiln": "uv tool install keramos-kiln",
}
# Lock file, in search order, and the package manager that wrote it.
NODE_LOCKS = (
    ("pnpm-lock.yaml", "pnpm"),
    ("yarn.lock", "yarn"),
    ("bun.lock", "bun"),
    ("bun.lockb", "bun"),
)
NODE_SCRIPTS = ("lint", "typecheck", "test")
MANIFESTS = ("pyproject.toml", "package.json", "manage.py")
SKIPPED_FOLDERS = frozenset({"node_modules", "dist", "build", "venv"})
LOGS = Path("kiln") / "fix"
# The tag of the images `kiln fix` builds to prove a converter: overwritten at each build.
BUILT_IMAGE = "localhost/kiln-fix-check:latest"

GREEN, RED, MISSING, TIMEOUT = "green", "red", "missing", "timeout"


@dataclass(frozen=True)
class Check:
    argv: tuple[str, ...]
    directory: str = "."

    def __str__(self) -> str:
        command = " ".join(self.argv)
        return command if self.directory == "." else f"{command} (in {self.directory}/)"


@dataclass(frozen=True)
class Result:
    check: Check
    status: str  # green, red, missing, timeout
    log: str = ""

    @property
    def ok(self) -> bool:
        return self.status == GREEN

    @property
    def reason(self) -> str:
        """Why the check cannot judge, as the summary says it."""
        if self.status == MISSING:
            tool = self.check.argv[0]
            return f"{tool} missing ({TOOL_HINTS.get(tool, 'install it')})"
        if self.status == TIMEOUT:
            return f"`{self.check}` timed out after {CHECK_TIMEOUT} s"
        return f"`{self.check}` was red before the fix"


def find(root: Path) -> list[Check]:
    """The repo's checks, the whole repo before and after alike: `kiln check` alone looks at the
    branch's changes, and would blame a converter for the older debt of a file it touched."""
    if (root / ".copier-answers.yml").exists():
        return [Check(("kiln", "check", "--all"))]
    folders = [
        ".",
        *sorted(
            child.name
            for child in root.iterdir()
            if child.is_dir()
            and not child.name.startswith(".")
            and child.name not in SKIPPED_FOLDERS
            and any((child / manifest).exists() for manifest in MANIFESTS)
        ),
    ]
    return [check for folder in folders for check in _checks_in(root / folder, folder)]


def _checks_in(path: Path, folder: str) -> list[Check]:
    checks: list[Check] = []
    runner = ("uv", "run") if (path / "uv.lock").exists() else ()
    tools: dict[str, object] = {}
    if (path / "pyproject.toml").exists():
        try:
            project = tomllib.loads((path / "pyproject.toml").read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            project = {}
        tools = project.get("tool", {})
    if "ruff" in tools or (path / "ruff.toml").exists():
        checks.append(Check((*runner, "ruff", "check"), folder))
    mypy = tools.get("mypy")
    if isinstance(mypy, dict):
        # The files its config names, which `mypy` alone checks: `.` would read the rest too.
        checks.append(Check((*runner, "mypy", *([] if mypy.get("files") else ["."])), folder))
    has_pytest = "pytest" in tools or (path / "pytest.ini").exists() or (path / "tests").is_dir()
    if has_pytest:
        checks.append(Check((*runner, "pytest", "-q"), folder))
    elif (path / "manage.py").exists():
        checks.append(Check((*runner, "python", "manage.py", "test"), folder))
    checks += _node_checks(path, folder)
    return checks


def _node_checks(path: Path, folder: str) -> list[Check]:
    try:
        package = json.loads((path / "package.json").read_text(encoding="utf-8"))
    except OSError, ValueError:
        return []
    scripts = package.get("scripts") if isinstance(package, dict) else None
    if not isinstance(scripts, dict):
        return []
    manager = next((name for lock, name in NODE_LOCKS if (path / lock).exists()), "npm")
    return [Check((manager, "run", name), folder) for name in NODE_SCRIPTS if name in scripts]


def run(root: Path, check: Check) -> Result:
    if shutil.which(check.argv[0]) is None:
        return Result(check, MISSING)
    # No bytecode written: `git add --all` would commit it in a repo that does not ignore it.
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        done = subprocess.run(
            check.argv,
            cwd=root / check.directory,
            env=environment,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=CHECK_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as expired:
        output = _text(expired.stdout) + _text(expired.stderr)
        return Result(check, TIMEOUT, output[-LOG_TAIL:])
    if done.returncode != 0:
        return Result(check, RED, (done.stdout + done.stderr)[-LOG_TAIL:])
    return Result(check, GREEN)


def image_builds(root: Path, changed: list[str]) -> list[Check]:
    """A build of each container file among `changed`, by podman or docker, from its folder;
    none without either."""
    builder = shutil.which("podman") or shutil.which("docker")
    if builder is None:
        return []
    names = {"Dockerfile", "Containerfile"}
    return [
        Check(
            (
                Path(builder).name,
                "build",
                "--quiet",
                "-t",
                BUILT_IMAGE,
                "-f",
                name,
                str(Path(name).parent),
            ),
        )
        for name in changed
        if Path(name).name in names
        or Path(name).name.startswith(("Dockerfile.", "Containerfile."))
        or name.endswith(".Dockerfile")
    ]


def first_failure(root: Path, checks: list[Check]) -> Result | None:
    """The first of the checks that does not pass, None when they all do."""
    for check in checks:
        result = run(root, check)
        if not result.ok:
            return result
    return None


def _text(output: str | bytes | None) -> str:
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output or ""


def logs_dir(root: Path) -> Path | None:
    """Where the logs of reverted converters live: the git folder, never committed."""
    try:
        common = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        return None
    return Path(common) / LOGS


def keep_log(root: Path, rule: str, result: Result, branch: str = "") -> Path | None:
    """The failing output, headed by the branch the converter's commit was set aside on."""
    folder = logs_dir(root)
    if folder is None:
        return None
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{rule}.log"
    head = f"# kiln fix's commit, set aside: git switch {branch}\n" if branch else ""
    path.write_text(f"{head}$ {result.check}\n{result.log}", encoding="utf-8")
    return path


def forget_log(root: Path, rule: str) -> None:
    folder = logs_dir(root)
    if folder is not None:
        (folder / f"{rule}.log").unlink(missing_ok=True)


def reverted(root: Path) -> dict[str, Path]:
    """The rules whose converter `kiln fix` had to undo, with the log of the check it broke."""
    folder = logs_dir(root)
    if folder is None or not folder.is_dir():
        return {}
    return {path.stem: path for path in sorted(folder.glob("*.log"))}
