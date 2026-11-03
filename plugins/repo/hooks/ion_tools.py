#!/usr/bin/env python3
"""At a session's start: Claude offers `ion upgrade` when Ion tools installed on the machine are
behind their source, on any machine where the `repo` plugin is on and `ion` is on the PATH, in
any folder.

`ion outdated --json` says which: a tool from PyPI behind its latest release, a tool from a
repo's `develop` behind that branch (most tools, before their first release), ion itself
included; a tool installed from a folder (`--editable`) is never late. ion-repo is left out: it
has its own question (`session_start.py`). The same cadence as an ion-repo update
(`reminders.py`: again after 5, 10, 30 then 50 sessions after each "no", "never" after four).
Never blocking: `ion outdated` asks every source at once, and is given a few seconds at most.
Called by `session_start.py`; silent when not due, without `ion`, or when nothing is late.
"""

import json
import shutil
import subprocess
from collections.abc import Callable
from typing import Any

import reminders

KEY = reminders.ION_TOOLS_KEY
ION = "ion"
OWN_PACKAGE = "ion-repo"
TIMEOUT_SECONDS = 10
YES, NO, NEVER = "Update", "Not now", "Never ask again"

Late = list[dict[str, Any]]


def outdated() -> Late:
    """The Ion tools `ion outdated` finds late, ion-repo aside; empty on any failure."""
    ion = shutil.which(ION)
    if ion is None:
        return []
    try:
        done = subprocess.run(
            [ion, "outdated", "--json"],
            check=False,
            timeout=TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
        )
        rows = json.loads(done.stdout) if done.returncode == 0 else []
    except OSError, subprocess.TimeoutExpired, ValueError:
        return []
    if not isinstance(rows, list):
        return []
    return [
        row
        for row in rows
        if isinstance(row, dict) and row.get("package") != OWN_PACKAGE and row.get("name")
    ]


def answer_command(verdict: str) -> str:
    return f"`{reminders.SCRIPT} {verdict} {KEY}`"


def described(late: Late) -> str:
    return ", ".join(
        f"{row['name']} ({row.get('installed', '?')} → {row.get('latest', '?')})" for row in late
    )


def question(late: Late, state: reminders.State) -> str:
    choices = f'"{YES}", "{NO}"'
    extra = ""
    if reminders.is_long_refusal(state, KEY):
        choices += f', "{NEVER}"'
        extra = f' If "{NEVER}": {answer_command("never")}.'
    return (
        f"Ion tools installed on this machine are behind their source: {described(late)}. After "
        "any ion-repo update question of this start and before any other question, ask the user "
        "with the AskUserQuestion tool, in their language, whether to update them now "
        f'({choices}; header "Ion", the tools named in the question). If "{YES}": run `ion '
        f"upgrade` (it can take a few minutes), then {answer_command('yes')}, then tell the "
        "user to restart Claude Code so the updated tools' skills and hooks load. If "
        f'"{NO}": {answer_command("no")}, without updating anything.{extra} Then resume their '
        "request."
    )


def context(find: Callable[[], Late] = outdated) -> str:
    """The offer when it is due and a tool is late, after counting this session; empty
    otherwise."""
    if shutil.which(ION) is None:
        return ""
    state = reminders.load()
    reminders.count_session(state, KEY)
    reminders.save(state)
    if not reminders.is_due(state, KEY):
        return ""
    late = find()
    return question(late, state) if late else ""
