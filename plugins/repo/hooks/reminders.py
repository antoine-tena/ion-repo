#!/usr/bin/env python3
"""Reminders: when to ask again whether to update ion-repo (the tool, or a repo).

Each question has a key (`tool`, or the root of a repo). It is asked at the first session where
it applies, then, after each "no", again after 5, 10, 30 and 50 sessions in the place where it is
asked; "never" closes it for good.

State: `~/.local/state/kiln/reminders.json` (`rappels.json` before kiln 0.4, migrated). Answers,
given by Claude after the question: `python3 reminders.py yes|no|never <key>`.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
STATE_PATH = STATE_DIR / "kiln" / "reminders.json"
LEGACY_STATE_PATH = STATE_DIR / "kiln" / "rappels.json"
SCRIPT = f'python3 "{Path(__file__).resolve()}"'

ANSWERS = ("yes", "no", "never")
# Answers of kiln 0.3, still accepted.
LEGACY_ANSWERS = {"oui": "yes", "non": "no", "jamais": "never"}
DELAYS = (5, 10, 30, 50)
TOOL_KEY = "tool"

State = dict[str, Any]
Question = dict[str, Any]


def load() -> State:
    for path in (STATE_PATH, LEGACY_STATE_PATH):
        try:
            loaded = json.loads(path.read_text())
        except OSError, ValueError:
            continue
        return migrate(loaded if isinstance(loaded, dict) else {})
    return {"questions": {}}


def migrate(state: State) -> State:
    """Brings an older state to the current format.

    kiln 0.3 kept questions by kind (`maj:<key>`, `adoption:<key>`) with French fields, and
    before that the update questions alone, at the root.
    """
    if "questions" not in state or not isinstance(state["questions"], dict):
        state = {
            "questions": {
                f"maj:{key}": entry for key, entry in state.items() if isinstance(entry, dict)
            }
        }
    questions: dict[str, Question] = {}
    for key, entry in state["questions"].items():
        if not isinstance(entry, dict):
            continue
        kind, colon, rest = key.partition(":")
        if colon and kind == "adoption":
            continue
        if colon and kind == "maj":
            key = TOOL_KEY if rest == "outil" else rest
        questions[key] = {
            "sessions": int(entry.get("sessions", 0)),
            "refusals": int(entry.get("refusals", entry.get("refus", 0))),
            "next": int(entry.get("next", entry.get("prochaine", 0))),
        }
        if entry.get("never") or entry.get("jamais"):
            questions[key]["never"] = True
    return {"questions": questions}


def save(state: State) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def question(state: State, key: str) -> Question:
    questions = state.setdefault("questions", {})
    entry: Question = questions.setdefault(key, {"sessions": 0, "refusals": 0, "next": 0})
    return entry


def count_session(state: State, key: str) -> Question:
    """One more session where the question is asked; once per session start."""
    entry = question(state, key)
    entry["sessions"] += 1
    return entry


def is_due(state: State, key: str) -> bool:
    entry = question(state, key)
    return not entry.get("never") and entry["sessions"] >= entry["next"]


def is_long_refusal(state: State, key: str) -> bool:
    return int(question(state, key)["refusals"]) >= len(DELAYS)


def record(state: State, key: str, verdict: str) -> None:
    entry = question(state, key)
    if verdict == "yes":
        entry["refusals"] = 0
        entry["next"] = 0
        return
    entry["refusals"] += 1
    if verdict == "never":
        entry["never"] = True
        return
    entry["next"] = entry["sessions"] + DELAYS[min(entry["refusals"], len(DELAYS)) - 1]


def main(arguments: list[str]) -> None:
    # kiln 0.3 passed a kind: `relances.py non maj outil`.
    if len(arguments) == 3 and arguments[1] in ("maj", "update"):
        arguments = [arguments[0], TOOL_KEY if arguments[2] == "outil" else arguments[2]]
    if len(arguments) == 2:
        arguments[0] = LEGACY_ANSWERS.get(arguments[0], arguments[0])
    if len(arguments) != 2 or arguments[0] not in ANSWERS:
        sys.exit(f"usage: reminders.py {'|'.join(ANSWERS)} <key>")
    verdict, key = arguments
    state = load()
    record(state, key, verdict)
    save(state)


if __name__ == "__main__":
    main(sys.argv[1:])
