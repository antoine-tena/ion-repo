"""`kiln dev`: runs the stack's development servers; Ctrl+C stops them all.

The servers' output is interleaved line by line, each line prefixed by its service in color
(`django   │ …`, `nuxt     │ …`). The servers keep their colors (`FORCE_COLOR`) and Python does
not buffer (`PYTHONUNBUFFERED`).

With `--containers` (podman project), the whole stack runs in podman (`compose.yaml`).
"""

import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import IO

from kiln import ui
from kiln.shell import KilnError, require_tools, run, step
from kiln.stack import Command, load_stack

COMPOSE_FILE = "compose.yaml"
# Color of each service's prefix, in launch order.
PREFIX_COLORS = (ui.FIRE, ui.MOSS, ui.GLOW, ui.CHEEK)
_print_lock = threading.Lock()


def run_dev_servers(root: Path, *, in_containers: bool = False) -> None:
    stack = load_stack(root)
    if in_containers:
        _run_containers(root, has_podman=stack.has_podman)
        return
    commands = stack.dev_commands()
    if not commands:
        raise KilnError("nothing to run: a command-line tool runs with uv run")
    step(" · ".join(f"{command.label} ({command.directory}/)" for command in commands))
    width = max(len(command.label) for command in commands)
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    if ui.is_styled():
        env["FORCE_COLOR"] = "1"
    processes = []
    readers = []
    for index, command in enumerate(commands):
        process = _start(root, command, env)
        prefix = service_prefix(command.label, width, PREFIX_COLORS[index % len(PREFIX_COLORS)])
        reader = threading.Thread(target=_relay, args=(process.stdout, prefix), daemon=True)
        reader.start()
        processes.append(process)
        readers.append(reader)
    try:
        for command, process in zip(commands, processes, strict=True):
            returncode = process.wait()
            if returncode not in (0, -2, -15):
                ui.note(f"{command.label} stopped (code {returncode})")
    except KeyboardInterrupt:
        pass
    finally:
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        for reader in readers:
            reader.join(timeout=1)


def _start(root: Path, command: Command, env: dict[str, str]) -> subprocess.Popen[str]:
    return subprocess.Popen(
        list(command.argv),
        cwd=root / command.directory,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )


def service_prefix(label: str, width: int, color: ui.Color) -> str:
    """`django   │ `: the service in color, aligned on the longest, then a bar."""
    return f"{ui.paint(f'{label:<{width}}', color, bold=True)} {ui.paint('│', ui.STONE_DARK)} "


def _relay(stream: IO[str] | None, prefix: str) -> None:
    """Copies a server's output, line by line, behind its prefix."""
    for line in stream or ():
        with _print_lock:
            sys.stdout.write(f"{prefix}{line.rstrip()}\n")
            sys.stdout.flush()


def _run_containers(root: Path, *, has_podman: bool) -> None:
    if not has_podman or not (root / COMPOSE_FILE).exists():
        raise KilnError("no podman in this project: kiln set podman=true, on a branch")
    require_tools("podman", "podman-compose")
    step("podman stack (podman-compose up --build)")
    try:
        run(["podman-compose", "-f", COMPOSE_FILE, "up", "--build"], root, live=True)
    except KeyboardInterrupt:
        run(["podman-compose", "-f", COMPOSE_FILE, "down"], root, live=True)
