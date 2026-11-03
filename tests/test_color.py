import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest

HOOKS = Path(__file__).resolve().parent.parent / "plugins/repo/hooks"


@pytest.fixture
def color(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    monkeypatch.syspath_prepend(str(HOOKS))
    for name in ("color", "reminders"):
        sys.modules.pop(name, None)
    module = importlib.import_module("color")
    monkeypatch.setattr(module.reminders, "STATE_PATH", tmp_path / "reminders.json")
    monkeypatch.setattr(module.reminders, "LEGACY_STATE_PATH", tmp_path / "rappels.json")
    return module


def test_the_first_session_asks_for_a_color(color: ModuleType) -> None:
    question = color.context()

    assert "/repo:color" in question
    assert "reminders.py" in question and " no color" in question


def test_a_no_keeps_the_next_49_sessions_quiet(color: ModuleType) -> None:
    color.context()
    state = color.reminders.load()
    color.reminders.record(state, "color", "no")
    color.reminders.save(state)

    assert [color.context() for _ in range(49)] == [""] * 49
    assert color.context() != ""


def test_never_closes_the_question(color: ModuleType) -> None:
    state = color.reminders.load()
    color.reminders.record(state, "color", "never")
    color.reminders.save(state)

    assert [color.context() for _ in range(2000)] == [""] * 2000
