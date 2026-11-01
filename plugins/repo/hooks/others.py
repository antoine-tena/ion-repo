"""The other sessions working on this repo (ion-repo#T-384): told at a session's start, so two
sessions do
not build on each other's half-done work unknowingly.

A session counts when it is still running (Claude Code's `~/.claude/sessions/<pid>.json`) and its
transcript (`~/.claude/projects/<launch folder>/<id>.jsonl`) was written in the last minutes with a
`cwd` in the repo or its worktrees, wherever it was launched from.
"""

import json
import os
import subprocess
import time
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
RECENT_SECONDS = 10 * 60
TAIL_BYTES = 256 * 1024


def context(cwd: str, current: str, now: float | None = None) -> str:
    """The instruction for Claude, empty when the session is alone on its repo."""
    root = _main_tree(cwd)
    if root is None:
        return ""
    found = _working_on(root, current, time.time() if now is None else now)
    if not found:
        return ""
    lines = "\n".join(f"- {branch or 'no branch'}, session {name}" for branch, name in found)
    return (
        f"ion-repo [OTHER-SESSION]: another session is working on {root.name} right now:\n{lines}\n"
        "Before anything else, tell the user in one line and ask whether to go on here: "
        "the rule is one session at a time on a project."
    )


def _main_tree(cwd: str) -> Path | None:
    """The main tree of the repo, also from one of its worktrees."""
    found = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    return Path(found.stdout.strip()).parent if found.returncode == 0 else None


def _working_on(root: Path, current: str, now: float) -> list[tuple[str, str]]:
    running = _running_sessions()
    found: dict[str, tuple[float, str]] = {}
    for transcript in (CLAUDE_DIR / "projects").glob("*/*.jsonl"):
        name = transcript.stem
        if name == current or name not in running:
            continue
        try:
            written = transcript.stat().st_mtime
            if now - written > RECENT_SECONDS or written <= found.get(name, (0.0, ""))[0]:
                continue
            place = _last_place(transcript)
        except OSError:
            continue
        if place and Path(place[0]).is_relative_to(root):
            # A session that entered a worktree writes under two launch folders: the latest counts.
            found[name] = (written, place[1])
    return sorted((branch, name) for name, (_, branch) in found.items())


def _running_sessions() -> set[str]:
    running = set()
    for record in (CLAUDE_DIR / "sessions").glob("*.json"):
        try:
            session = json.loads(record.read_text(encoding="utf-8"))["sessionId"]
            os.kill(int(record.stem), 0)
        except PermissionError:
            running.add(session)
        except OSError, ValueError, KeyError, TypeError:
            continue
        else:
            running.add(session)
    return running


def _last_place(transcript: Path) -> tuple[str, str] | None:
    """The `cwd` and `gitBranch` last written; the end of the file is enough, a transcript grows
    to many megabytes."""
    with transcript.open("rb") as file:
        file.seek(max(file.seek(0, os.SEEK_END) - TAIL_BYTES, 0))
        tail = file.read().decode("utf-8", errors="replace")
    for line in reversed(tail.splitlines()):
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and entry.get("cwd"):
            return entry["cwd"], entry.get("gitBranch") or ""
    return None
