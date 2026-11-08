"""An ion-repo installed from its checkout follows the checkout's dependencies (`resync.py`)."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from ion_repo import resync


def checkout(tmp_path: Path, *dependencies: str) -> Path:
    listed = ", ".join(f'"{line}"' for line in dependencies)
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "ion-repo"\ndependencies = [{listed}]\n'
    )
    return tmp_path


def test_met_dependencies_leave_nothing(tmp_path: Path) -> None:
    assert resync.unmet(checkout(tmp_path, "packaging>=1", "copier")) == []


def test_an_older_or_missing_dependency_is_named(tmp_path: Path) -> None:
    found = resync.unmet(checkout(tmp_path, "packaging>=999", "no-such-package-xyz"))

    assert found[0].startswith("packaging>=999 (") and found[1] == "no-such-package-xyz"


def test_a_dependency_for_another_platform_is_skipped(tmp_path: Path) -> None:
    assert resync.unmet(checkout(tmp_path, 'no-such-package-xyz; sys_platform == "nowhere"')) == []


def test_outside_a_uv_tool_nothing_is_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", str(tmp_path))  # no uv-receipt.toml

    assert resync.editable_checkout() is None


def test_a_late_tool_installs_again_and_starts_anew(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []

    def run(command: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    def execv(_path: str, arguments: list[str]) -> None:
        calls.append(list(arguments))

    monkeypatch.delenv(resync.DONE_VARIABLE, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setattr(resync, "editable_checkout", lambda: tmp_path)
    monkeypatch.setattr(resync, "unmet", lambda _: ["ion-score>=0.1.2 (0.1.1 installed)"])
    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(os, "execv", execv)

    resync.ensure()

    assert calls[0] == ["uv", "tool", "install", "--reinstall", "--editable", str(tmp_path)]
    assert calls[1] == sys.argv and os.environ[resync.DONE_VARIABLE] == "1"


def test_once_started_anew_it_never_loops(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(resync.DONE_VARIABLE, "1")
    monkeypatch.setattr(resync, "editable_checkout", lambda: pytest.fail("read again"))

    resync.ensure()
