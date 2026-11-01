import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

MODULE_PATH = Path(__file__).resolve().parent.parent / "plugins/repo/hooks/reminders.py"


@pytest.fixture
def reminders(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    spec = importlib.util.spec_from_file_location("reminders", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "STATE_PATH", tmp_path / "reminders.json")
    monkeypatch.setattr(module, "LEGACY_STATE_PATH", tmp_path / "rappels.json")
    return module


def test_refusals_push_the_question_back(reminders: ModuleType) -> None:
    state: dict[str, Any] = {}
    asked_at = []
    for session in range(1, 110):
        reminders.count_session(state, "tool")
        if reminders.is_due(state, "tool"):
            asked_at.append(session)
            reminders.record(state, "tool", "no")

    assert asked_at == [1, 6, 16, 46, 96]


def test_agreeing_resets_the_reminders(reminders: ModuleType) -> None:
    state: dict[str, Any] = {}
    reminders.record(state, "tool", "no")
    reminders.record(state, "tool", "yes")

    assert state["questions"]["tool"] == {"sessions": 0, "refusals": 0, "next": 0}


def test_never_closes_the_question(reminders: ModuleType) -> None:
    state: dict[str, Any] = {}
    reminders.record(state, "/a", "never")
    for _ in range(1000):
        reminders.count_session(state, "/a")

    assert not reminders.is_due(state, "/a")


def test_the_state_of_kiln_0_3_keeps_its_update_reminders(reminders: ModuleType) -> None:
    legacy = {
        "bienveillance": 0.4,
        "sessions": 30,
        "dernieres": {"adoption": 12},
        "questions": {
            "maj:outil": {"sessions": 12, "refus": 2, "prochaine": 20},
            "maj:/home/n/repo": {"sessions": 3, "refus": 4, "prochaine": 0, "jamais": True},
            "adoption:/home/n/other": {"sessions": 5, "refus": 1, "prochaine": 40},
        },
    }
    (reminders.LEGACY_STATE_PATH).write_text(json.dumps(legacy))

    assert reminders.load() == {
        "questions": {
            "tool": {"sessions": 12, "refusals": 2, "next": 20},
            "/home/n/repo": {"sessions": 3, "refusals": 4, "next": 0, "never": True},
        }
    }


def test_the_oldest_state_keeps_its_reminders(reminders: ModuleType) -> None:
    state = reminders.migrate({"outil": {"sessions": 12, "refus": 2, "prochaine": 20}})

    assert state["questions"]["tool"] == {"sessions": 12, "refusals": 2, "next": 20}


def test_answers_are_recorded_from_the_command_line(reminders: ModuleType) -> None:
    reminders.main(["no", "/home/n/repo"])
    # The form of kiln 0.3, still given by skills cached before the update.
    reminders.main(["non", "maj", "outil"])

    questions = reminders.load()["questions"]
    assert questions["/home/n/repo"]["refusals"] == 1
    assert questions["tool"]["refusals"] == 1
    with pytest.raises(SystemExit):
        reminders.main(["maybe", "tool"])
