"""The proof a removal must pass, in steps: the type checker, then the tests, then behaviour
compared test by test with the run before.

A baseline runs first. A step already red there cannot prove anything and is left out (said);
the tests are compared one by one, so a repo with known failures can still be slimmed: what
passed must still pass, and every test must still be collected. Without tests, nothing is
proven and nothing is removed.
"""

import json
import os
import shutil
import subprocess
import tempfile
import time
import tomllib
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

TYPES, TESTS = "types", "tests"
# No bytecode left in the tree by the runs: nothing for `git add` to pick up.
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


@dataclass(frozen=True)
class Step:
    name: str  # what the user reads: `backend: mypy`, `frontend: pnpm run typecheck`
    kind: str  # types, tests
    command: tuple[str, ...]
    per_test: bool = False  # pytest: outcomes compared one by one
    folder: str = ""  # the project it runs in, relative to the root ("" for the root)


@dataclass
class Baseline:
    steps: list[Step]
    outcomes: dict[str, str] = field(default_factory=dict)  # pytest test id → passed, failed…
    dropped: list[str] = field(default_factory=list)  # steps red before anything was removed
    executed: dict[str, set[int]] | None = None  # lines the tests ran, by file
    seconds: float = 0.0  # one run of every step: what each proof costs

    @property
    def proves(self) -> bool:
        return any(step.kind == TESTS for step in self.steps)


def projects(root: Path, files: tuple[str, ...], manifest: str) -> list[str]:
    """The folders holding a `manifest` (`pyproject.toml`, `package.json`): a monorepo's
    backend and frontend, each with its own tests."""
    folders = {
        str(PurePosixPath(name).parent) for name in files if PurePosixPath(name).name == manifest
    }
    return sorted(
        "" if folder == "." else folder
        for folder in folders
        if "node_modules" not in folder and (root / folder / manifest).is_file()
    )


def steps(root: Path, files: tuple[str, ...]) -> list[Step]:
    """The type checkers and tests of each project of the repo, from its manifests."""
    found: list[Step] = []
    for folder in projects(root, files, "pyproject.toml"):
        found += _python_steps(root / folder, folder)
    for folder in projects(root, files, "package.json"):
        found += _node_steps(root / folder, folder)
    return found


def _python_steps(project: Path, folder: str) -> list[Step]:
    try:
        tools = tomllib.loads((project / "pyproject.toml").read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return []
    tools = tools.get("tool", {})
    runner = ("uv", "run", "--exact") if (project / "uv.lock").is_file() else ()
    prefix = f"{folder}: " if folder else ""
    found = [
        Step(f"{prefix}{checker}", TYPES, (*runner, *command), folder=folder)
        for checker, command in (
            ("mypy", ("mypy", ".")),
            ("pyright", ("pyright",)),
            ("ty", ("ty", "check")),
        )
        if checker in tools
    ]
    if "pytest" in tools or any(
        (project / name).exists() for name in ("tests", "conftest.py", "pytest.ini")
    ):
        found.append(Step(f"{prefix}pytest", TESTS, (*runner, "pytest"), True, folder))
    return found


def _node_steps(project: Path, folder: str) -> list[Step]:
    manager = "pnpm" if (project / "pnpm-lock.yaml").is_file() else "npm"
    try:
        scripts = json.loads((project / "package.json").read_text(encoding="utf-8"))
    except ValueError:
        return []
    scripts = scripts.get("scripts", {}) if isinstance(scripts, dict) else {}
    prefix = f"{folder}: " if folder else ""
    return [
        Step(f"{prefix}{manager} run {script}", kind, (manager, "run", script), folder=folder)
        for script, kind in (
            ("typecheck", TYPES),
            ("lint", TYPES),
            ("test", TESTS),
            ("build", TESTS),
        )
        if script in scripts
    ]


def baseline(root: Path, wanted: list[Step]) -> Baseline:
    """Each step run once on the untouched tree, then the tests once more under coverage, so
    that code the tests run is known to be alive."""
    result = Baseline(steps=[])
    started = time.monotonic()
    for step in wanted:
        if shutil.which(step.command[0]) is None:
            result.dropped.append(f"{step.name}: not installed")
            continue
        if step.per_test:
            outcomes = _pytest(root, step)
            if not any(outcome == "passed" for outcome in (outcomes or {}).values()):
                result.dropped.append(f"{step.name}: no test passes")
                continue
            result.outcomes.update(outcomes or {})
            result.steps.append(step)
        elif _run(root / step.folder, step.command):
            result.steps.append(step)
        else:
            result.dropped.append(f"{step.name}: red before any removal")
    result.seconds = time.monotonic() - started
    result.executed = coverage(root, result)
    return result


def holds(root: Path, base: Baseline, touched: list[str] | None = None) -> str:
    """ "" when the tree still passes the steps of the baseline, else what broke. With
    `touched`, only the steps of the projects holding those paths run: a removal in the
    backend cannot break the frontend's tests."""
    for step in base.steps:
        if touched is not None and not any(_inside(path, step.folder) for path in touched):
            continue
        if step.per_test:
            outcomes = _pytest(root, step)
            if outcomes is None:
                return f"{step.name}: the tests no longer run"
            broken = [
                test
                for test, outcome in base.outcomes.items()
                if _belongs(test, step.folder)
                and outcome == "passed"
                and outcomes.get(test) != "passed"
            ]
            if broken:
                return f"{step.name}: {broken[0]} {outcomes.get(broken[0], 'missing')}"
        elif not _run(root / step.folder, step.command):
            return f"{step.name} turned red"
    return ""


def _run(root: Path, command: tuple[str, ...]) -> bool:
    done = subprocess.run(command, cwd=root, env=ENV, capture_output=True, check=False)
    return done.returncode == 0


def _pytest(root: Path, step: Step, data: Path | None = None) -> dict[str, str] | None:
    """Each test's outcome (JUnit XML); None when nothing was collected. With `data`, the run
    goes under coverage, pytest started as its own script: the same import path as without."""
    with tempfile.TemporaryDirectory(prefix="kiln-proof-") as scratch:
        report = Path(scratch) / "junit.xml"
        options = ("-q", "-p", "no:cacheprovider", f"--junitxml={report}")
        command: tuple[str, ...] = (*step.command, *options)
        if data is not None:
            # coverage brought for this run only, the repo's dependencies untouched.
            script = 'exec coverage run --data-file="$0" "$(command -v pytest)" "$@"'
            runner = step.command[: step.command.index("pytest")]
            runner = tuple(part for part in runner if part != "--exact")
            if runner[:2] == ("uv", "run"):
                runner = (*runner, "--with", "coverage")
            command = (*runner, "sh", "-c", script, str(data), *options)
        subprocess.run(command, cwd=root / step.folder, env=ENV, capture_output=True, check=False)
        outcomes = _junit(report)
        return {_test_id(step.folder, test): outcome for test, outcome in outcomes.items()} or None


def _test_id(folder: str, test: str) -> str:
    """A test named from the root: two projects may each have a `tests.test_api::test_a`."""
    return f"{folder}/{test}" if folder else test


def _inside(path: str, folder: str) -> bool:
    return not folder or path.startswith(f"{folder}/")


def _belongs(test: str, folder: str) -> bool:
    return test.startswith(f"{folder}/") if folder else True


def _junit(report: Path) -> dict[str, str]:
    try:
        tree = ElementTree.parse(report)
    except OSError, ElementTree.ParseError:
        return {}
    outcomes: dict[str, str] = {}
    for case in tree.iter("testcase"):
        test = f"{case.get('classname', '')}::{case.get('name', '')}"
        outcome = "passed"
        for tag in ("failure", "error", "skipped"):
            if case.find(tag) is not None:
                outcome = {"failure": "failed"}.get(tag, tag)
        outcomes[test] = outcome
    return outcomes


def _executed(root: Path, step: Step, data: Path) -> dict[str, set[int]] | None:
    """The lines run, by path relative to the root (`coverage json`)."""
    out = data.with_suffix(".json")
    runner = ("uv", "run", "--with", "coverage") if step.command[0] == "uv" else ()
    subprocess.run(
        (*runner, "coverage", "json", f"--data-file={data}", "-o", str(out)),
        cwd=root / step.folder,
        capture_output=True,
        check=False,
    )
    try:
        files = json.loads(out.read_text(encoding="utf-8")).get("files", {})
    except OSError, ValueError:
        return None
    executed: dict[str, set[int]] = {}
    for name, details in files.items():
        path = Path(name) if Path(name).is_absolute() else root / step.folder / name
        if path.is_relative_to(root):
            lines = set(details.get("executed_lines", []))
            executed[path.relative_to(root).as_posix()] = lines
    return executed


def coverage(root: Path, base: Baseline) -> dict[str, set[int]] | None:
    """The lines the tests of every project run, by file; None when coverage cannot run, or
    its run does not pass the same tests (then it measured something else)."""
    executed: dict[str, set[int]] = {}
    for step in (item for item in base.steps if item.per_test):
        with tempfile.TemporaryDirectory(prefix="kiln-coverage-") as scratch:
            data = Path(scratch) / "coverage"
            outcomes = _pytest(root, step, data) or {}
            wanted = {
                test
                for test, outcome in base.outcomes.items()
                if outcome == "passed" and _belongs(test, step.folder)
            }
            ran = {test for test, outcome in outcomes.items() if outcome == "passed"}
            measured = _executed(root, step, data) if data.is_file() and ran == wanted else None
            if measured is None:
                return None
            executed.update(measured)
    return executed or None
