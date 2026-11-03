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


def answer(look: ModuleType, verdict: str) -> None:
    state = look.reminders.load()
    look.reminders.record(state, "look", verdict)
    look.reminders.save(state)


def test_the_first_session_asks_for_the_look(look: ModuleType) -> None:
    question = look.context()

    assert "/repo:look" in question
    assert "reminders.py" in question and " no look" in question
    assert "new:" not in question


@pytest.mark.parametrize("verdict", ["yes", "no"])
def test_an_answer_keeps_it_quiet_until_something_new(
    look: ModuleType, monkeypatch: pytest.MonkeyPatch, verdict: str
) -> None:
    look.context()
    answer(look, verdict)

    assert [look.context() for _ in range(3000)] == [""] * 3000

    monkeypatch.setitem(look.reminders.NEWS, "look", 2)
    monkeypatch.setitem(look.WHATS_NEW, 2, "a fourth status line style")
    question = look.context()
    assert "new: a fourth status line style" in question
    assert "their name and Claude's above the messages, the status line in" not in question


def test_never_closes_it_even_for_something_new(
    look: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    answer(look, "never")
    monkeypatch.setitem(look.reminders.NEWS, "look", 2)

    assert look.context() == ""


def test_each_version_says_what_it_brought(look: ModuleType) -> None:
    assert set(look.WHATS_NEW) == set(range(1, look.reminders.NEWS["look"] + 1))
