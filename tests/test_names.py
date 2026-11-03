import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest

HOOKS = Path(__file__).resolve().parent.parent / "plugins/repo/hooks"


@pytest.fixture
def names(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    monkeypatch.syspath_prepend(str(HOOKS))
    for name in ("names", "reminders"):
        sys.modules.pop(name, None)
    module = importlib.import_module("names")
    monkeypatch.setattr(module.reminders, "STATE_PATH", tmp_path / "reminders.json")
    monkeypatch.setattr(module.reminders, "LEGACY_STATE_PATH", tmp_path / "rappels.json")
    return module


def test_the_first_session_asks_for_the_names(names: ModuleType) -> None:
    question = names.context()

    assert "/repo:names" in question
    assert "reminders.py" in question and " no names" in question


def test_a_no_keeps_the_next_49_sessions_quiet(names: ModuleType) -> None:
    names.context()
    state = names.reminders.load()
    names.reminders.record(state, "names", "no")
    names.reminders.save(state)

    assert [names.context() for _ in range(49)] == [""] * 49
    assert names.context() != ""


def test_never_closes_the_question(names: ModuleType) -> None:
    state = names.reminders.load()
    names.reminders.record(state, "names", "never")
    names.reminders.save(state)

    assert [names.context() for _ in range(2000)] == [""] * 2000
