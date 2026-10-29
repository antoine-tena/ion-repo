#!/usr/bin/env python3
"""A session started outside any repo whose first messages name a repo below it.

Claude Code loads a repo's `CLAUDE.md`, skills, settings and memory from the folder it was
started in: a session started in `~/code` that works in `~/code/shop` misses them all, and a
`cd` along the way doesn't bring them back. So the session is never moved; at its first
messages (up to `PROMPTS_WATCHED`, slash commands aside), when they name a repo found below the
launch folder, Claude is told, and says it in one line with the command that restarts there,
unless the message is only a question or a discussion.

Silent inside a repo, when no repo is named, and once a repo has been named. State per session:
`~/.local/state/kiln/places/<session id>` (prompts seen), removed after `KEPT_DAYS`.
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reminders

PLACES_DIR = reminders.STATE_DIR / "kiln" / "places"
PROMPTS_WATCHED = 3
KEPT_DAYS = 30
# The search below the launch folder: `~` reaches `~/code/<tool>/<repo>` at depth 4.
MAX_DEPTH = 4
MAX_FOLDERS = 3000
TIME_BUDGET_SECONDS = 1.5
SKIPPED_FOLDERS = {"node_modules", "venv", "__pycache__", "site-packages", "target", "dist"}
MIN_NAME_LENGTH = 3
MAX_CANDIDATES = 3
DONE = "done"


def inside_repo(cwd: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=3,
        )
    except OSError, subprocess.SubprocessError:
        return True
    return result.returncode == 0 and result.stdout.strip() == "true"


def repos_below(root: Path) -> list[Path]:
    """The git repos below `root`, shallowest first, without entering a repo or a hidden folder."""
    deadline = time.monotonic() + TIME_BUDGET_SECONDS
    found: list[Path] = []
    level = [root]
    seen = 0
    for _ in range(MAX_DEPTH):
        below: list[Path] = []
        for folder in level:
            try:
                entries = sorted(os.scandir(folder), key=lambda entry: entry.name)
            except OSError:
                continue
            for entry in entries:
                if entry.name.startswith(".") or entry.name in SKIPPED_FOLDERS:
                    continue
                try:
                    if not entry.is_dir(follow_symlinks=False):
                        continue
                except OSError:
                    continue
                seen += 1
                path = Path(entry.path)
                if (path / ".git").exists():
                    found.append(path)
                else:
                    below.append(path)
            if seen > MAX_FOLDERS or time.monotonic() > deadline:
                return found
        level = below
    return found


def named(prompt: str, name: str) -> bool:
    """`name` as a word of `prompt`: `kiln` in "kiln's hooks" or `~/code/kiln`, not `kiln-x`."""
    pattern = rf"(?<![\w.-]){re.escape(name.lower())}(?![\w-]|\.\w)"
    return re.search(pattern, prompt.lower()) is not None


def candidates(prompt: str, repos: list[Path], cwd: Path) -> list[Path]:
    """The repos the prompt names; a name already in the launch path (`Keramos` started in
    `~/code/Keramos`) means that folder, not the repo of the same name below it."""
    around = {part.lower() for part in cwd.parts}
    return [
        repo
        for repo in repos
        if len(repo.name) >= MIN_NAME_LENGTH
        and repo.name.lower() not in around
        and named(prompt, repo.name)
    ][:MAX_CANDIDATES]


def advice(cwd: str, found: list[Path]) -> str:
    places = ", ".join(f"`{repo.name}` ({repo})" for repo in found)
    command = f"cd {found[0]} && claude"
    return (
        f"kiln [WRONG-PLACE]: this session was started in {cwd}, which is not a git repo, and the "
        f"message names {places}. A repo's CLAUDE.md, skills, settings and memory load only from "
        "the folder a session is started in: a cd during the session doesn't bring them. If the "
        "task will change files in that repo or needs its rules or skills, say so in one line "
        f"before anything else, with the command that restarts there (`{command}`, or the right "
        "repo's path if another one is meant), and go on only if the user wants to stay. If the "
        "message is a question or a discussion, or names the repo in passing, say nothing of it."
    )


def forget_old_sessions() -> None:
    limit = time.time() - KEPT_DAYS * 86400
    try:
        for path in PLACES_DIR.iterdir():
            if path.stat().st_mtime < limit:
                path.unlink()
    except OSError:
        pass


def check(payload: dict[str, object]) -> str | None:
    """What to tell Claude about the session's place at this prompt, or None."""
    session_id = str(payload.get("session_id") or "")
    prompt = str(payload.get("prompt") or "")
    cwd = str(payload.get("cwd") or os.getcwd())
    if not session_id or "/" in session_id or prompt.lstrip().startswith("/"):
        return None
    marker = PLACES_DIR / session_id
    try:
        seen = marker.read_text(encoding="utf-8").strip()
    except OSError:
        seen = ""
        forget_old_sessions()
    if seen == DONE or (seen.isdigit() and int(seen) >= PROMPTS_WATCHED):
        return None
    if inside_repo(cwd):
        found: list[Path] = []
        seen = DONE
    else:
        found = candidates(prompt, repos_below(Path(cwd)), Path(cwd))
        seen = DONE if found else str(int(seen or 0) + 1)
    try:
        PLACES_DIR.mkdir(parents=True, exist_ok=True)
        marker.write_text(seen, encoding="utf-8")
    except OSError:
        pass
    return advice(cwd, found) if found else None
