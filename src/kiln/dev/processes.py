"""What `kiln dev` runs on the machine: the stack's servers and each folder's `Procfile.dev`.

A `Procfile.dev` (the format of foreman and of Rails' `bin/dev`) lists one process per line,
`name: command`, run in its folder (`backend/`, `frontend/` or the root) through `sh -c`: a Celery
worker, a scheduler, a CSS watcher. A name taken by the stack (`django`) replaces its server.

Each process gets the `.env` of its folder, the shell's environment winning over it, and leads
its own process group: stopping it stops the children a `sh -c` or `uv run` started.
"""

import contextlib
import os
import re
import signal
import subprocess
from pathlib import Path
from typing import IO

from kiln.stack import BACKEND_DIR, FRONTEND_DIR, Command, load_stack

ENV_FILE = ".env"
PROCFILE = "Procfile.dev"
PROCFILE_DIRS = (BACKEND_DIR, FRONTEND_DIR, ".")
_PROCFILE_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(\S.*)$")


def dev_processes(root: Path) -> list[Command]:
    """The stack's servers, then the processes of the `Procfile.dev`s; a same name replaces."""
    by_label = {command.label: command for command in load_stack(root).dev_commands()}
    for directory in PROCFILE_DIRS:
        for command in procfile_commands(root, directory):
            by_label[command.label] = command
    return list(by_label.values())


def procfile_commands(root: Path, directory: str) -> list[Command]:
    path = root / directory / PROCFILE
    if not path.is_file():
        return []
    commands = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line_match := _PROCFILE_LINE.match(line.strip()):
            label, shell_command = line_match.groups()
            commands.append(Command(label, directory, ("sh", "-c", shell_command)))
    return commands


def read_env_file(path: Path) -> dict[str, str]:
    """`KEY=value` lines of a `.env`: comments, blanks and `export` ignored, quotes removed."""
    if not path.is_file():
        return {}
    variables = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip().removeprefix("export ").strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        variables[key.strip()] = value
    return variables


def spawn(
    root: Path, command: Command, env: dict[str, str], output: IO[str] | int
) -> subprocess.Popen[str]:
    directory = root / command.directory
    return subprocess.Popen(
        list(command.argv),
        cwd=directory,
        env={**read_env_file(directory / ENV_FILE), **env},
        stdin=subprocess.DEVNULL,
        stdout=output,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        start_new_session=True,
    )


def signal_group(pid: int, signal_number: int = signal.SIGTERM) -> None:
    """Sends a signal to the process group a process leads; nothing if it is gone."""
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(pid, signal_number)
