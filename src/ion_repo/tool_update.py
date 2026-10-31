"""The update of the tool, offered after a command typed in a terminal.

In Claude Code, the session start hook asks (`plugins/repo/hooks/session_start.py`); here, a
command typed by hand ends with the offer when a newer release exists on the machine's channel.
GitHub is asked at most once a day; after a "no", the same release is offered again a week
later. Never outside a terminal, inside Claude Code, for a tool installed from a checkout (its
developer), or with `ION_REPO_NO_UPDATE_CHECK=1`.

State: `~/.local/state/kiln/tool-update.json`.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from ion_repo import ui
from ion_repo.shell import environment
from ion_repo.versions import (
    install_source,
    installed_version,
    latest_release,
    release_version,
    upgrade_command,
)

STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
STATE_PATH = STATE_DIR / "kiln" / "tool-update.json"
CHECK_INTERVAL = 24 * 3600
REFUSAL_DELAY = 7 * 24 * 3600
OPT_OUT_VARIABLE = "ION_REPO_NO_UPDATE_CHECK"
# Set by Claude Code in the commands it runs: its own hook asks there.
CLAUDE_CODE_VARIABLE = "CLAUDECODE"
# `doctor` already reports a late tool; `completion` is read by the shell.
SILENT_COMMANDS = frozenset({"completion", "doctor", "frame"})

State = dict[str, Any]


def load() -> State:
    try:
        loaded = json.loads(STATE_PATH.read_text())
    except OSError, ValueError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def save(state: State) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(state, indent=2))
    except OSError:
        pass


def should_check(command: str | None) -> bool:
    return (
        command not in SILENT_COMMANDS
        and sys.stdin.isatty()
        and sys.stdout.isatty()
        and not os.environ.get(CLAUDE_CODE_VARIABLE)
        and not environment(OPT_OUT_VARIABLE)
        and install_source() != "folder"
    )


def newer_release(state: State, now: float) -> str | None:
    """The latest release if newer than the tool; GitHub asked at most once a day."""
    if now - float(state.get("checked", 0)) >= CHECK_INTERVAL:
        state["checked"] = now
        state["latest"] = latest_release()
    latest = state.get("latest")
    if not isinstance(latest, str):
        return None
    current, available = release_version(installed_version().split()[0]), release_version(latest)
    if current is None or available is None or available <= current:
        return None
    return latest


def is_due(state: State, tag: str, now: float) -> bool:
    return state.get("refused") != tag or now - float(state.get("refused_at", 0)) >= REFUSAL_DELAY


def offer(command: str | None, *, now: float | None = None) -> None:
    """After a command: offers the newer release, installs it on a yes."""
    if not should_check(command):
        return
    now = time.time() if now is None else now
    state = load()
    tag = newer_release(state, now)
    if tag is None or not is_due(state, tag, now):
        save(state)
        return
    upgrade = upgrade_command(tag)
    print()
    ui.note(f"ion-repo {tag} is available (this machine has {installed_version()}).")
    try:
        answer = input(f"Update now ({upgrade})? [Y/n] ").strip().lower()
    except EOFError, KeyboardInterrupt:
        answer = "n"
        print()
    if answer in ("", "y", "yes", "o", "oui"):
        state.pop("refused", None)
        save(state)
        if subprocess.run(upgrade, shell=True, check=False).returncode == 0:
            ui.success(
                f"ion-repo {tag} installed. In each repo: ion repo update (skill /repo:update)."
            )
        return
    state.update(refused=tag, refused_at=now)
    save(state)
    ui.note(f"Offered again in a week. Never: export {OPT_OUT_VARIABLE}=1.")
