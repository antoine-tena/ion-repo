"""The last `kiln-cli` moving its tester to Ion; uv and the process replacement simulated."""

import os
import sys
from pathlib import Path

import pytest

from ion_repo import kiln_move


class HandedError(Exception):
    """The process would have been replaced."""


@pytest.fixture
def tool(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    prefix = tmp_path / "tools" / "kiln-cli"
    prefix.mkdir(parents=True)
    (prefix / kiln_move.RECEIPT).touch()
    monkeypatch.setattr(sys, "prefix", str(prefix))
    monkeypatch.setattr(sys, "argv", ["kiln", "frame", "repo", "merge"])
    monkeypatch.setattr(kiln_move, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(kiln_move, "ATTEMPT_FILE", tmp_path / "state" / "attempt")
    monkeypatch.setattr(kiln_move, "LOCK_FILE", tmp_path / "state" / "lock")
    monkeypatch.delenv(kiln_move.OPT_OUT_VARIABLE, raising=False)
    monkeypatch.setattr(kiln_move.shutil, "which", lambda name: None)

    def execvp(command: str, args: list[str]) -> None:
        raise HandedError(args)

    monkeypatch.setattr(os, "execvp", execvp)
    return prefix


def fake_steps(
    monkeypatch: pytest.MonkeyPatch, prefix: Path, fail_on: str | None = None
) -> list[list[str]]:
    calls: list[list[str]] = []

    def step(command: list[str]) -> bool:
        calls.append(list(command))
        if command[:3] == ["uv", "tool", "uninstall"]:
            (prefix / kiln_move.RECEIPT).unlink()
        return fail_on is None or fail_on not in command

    monkeypatch.setattr(kiln_move, "step", step)
    return calls


def test_the_tools_move_in_the_order_uv_requires(
    tool: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = fake_steps(monkeypatch, tool)

    with pytest.raises(HandedError) as handed:
        kiln_move.run()

    assert [call[3:] if call[2] == "uninstall" else call[-1] for call in calls] == [
        "ion-sh",
        "ion-repo",
        ["kiln-cli"],
        "ion-repo",
    ]
    assert "--force" in calls[1] and "--force" in calls[3]
    assert handed.value.args[0] == ["ion-repo", "frame", "repo", "merge"]


def test_ion_repo_not_available_leaves_kiln_cli_working(
    tool: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls = fake_steps(monkeypatch, tool, fail_on="ion-repo")

    kiln_move.run()

    assert not any("uninstall" in call for call in calls)
    assert kiln_move.manual() in capsys.readouterr().err


def test_a_failed_move_waits_a_day_and_says_the_command(
    tool: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_steps(monkeypatch, tool, fail_on="ion-repo")
    kiln_move.run()
    capsys.readouterr()
    calls = fake_steps(monkeypatch, tool)

    kiln_move.run()

    assert calls == []
    assert kiln_move.manual() in capsys.readouterr().err


def test_the_opt_out_only_says_the_command(tool: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(kiln_move.OPT_OUT_VARIABLE, "1")
    calls = fake_steps(monkeypatch, tool)

    kiln_move.run()

    assert calls == []


@pytest.mark.parametrize("name", ["ion-repo", "kiln-cli-uvx"])
def test_any_other_environment_stays_put(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.setattr(sys, "prefix", str(tmp_path / name))

    assert not kiln_move.in_legacy_tool()


def test_uvx_of_kiln_cli_has_no_receipt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefix = tmp_path / "kiln-cli"
    prefix.mkdir()
    monkeypatch.setattr(sys, "prefix", str(prefix))

    assert not kiln_move.in_legacy_tool()


def test_the_stdout_of_a_failed_step_stays_clean(
    tool: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert kiln_move.step([sys.executable, "-c", "print('out'); raise SystemExit(3)"]) is False
    assert capsys.readouterr().out == ""


def test_keramos_kiln_moves_too(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefix = tmp_path / "keramos-kiln"
    prefix.mkdir()
    (prefix / kiln_move.RECEIPT).touch()
    monkeypatch.setattr(sys, "prefix", str(prefix))

    assert kiln_move.in_legacy_tool()
    assert "uv tool uninstall keramos-kiln" in kiln_move.manual()
