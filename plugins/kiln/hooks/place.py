#!/usr/bin/env python3
"""A session started outside any repo: Claude is told, with the repos below the launch folder,
and judges from each task whether it belongs to one of them.

A session works in any folder, and a repo's `CLAUDE.md` and `.claude/rules/` load as its files
are read; but its `.claude/settings.json` is read only at launch (the plugins it enables, with
their skills and hooks, its permissions, its env), and the memory stays the launch folder's. So
the session is never moved: Claude says when a task deserves a restart in its repo. Called by
`session_start.py`; silent inside a repo and when no repo lies below.
"""

import os
import subprocess
import time
from pathlib import Path

# The search below the launch folder: `~` reaches `~/code/<tool>/<repo>` at depth 4.
MAX_DEPTH = 4
MAX_FOLDERS = 3000
TIME_BUDGET_SECONDS = 1.5
SKIPPED_FOLDERS = {"node_modules", "venv", "__pycache__", "site-packages", "target", "dist"}
MAX_LISTED = 40


def inside_repo(cwd: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--is-inside-work-tree"],
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


def context(cwd: Path) -> str:
    """What Claude is told at the start of a session in `cwd`, or "" inside a repo."""
    if inside_repo(cwd):
        return ""
    repos = repos_below(cwd)
    if not repos:
        return ""
    listed = ", ".join(str(repo.relative_to(cwd)) for repo in repos[:MAX_LISTED])
    if len(repos) > MAX_LISTED:
        listed += f" and {len(repos) - MAX_LISTED} more"
    return (
        f"kiln [WRONG-PLACE]: this session was started in {cwd}, which is not a git repo. "
        f"Repos below it: {listed}. When a task belongs to one of them, named or not (judge from "
        "what it will touch), and is more than reading or a small edit, say so in one line before "
        "starting, with the command that restarts there (`cd <repo path> && claude`), and go on "
        "here only if the user wants to. Working from here, that repo's CLAUDE.md and "
        ".claude/rules load as its files are read, but not its .claude/settings.json, read only "
        "at launch: the plugins it enables (their skills and hooks), its permissions (the denied "
        "reads of .env files and keys) and its env; the memory stays this folder's. Say nothing "
        "of it for a question, a discussion, or work across several repos."
    )
