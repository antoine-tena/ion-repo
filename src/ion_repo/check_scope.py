"""Which tests `ion repo check --tests` runs on a branch: those of the Python packages its changes
touch, not the whole suite.

A changed file puts its top-level package's tests in the scope (`treasury/cashflow.py` -> the
tests under `treasury/`), and so do the other packages whose test files import a changed module
directly (`from treasury import cashflow`). A changed test file runs by itself. What can reach
anything (the lockfile, `pytest.ini`, a root `conftest.py`, the settings, a shared `core/`
package, a Python file at the root of the project) runs the whole suite, as does `--all`.
Imports are read from the test files, not followed: a test that reaches a module only through
another one is not found, which `ion repo check --all --tests` (the release) covers.
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

SOURCE_DIR = "src"
SHARED_PACKAGES = frozenset({"core", "common", "shared"})
SUITE_CONFIG_FILES = frozenset(
    {"conftest.py", "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini", "uv.lock"}
)
SETTINGS_PART = "settings"
IGNORED_FOLDERS = frozenset({".venv", "node_modules"})
TEST_FILE_PREFIX = "test_"
TEST_FILE_SUFFIX = "_test.py"
PYTHON_SUFFIX = ".py"
INIT_MODULE = "__init__"
MIN_ANCESTOR_PARTS = 2


@dataclass
class RunScope:
    """The test paths to run, relative to the Python project's folder; `is_whole` when all."""

    is_whole: bool = False
    paths: list[str] = field(default_factory=list)
    reason: str = ""

    @property
    def is_empty(self) -> bool:
        return not self.is_whole and not self.paths

    def describe(self) -> str:
        if self.is_whole:
            return f"the whole suite ({self.reason})"
        if self.is_empty:
            return f"no test to run ({self.reason})"
        return f"{', '.join(self.paths)} ({self.reason})"


def scope_of(project: Path, changed: list[str] | None, directory: str) -> RunScope:
    """The tests to run in `project` (the Python folder `directory` of the repo) for the changed
    files of the repo; None, the whole suite."""
    if changed is None:
        return RunScope(is_whole=True, reason="all files checked")
    prefix = "" if directory == "." else f"{directory}/"
    relative = [path.removeprefix(prefix) for path in changed if path.startswith(prefix)]
    if (broad := next((path for path in relative if _is_broad(path)), None)) is not None:
        return RunScope(is_whole=True, reason=f"{broad} reaches every test")
    scope = RunScope()
    modules: list[str] = []
    for path in relative:
        if _is_test_file(path):
            _add(scope.paths, path)
        elif package := _package_of(path):
            if _has_tests(project / package):
                _add(scope.paths, package)
            if path.endswith(PYTHON_SUFFIX):
                modules.append(_module_of(project, path))
    importers = _importing_packages(project, modules, scope.paths)
    for package, module in importers.items():
        _add(scope.paths, package)
        scope.reason += f"{package} imports {module}; "
    scope.paths = _without_nested(scope.paths)
    changed_packages = sorted({_package_of(path) or path for path in relative})
    scope.reason = (scope.reason + f"changed: {', '.join(changed_packages)}").strip()
    return scope


def _is_broad(path: str) -> bool:
    """A changed file whose reach cannot be told: configuration, settings, shared code, a Python
    file of the project's root."""
    parts = PurePosixPath(path).parts
    name = parts[-1]
    if len(parts) == 1:
        return name in SUITE_CONFIG_FILES or name.endswith(PYTHON_SUFFIX)
    if parts[0] in SHARED_PACKAGES and name.endswith(PYTHON_SUFFIX):
        return True
    return name.endswith(PYTHON_SUFFIX) and (
        SETTINGS_PART in parts[:-1] or name.removesuffix(PYTHON_SUFFIX) == SETTINGS_PART
    )


def _is_test_file(path: str) -> bool:
    name = PurePosixPath(path).name
    is_prefixed = name.startswith(TEST_FILE_PREFIX) and name.endswith(PYTHON_SUFFIX)
    return is_prefixed or name.endswith(TEST_FILE_SUFFIX)


def _package_of(path: str) -> str | None:
    """The top-level folder of a changed file, under `src/` when the project has that layout."""
    parts = PurePosixPath(path).parts
    if len(parts) < MIN_ANCESTOR_PARTS:
        return None
    if parts[0] == SOURCE_DIR and len(parts) > MIN_ANCESTOR_PARTS:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def _module_of(project: Path, path: str) -> str:
    parts = list(PurePosixPath(path).with_suffix("").parts)
    if parts[0] == SOURCE_DIR and (project / SOURCE_DIR).is_dir():
        parts = parts[1:]
    if parts[-1] == INIT_MODULE:
        parts = parts[:-1]
    return ".".join(parts)


def _has_tests(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    return any(
        _is_test_file(str(file.relative_to(folder)))
        for file in folder.rglob(f"*{PYTHON_SUFFIX}")
        if not any(part.startswith(".") for part in file.relative_to(folder).parts)
    )


def _importing_packages(project: Path, modules: list[str], already: list[str]) -> dict[str, str]:
    """The packages, not yet in the scope, whose test files import one of the changed modules."""
    if not modules or not project.is_dir():
        return {}
    found: dict[str, str] = {}
    for folder in sorted(path for path in project.iterdir() if path.is_dir()):
        package = folder.name
        if package.startswith(".") or package in IGNORED_FOLDERS or package in already:
            continue
        for test_file in _test_files(folder):
            if module := _first_imported(test_file, modules):
                found[package] = module
                break
    return found


def _test_files(folder: Path) -> list[Path]:
    return [
        file
        for file in sorted(folder.rglob(f"*{PYTHON_SUFFIX}"))
        if _is_test_file(file.name) and not IGNORED_FOLDERS.intersection(file.parts)
    ]


def _first_imported(test_file: Path, modules: list[str]) -> str | None:
    try:
        tree = ast.parse(test_file.read_text(encoding="utf-8"))
    except SyntaxError, UnicodeDecodeError, OSError:
        return None
    imported = _imported_names(tree)
    for module in modules:
        if any(_reaches(name, module) for name in imported):
            return module
    return None


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def _reaches(imported: str, changed_module: str) -> bool:
    """An import of the changed module, of its submodule, or of a package above it that is not
    the top-level one (`treasury.models` reaches `treasury.models.invoice`)."""
    if imported == changed_module or imported.startswith(f"{changed_module}."):
        return True
    return (
        changed_module.startswith(f"{imported}.") and imported.count(".") + 1 >= MIN_ANCESTOR_PARTS
    )


def _add(paths: list[str], path: str) -> None:
    if path not in paths:
        paths.append(path)


def _without_nested(paths: list[str]) -> list[str]:
    """A path inside another one of the list is already run by it."""
    return [
        path
        for path in paths
        if not any(other != path and path.startswith(f"{other}/") for other in paths)
    ]
