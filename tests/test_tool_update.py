import subprocess
import sys
from pathlib import Path

import pytest

from ion_repo import tool_update

DAY = tool_update.CHECK_INTERVAL


@pytest.fixture
def terminal(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[str]:
    """A command typed by hand, tool v0.4.1, GitHub at v0.4.2; returns the commands run."""
    monkeypatch.setattr(tool_update, "STATE_PATH", tmp_path / "tool-update.json")
    monkeypatch.setattr(tool_update, "should_check", lambda command: True)
    monkeypatch.setattr(tool_update, "installed_version", lambda: "v0.4.1")
    monkeypatch.setattr(tool_update, "latest_release", lambda: "v0.4.2")
    monkeypatch.setattr(tool_update, "upgrade_command", lambda tag: f"install {tag}")
    ran: list[str] = []

    def fake_run(command: str, **_: object) -> subprocess.CompletedProcess[str]:
        ran.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    return ran


def answer(monkeypatch: pytest.MonkeyPatch, reply: str) -> list[str]:
    prompts: list[str] = []

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return reply

    monkeypatch.setattr("builtins.input", fake_input)
    return prompts


def test_a_yes_installs_the_newer_release(
    monkeypatch: pytest.MonkeyPatch, terminal: list[str]
) -> None:
    answer(monkeypatch, "")

    tool_update.offer("status", now=DAY)

    assert terminal == ["install v0.4.2"]


def test_a_no_waits_a_week_before_offering_the_same_release(
    monkeypatch: pytest.MonkeyPatch, terminal: list[str]
) -> None:
    prompts = answer(monkeypatch, "n")

    tool_update.offer("status", now=DAY)
    tool_update.offer("status", now=2 * DAY)
    tool_update.offer("status", now=DAY + tool_update.REFUSAL_DELAY)

    assert len(prompts) == 2
    assert terminal == []


def test_github_is_asked_once_a_day(monkeypatch: pytest.MonkeyPatch, terminal: list[str]) -> None:
    asked: list[float] = []

    def fake_release() -> str:
        asked.append(1)
        return "v0.4.1"

    monkeypatch.setattr(tool_update, "latest_release", fake_release)

    for hour in range(5):
        tool_update.offer("status", now=DAY + hour * 3600)
    tool_update.offer("status", now=2 * DAY)

    assert len(asked) == 2


def test_an_up_to_date_tool_asks_nothing(
    monkeypatch: pytest.MonkeyPatch, terminal: list[str]
) -> None:
    monkeypatch.setattr(tool_update, "latest_release", lambda: "v0.4.1")
    prompts = answer(monkeypatch, "")

    tool_update.offer("status", now=DAY)

    assert prompts == []


@pytest.mark.parametrize(
    ("command", "variable"),
    [("status", "CLAUDECODE"), ("status", "ION_REPO_NO_UPDATE_CHECK"), ("doctor", None)],
)
def test_no_offer_in_claude_code_when_opted_out_or_in_doctor(
    monkeypatch: pytest.MonkeyPatch, command: str, variable: str | None
) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(tool_update, "install_source", lambda: "pypi")
    for name in ("CLAUDECODE", "ION_REPO_NO_UPDATE_CHECK"):
        monkeypatch.delenv(name, raising=False)
    if variable:
        monkeypatch.setenv(variable, "1")

    assert not tool_update.should_check(command)
