import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "plugins/kiln/hooks/rtk.py"

# Stand-in for `rtk hook claude`: prefixes every command with `rtk`, like the real one does
# for git, tests or builds.
FAKE_RTK = """#!/bin/sh
python3 -c '
import json, sys
command = json.load(sys.stdin)["tool_input"]["command"]
print(json.dumps({"hookSpecificOutput": {"updatedInput": {"command": "rtk " + command}}}))
'
"""


@pytest.fixture
def fake_path(tmp_path: Path) -> str:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    rtk = bin_dir / "rtk"
    rtk.write_text(FAKE_RTK)
    rtk.chmod(0o755)
    return f"{bin_dir}{os.pathsep}{os.environ['PATH']}"


def rewritten(command: str, cwd: Path, path: str) -> str | None:
    cwd.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"tool_input": {"command": command}, "cwd": str(cwd)})
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        env={**os.environ, "PATH": path},
        check=True,
    )
    if not result.stdout.strip():
        return None
    output = json.loads(result.stdout)["hookSpecificOutput"]
    assert "permissionDecision" not in output
    return str(output["updatedInput"]["command"])


def test_git_is_routed_through_rtk_in_the_main_tree(tmp_path: Path, fake_path: str) -> None:
    assert rewritten("git status", tmp_path / "repo", fake_path) == "rtk git status"


def test_git_stays_as_typed_in_a_claude_worktree(tmp_path: Path, fake_path: str) -> None:
    worktree = tmp_path / "repo/.claude/worktrees/feat-x/backend"
    assert rewritten("git status --short", worktree, fake_path) is None


def test_other_commands_still_go_through_rtk_in_a_worktree(tmp_path: Path, fake_path: str) -> None:
    worktree = tmp_path / "repo/.claude/worktrees/feat-x"
    assert rewritten("uv run pytest -q", worktree, fake_path) == "rtk uv run pytest -q"
