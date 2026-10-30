#!/usr/bin/env python3
"""UserPromptSubmit: at the first prompt of a session where kiln offers an update, shows the logo
of kiln in color with the update on offer, right before Claude asks the question.

`session_start.py` leaves the notice in `~/.local/state/kiln/notices/<session id>`; it is shown
once, then removed. Silent in every other case.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reminders

NOTICES_DIR = reminders.STATE_DIR / "kiln" / "notices"


def main() -> None:
    try:
        session_id = json.load(sys.stdin).get("session_id", "")
        if not session_id or "/" in session_id:
            return
        path = NOTICES_DIR / session_id
        text = path.read_text(encoding="utf-8")
        path.unlink()
    except Exception:
        return
    print(json.dumps({"systemMessage": text}, ensure_ascii=False))


if __name__ == "__main__":
    main()
