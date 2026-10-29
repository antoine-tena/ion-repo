#!/usr/bin/env python3
"""UserPromptSubmit: at the first prompt of a session where kiln offers an update, shows the logo
of kiln in color with the update on offer, right before Claude asks the question; and, in a
session started outside any repo, tells Claude when the message names a repo below it
(`place.py`).

`session_start.py` leaves the notice in `~/.local/state/kiln/notices/<session id>`; it is shown
once, then removed. Silent in every other case.
"""

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import place
import reminders

NOTICES_DIR = reminders.STATE_DIR / "kiln" / "notices"


def notice(session_id: str) -> str | None:
    if not session_id or "/" in session_id:
        return None
    path = NOTICES_DIR / session_id
    try:
        text = path.read_text(encoding="utf-8")
        path.unlink()
    except OSError:
        return None
    return text


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    output: dict[str, Any] = {}
    text = notice(str(payload.get("session_id") or ""))
    if text:
        output["systemMessage"] = text
    try:
        context = place.check(payload)
    except Exception:
        context = None
    if context:
        output["hookSpecificOutput"] = {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    if output:
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
