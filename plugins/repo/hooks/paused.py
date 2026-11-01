"""The sessions `ion repo pause` kept (T-344): listed at the next start, in any repo, above the
first prompt; a session leaves the list once resumed, or when its repo or branch is gone (merged and
deleted).

One file per session in `~/.local/state/kiln/sessions/<id>.json`, written by `ion repo pause`.
"""

import datetime
import json
import subprocess
from pathlib import Path

import reminders

SESSIONS_DIR = reminders.STATE_DIR / "kiln" / "sessions"


def forget(session_id: str) -> None:
    """A resumed session leaves the list."""
    if session_id and "/" not in session_id:
        (SESSIONS_DIR / f"{session_id}.json").unlink(missing_ok=True)


def listing(current: str = "", now: datetime.datetime | None = None) -> str:
    """The paused sessions, one block each; empty when there is none."""
    now = now or datetime.datetime.now().astimezone()
    blocks = []
    for path in sorted(SESSIONS_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            paused = datetime.datetime.fromisoformat(record["paused"])
        except OSError, ValueError, KeyError, TypeError:
            path.unlink(missing_ok=True)
            continue
        if record.get("id") == current:
            continue
        if not _still_there(record):
            path.unlink(missing_ok=True)
            continue
        repo = record.get("project") or Path(record.get("repo", "")).name
        branch = record.get("branch") or ""
        where = f"{repo} · {branch}" if branch else repo
        lines = [f"  ⏸ {record.get('name', '?')}  ({where}, {_age(now - paused)} ago)"]
        if record.get("next"):
            lines.append(f"    next: {record['next']}")
        lines.append(f"    claude --resume {record.get('id', '')}")
        blocks.append((paused, "\n".join(lines)))
    if not blocks:
        return ""
    blocks.sort(key=lambda block: block[0], reverse=True)
    return "Paused sessions (/repo:pause):\n" + "\n".join(text for _, text in blocks)


def _still_there(record: dict[str, str]) -> bool:
    repo = Path(record.get("repo", ""))
    if not repo.is_dir():
        return False
    branch = record.get("branch")
    if not branch:
        return True
    found = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    return found.returncode == 0


def _age(elapsed: datetime.timedelta) -> str:
    minutes = int(elapsed.total_seconds() // 60)
    if minutes < 60:
        return f"{max(minutes, 1)} min"
    if minutes < 48 * 60:
        return f"{minutes // 60} h"
    return f"{minutes // (24 * 60)} d"
