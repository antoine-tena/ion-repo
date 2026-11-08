import importlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path
from types import ModuleType

import pytest

HOOKS = Path(__file__).resolve().parent.parent / "plugins/repo/hooks"
HOST_LATE = {
    "name": "host",
    "package": "ion-host",
    "source": "git",
    "installed": "7cdf9f4",
    "latest": "b67d486",
}
REPO_LATE = {**HOST_LATE, "name": "repo", "package": "ion-repo", "source": "pypi"}


@pytest.fixture
def tools(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """The hook module, its reminders kept aside, with a fake `ion` on the PATH."""
    monkeypatch.syspath_prepend(str(HOOKS))
    for name in ("ion_tools", "reminders"):
        sys.modules.pop(name, None)
    module = importlib.import_module("ion_tools")
    monkeypatch.setattr(module.reminders, "STATE_PATH", tmp_path / "reminders.json")
    monkeypatch.setattr(module.reminders, "LEGACY_STATE_PATH", tmp_path / "rappels.json")
    fake_ion(tmp_path, monkeypatch, json.dumps([REPO_LATE, HOST_LATE]))
    return module


def fake_ion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, printed: str, code: int = 0) -> None:
    """`ion` on the PATH, printing `printed` for `ion outdated --json`."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / "printed.json").write_text(printed)
    ion = bin_dir / "ion"
    ion.write_text(
        f'#!/bin/sh\n[ "$*" = "outdated --json" ] || exit 2\ncat "{bin_dir}/printed.json"\n'
        f"exit {code}\n"
    )
    ion.chmod(ion.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")


def answer(tools: ModuleType, verdict: str) -> None:
    state = tools.reminders.load()
    tools.reminders.record(state, tools.KEY, verdict)
    tools.reminders.save(state)


def session_start(tools: ModuleType, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """The hook that asks the question, with the same `ion_tools`."""
    spec = importlib.util.spec_from_file_location("session_start", HOOKS / "session_start.py")
    assert spec is not None and spec.loader is not None
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    monkeypatch.setattr(hook, "ion_tools", tools)
    return hook


def test_late_tools_are_offered_ion_upgrade_and_a_restart(
    tools: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = session_start(tools, monkeypatch)

    offer = hook.update_question([hook.ion_tools_step(tools.due(), tools.reminders.load())])

    assert "host (7cdf9f4 → b67d486)" in offer
    assert "`ion upgrade`" in offer
    assert "restart Claude Code" in offer
    assert "AskUserQuestion" in offer


def test_ion_repo_is_left_out_in_its_own_repos_only(
    tools: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_ion(tmp_path, monkeypatch, json.dumps([REPO_LATE]))

    assert tools.due() == []
    assert tools.due(include_own=True) == [REPO_LATE]


def test_nothing_late_or_a_failing_ion_says_nothing(
    tools: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_ion(tmp_path, monkeypatch, "[]")
    assert tools.due() == []
    fake_ion(tmp_path, monkeypatch, "not json")
    assert tools.due() == []
    fake_ion(tmp_path, monkeypatch, json.dumps([HOST_LATE]), code=1)
    assert tools.due() == []


def test_an_ion_without_the_outdated_command_is_offered_the_upgrade(
    tools: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ion = tmp_path / "bin" / "ion"
    ion.write_text("#!/bin/sh\necho \"ion: error: invalid choice: 'outdated'\" >&2\nexit 2\n")
    ion.chmod(ion.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{ion.parent}{os.pathsep}{os.environ['PATH']}")

    assert [row["package"] for row in tools.outdated()] == ["ion-sh"]


def test_without_ion_nothing_is_counted_nor_said(
    tools: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))

    assert tools.due() == []
    assert not (tmp_path / "reminders.json").exists()


def test_a_no_waits_like_an_ion_repo_update_then_never_closes_it(
    tools: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = session_start(tools, monkeypatch)
    assert tools.due()
    answer(tools, "no")
    for _ in range(4):
        assert tools.due() == []
    assert tools.due()
    for _ in range(3):
        answer(tools, "no")
    state = tools.reminders.load()
    assert tools.reminders.is_long_refusal(state, tools.KEY)
    assert "Never ask again for host" in hook.update_question(
        [hook.ion_tools_step([HOST_LATE], state)]
    )
    answer(tools, "never")
    for _ in range(60):
        assert tools.due() == []


def test_the_offer_is_made_at_startup_only(
    tools: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = session_start(tools, monkeypatch)

    [step] = hook.ion_tools_steps({"source": "startup", "cwd": str(tmp_path)})
    assert "repo (" in step.subject and "host (" in step.subject  # outside its repos, ion-repo too
    assert hook.ion_tools_steps({"source": "clear", "cwd": str(tmp_path)}) == []
