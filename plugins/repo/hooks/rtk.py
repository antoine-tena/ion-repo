#!/usr/bin/env python3
"""PreToolUse (Bash): routes the command through rtk, which condenses its output (tests, lint,
git, builds) before it enters the context.

Without rtk in the PATH, the hook does nothing. The rewrite comes from `rtk hook claude`, minus
its permission decision (`allow`): the rewritten command goes through the usual permissions,
like the original. A repo opts out with `git config kiln.rtk false` (`rtk.desactive true`
before kiln 0.4).

In a worktree of `.claude/worktrees/`, git commands stay as typed: Claude Code's worktree
isolation refuses any git it cannot read as targeting the worktree, and `rtk git …` is one.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

raw = sys.stdin.read()
cwd = json.loads(raw).get("cwd") or "."

if not shutil.which("rtk"):
    sys.exit(0)


def git_flag(key: str) -> str:
    return subprocess.run(
        ["git", "-C", cwd, "config", "--get", "--type=bool", key],
        capture_output=True,
        text=True,
    ).stdout.strip()


if git_flag("kiln.rtk") == "false" or git_flag("rtk.desactive") == "true":
    sys.exit(0)

rewrite = subprocess.run(["rtk", "hook", "claude"], input=raw, capture_output=True, text=True)
try:
    output = json.loads(rewrite.stdout)
except json.JSONDecodeError:
    sys.exit(0)
specific = output.get("hookSpecificOutput") or {}
if "updatedInput" not in specific:
    sys.exit(0)
RTK_GIT = re.compile(r"\brtk\s+git\b")
in_claude_worktree = "/.claude/worktrees/" in Path(cwd).resolve().as_posix() + "/"
if in_claude_worktree and RTK_GIT.search(str(specific["updatedInput"].get("command", ""))):
    sys.exit(0)
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "updatedInput": specific["updatedInput"],
            }
        }
    )
)
