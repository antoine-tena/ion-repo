#!/usr/bin/env python3
"""PreToolUse (Bash): refuses a `git commit` on a main branch (main, master, develop), and a
commit message signed by Claude (`Co-Authored-By: Claude`, `Claude-Session:`): once pushed to
the integration branch, it cannot be erased.

Only exception: the commit that concludes a merge in progress (MERGE_HEAD present), for example
after resolving a conflict of `git merge --no-ff`.

A repo where commits go straight to the main branch opts out with
`git config kiln.branch-guard false` (`garde-branche.desactive true` before kiln 0.4).
"""

import contextlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROTECTED_BRANCHES = {"main", "master", "develop"}


def git_config(directory: str, key: str) -> str:
    return subprocess.run(
        ["git", "-C", directory, "config", "--get", key],
        capture_output=True,
        text=True,
        timeout=5,
    ).stdout.strip()


data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")
cwd = data.get("cwd") or "."

# Each subcommand (separated by ; && || | or a newline) is read in order: a `cd` changes the
# current directory, a `git [-C dir] commit` at the head of a subcommand is checked in its
# directory. The text "git commit" in an echo or a message does not count.
targets = []
for part in re.split(r"&&|\|\||[;|\n]", cmd):
    part = part.strip().lstrip("(").strip()
    m = re.match(r"cd\s+(\S+)", part)
    if m:
        cwd = os.path.join(cwd, os.path.expanduser(m.group(1).strip("'\"")))
        continue
    m = re.match(r"git((?:\s+-[cC]\s+\S+)*)\s+commit\b", part)
    if m:
        c = re.findall(r"-C\s+(\S+)", m.group(1))
        targets.append(os.path.join(cwd, *(p.strip("'\"") for p in c)) if c else cwd)

# The message is in the command (-m, heredoc) or in a file (-F, --file).
SIGNATURE = re.compile(r"co-authored-by:\s*claude|claude-session:", re.I)
if targets:
    message = cmd
    for path in re.findall(r"(?:-F\s*|--file[=\s])(\S+)", cmd):
        with contextlib.suppress(OSError):
            message += Path(cwd, path.strip("'\"")).read_text()
    if SIGNATURE.search(message):
        print(
            "Commit refused: no Co-Authored-By: Claude or Claude-Session: "
            "in a commit message. Remove them.",
            file=sys.stderr,
        )
        sys.exit(2)

for target in targets:
    try:
        branch = subprocess.run(
            ["git", "-C", target, "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except Exception:
        continue
    is_disabled = git_config(target, "kiln.branch-guard") == "false" or (
        git_config(target, "garde-branche.desactive") == "true"
    )
    is_merging = (
        subprocess.run(
            ["git", "-C", target, "rev-parse", "-q", "--verify", "MERGE_HEAD"],
            capture_output=True,
            timeout=5,
        ).returncode
        == 0
    )
    if branch in PROTECTED_BRANCHES and not is_disabled and not is_merging:
        print(
            f"Commit refused: never commit on {branch}. Create a branch (worktree) first.",
            file=sys.stderr,
        )
        sys.exit(2)
