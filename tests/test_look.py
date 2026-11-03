import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest

HOOKS = Path(__file__).resolve().parent.parent / "plugins/repo/hooks"


@pytest.fixture
def look(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    monkeypatch.syspath_prepend(str(HOOKS))
    for name in ("look", "reminders"):
        sys.modules.pop(name, None)
    module = importlib.import_module("look")
    monkeypatch.setattr(module.reminders, "STATE_PATH", tmp_path / "reminders.json")
    monkeypatch.setattr(module.reminders, "LEGACY_STATE_PATH", tmp_path / "rappels.json")
    return module


def test_the_first_session_asks_for_the_statusline(look: ModuleType) -> None:
    question = look.context()

    assert "/repo:statusline" in question
    assert "reminders.py" in question and " no statusline" in question


def test_a_no_keeps_the_next_49_sessions_quiet(look: ModuleType) -> None:
    look.context()
    state = look.reminders.load()
    look.reminders.record(state, "statusline", "no")
    look.reminders.save(state)

    assert [look.context() for _ in range(49)] == [""] * 49
    assert look.context() != ""


def test_never_closes_the_question(look: ModuleType) -> None:
    state = look.reminders.load()
    look.reminders.record(state, "statusline", "never")
    look.reminders.save(state)

    assert [look.context() for _ in range(2000)] == [""] * 2000
