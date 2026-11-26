"""What `ion repo check` looks at: the branch's changes, the whole repo on a release branch."""

import subprocess
from pathlib import Path

import pytest

from ion_repo import check, check_scope


def _repo(root: Path, branch: str) -> Path:
    subprocess.run(["git", "init", "-q", "-b", branch, str(root)], check=True)
    return root


@pytest.mark.parametrize("branch", ["release/v1.2.3", "hotfix/v1.2.4"])
def test_a_release_branch_checks_the_whole_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, branch: str
) -> None:
    scopes: list[list[str] | None] = []

    def record(_root: Path, _with_tests: bool, changed: list[str] | None) -> list[str]:
        scopes.append(changed)
        return []

    monkeypatch.setattr(check, "changed_files", lambda _root: [])
    monkeypatch.setattr(check, "run_checks", record)
    check.check_project(_repo(tmp_path, branch))
    assert scopes == [None]


def test_a_branch_without_changes_does_not_claim_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check, "changed_files", lambda _root: [])
    check.check_project(_repo(tmp_path, "feat/nothing"))
    printed = capsys.readouterr()
    output = printed.out + printed.err
    assert "nothing was checked" in output
    assert "--all --tests" in output
    assert "✓" not in output


def _backend(root: Path) -> Path:
    """A Django-like backend: apps with their tests, one app whose test imports another's module."""
    files = {
        "conftest.py": "",
        "core/settings.py": "",
        "core/money.py": "",
        "treasury/cashflow.py": "",
        "treasury/models/__init__.py": "",
        "treasury/models/ledger.py": "",
        "treasury/tests/test_cashflow.py": "from treasury import cashflow\n",
        "accounts/service.py": "",
        "accounts/tests/test_gdpr.py": "from treasury.models.ledger import Ledger\n",
        "stations/tests/test_map.py": "import stations\n",
        "events/tests/test_trips.py": "from treasury.cashflow import forecast\n",
        "media/photo.jpg": "",
    }
    for name, text in files.items():
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
    return root


def test_a_change_runs_its_apps_tests_and_those_importing_its_module(tmp_path: Path) -> None:
    project = _backend(tmp_path)
    scope = check_scope.scope_of(project, ["backend/treasury/cashflow.py"], "backend")
    assert not scope.is_whole
    assert scope.paths == ["treasury", "events"]
    assert "events imports treasury.cashflow" in scope.reason


def test_a_package_a_test_imports_by_its_models_is_in_the_scope(tmp_path: Path) -> None:
    project = _backend(tmp_path)
    scope = check_scope.scope_of(project, ["backend/treasury/models/ledger.py"], "backend")
    assert scope.paths == ["treasury", "accounts"]


def test_an_app_nobody_imports_runs_alone(tmp_path: Path) -> None:
    project = _backend(tmp_path)
    scope = check_scope.scope_of(project, ["backend/stations/tests/test_map.py"], "backend")
    assert scope.paths == ["stations/tests/test_map.py"]


@pytest.mark.parametrize(
    "path",
    [
        "backend/conftest.py",
        "backend/uv.lock",
        "backend/pytest.ini",
        "backend/manage.py",
        "backend/core/money.py",
        "backend/core/settings.py",
        "backend/config/settings/base.py",
    ],
)
def test_what_reaches_every_test_runs_the_whole_suite(tmp_path: Path, path: str) -> None:
    scope = check_scope.scope_of(_backend(tmp_path), [path], "backend")
    assert scope.is_whole
    assert "reaches every test" in scope.reason


def test_nothing_reached_runs_no_test(tmp_path: Path) -> None:
    changed = ["backend/media/photo.jpg", "backend/README.md", "frontend/app/app.vue"]
    scope = check_scope.scope_of(_backend(tmp_path), changed, "backend")
    assert scope.is_empty
    assert "no test to run" in scope.describe()


def test_all_checks_the_whole_suite(tmp_path: Path) -> None:
    scope = check_scope.scope_of(_backend(tmp_path), None, "backend")
    assert scope.is_whole


def test_a_src_layout_maps_a_module_to_the_tests_importing_it(tmp_path: Path) -> None:
    for name, text in {
        "src/tool/check.py": "",
        "tests/test_check.py": "from tool import check\n",
        "tests/test_docs.py": "import pathlib\n",
    }.items():
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text(text)
    scope = check_scope.scope_of(tmp_path, ["src/tool/check.py"], ".")
    assert scope.paths == ["tests"]
    assert "tests imports tool.check" in scope.reason


def _stack_commands(root: Path, changed: list[str]) -> list[check.Command]:
    stack = check.Stack(backend="django", frontend="none", has_podman=True)
    return check._check_commands(root, stack, with_tests=True, changed=changed)


def test_the_check_runs_pytest_on_the_scope_only(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _backend(tmp_path / "backend")
    commands = _stack_commands(tmp_path, ["backend/treasury/cashflow.py"])
    pytest_command = next(command for command in commands if command.label == "backend pytest")
    assert pytest_command.argv == ("uv", "run", "pytest", "-q", "treasury", "events")
    printed = capsys.readouterr()
    assert "backend pytest: treasury, events" in printed.out + printed.err


def test_the_check_skips_pytest_when_no_test_is_reached(tmp_path: Path) -> None:
    _backend(tmp_path / "backend")
    commands = _stack_commands(tmp_path, ["backend/media/photo.jpg"])
    assert "backend pytest" not in [command.label for command in commands]


def test_the_shared_compose_databases_are_left_alone_when_the_ci_job_gives_its_own(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check, "load_stack", lambda _root: check.Stack("django", "none", True))
    monkeypatch.setattr(check, "_ci_django_job", lambda _root, _directory: None)
    assert check._needs_compose_databases(tmp_path)
    monkeypatch.setattr(check, "_ci_django_job", lambda _root, _directory: object())
    assert not check._needs_compose_databases(tmp_path)
