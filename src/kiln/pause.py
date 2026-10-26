"""`kiln pause`: a Claude Code session named and its place kept, listed at the next start (T-344).

Claude Code already names a session (`/rename`) and resumes it (`claude --resume`); what it lacks
is the list, at the next start in any repo, of the sessions left halfway with where each stopped
and its next step. One file per session in `~/.local/state/kiln/sessions/<id>.json`, which the
plugin's `session_start.py` reads; it drops a session once resumed or its branch deleted.
"""

import datetime
import json
import os
import subprocess
from pathlib import Path

from kiln import ui
from kiln.shell import KilnError

STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
SESSIONS_DIR = STATE_DIR / "kiln" / "sessions"
# What Claude Code gives the commands a session runs: the id `claude --resume` takes.
SESSION_VARIABLE = "CLAUDE_CODE_SESSION_ID"


def pause(cwd: Path, name: str, next_step: str) -> Path:
    session = os.environ.get(SESSION_VARIABLE, "")
    if not session or "/" in session:
        raise KilnError("no Claude Code session here: /kiln:pause runs from inside one")
    root = Path(_git(cwd, "rev-parse", "--show-toplevel") or cwd)
    # The project's name, not a worktree's folder: the parent of the shared git folder.
    common = _git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
    record = {
        "id": session,
        "name": name,
        "project": Path(common).parent.name if common else root.name,
        "repo": str(root),
        "branch": _git(cwd, "branch", "--show-current"),
        "next": next_step,
        "paused": datetime.datetime.now().astimezone().isoformat(timespec="minutes"),
    }
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = SESSIONS_DIR / f"{session}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.success(f"Paused: {name}")
    ui.note(f"Listed at the next session start; resume with: claude --resume {session}")
    return path


def _git(cwd: Path, *arguments: str) -> str:
    done = subprocess.run(["git", *arguments], cwd=cwd, capture_output=True, text=True, check=False)
    return done.stdout.strip() if done.returncode == 0 else ""
