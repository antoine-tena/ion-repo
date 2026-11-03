#!/usr/bin/env python3
"""At a session's start: the Ion tools installed on the machine behind their source, on any machine
where the `repo` plugin is on and `ion` is on the PATH, in any folder; `session_start.py` puts
them in its one update question, `ion upgrade` on a yes.

`ion outdated --json` says which: a tool from PyPI behind its latest release, a tool from a
repo's `develop` behind that branch (most tools, before their first release), ion itself
included; a tool installed from a folder (`--editable`) is never late. ion-repo is left out in its
own repos, where the same question updates it apart (`/repo:update tool`). The same cadence as an
ion-repo update (`reminders.py`: again after 5, 10, 30 then 50 sessions after each "no", "never"
after four).
Never blocking: `ion outdated` asks every source at once, and is given a few seconds at most.
Called by `session_start.py`; nothing when not due, without `ion`, or when nothing is late.
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

Late = list[dict[str, Any]]


def outdated(include_own: bool = False) -> Late:
    """The Ion tools `ion outdated` finds late, ion-repo aside unless `include_own`; empty on any
    failure."""
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
        if isinstance(row, dict)
        and row.get("name")
        and (include_own or row.get("package") != OWN_PACKAGE)
    ]


def described(late: Late) -> str:
    return ", ".join(
        f"{row['name']} ({row.get('installed', '?')} → {row.get('latest', '?')})" for row in late
    )


def due(include_own: bool = False, find: Callable[[], Late] | None = None) -> Late:
    """The late tools when the question is due, after counting this session; empty otherwise."""
    if shutil.which(ION) is None:
        return []
    state = reminders.load()
    reminders.count_session(state, KEY)
    reminders.save(state)
    if not reminders.is_due(state, KEY):
        return []
    return find() if find else outdated(include_own)
