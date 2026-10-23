"""`kiln dev` in the foreground: the processes' output interleaved; Ctrl+C stops them all.

Each line is prefixed by its process in color (`django   │ …`, `nuxt     │ …`). The processes
keep their colors (`FORCE_COLOR`) and Python does not buffer (`PYTHONUNBUFFERED`). Closing the
terminal stops them too: each leads its own process group, out of reach of the terminal's
signals, so kiln stops them itself.
"""

import contextlib
import os
import signal
import subprocess
import sys
import threading
from collections.abc import Iterator
from pathlib import Path
from types import FrameType
from typing import IO

from kiln import ui
from kiln.dev.processes import runs_beyond_front, signal_group, spawn
from kiln.stack import Command

# Color of each process's prefix, in launch order.
PREFIX_COLORS = (ui.FIRE, ui.MOSS, ui.GLOW, ui.CHEEK)
STOP_SECONDS = 10
_print_lock = threading.Lock()


def run_foreground(root: Path, commands: list[Command]) -> None:
    width = max(len(command.label) for command in commands)
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    full_stack = runs_beyond_front(commands)
    if ui.is_styled():
        env["FORCE_COLOR"] = "1"
    processes = []
    readers = []
    with _stopped_by_signals():
        try:
            for index, command in enumerate(commands):
                process = spawn(root, command, env, subprocess.PIPE, full_stack=full_stack)
                color = PREFIX_COLORS[index % len(PREFIX_COLORS)]
                prefix = service_prefix(command.label, width, color)
                reader = threading.Thread(target=relay, args=(process.stdout, prefix), daemon=True)
                reader.start()
                processes.append(process)
                readers.append(reader)
            _wait_all(commands, processes)
        except KeyboardInterrupt:
            pass
        finally:
            stop_all(processes)
            for reader in readers:
                reader.join(timeout=1)


def _wait_all(commands: list[Command], processes: list[subprocess.Popen[str]]) -> None:
    for command, process in zip(commands, processes, strict=True):
        returncode = process.wait()
        if returncode not in (0, -signal.SIGINT, -signal.SIGTERM):
            ui.note(f"{command.label} stopped (code {returncode})")


def stop_all(processes: list[subprocess.Popen[str]]) -> None:
    """SIGTERM to each process group, then SIGKILL to those still there after a while."""
    for process in processes:
        signal_group(process.pid)
    for process in processes:
        try:
            process.wait(timeout=STOP_SECONDS)
        except subprocess.TimeoutExpired:
            signal_group(process.pid, signal.SIGKILL)
            process.wait()


@contextlib.contextmanager
def _stopped_by_signals() -> Iterator[None]:
    """A closed terminal (SIGHUP) or a `kill` (SIGTERM) stops the processes like Ctrl+C."""

    def interrupt(signal_number: int, frame: FrameType | None) -> None:
        raise KeyboardInterrupt

    numbers = (signal.SIGHUP, signal.SIGTERM)
    previous = {number: signal.signal(number, interrupt) for number in numbers}
    try:
        yield
    finally:
        for number, handler in previous.items():
            signal.signal(number, handler)


def service_prefix(label: str, width: int, color: ui.Color) -> str:
    """`django   │ `: the process in color, aligned on the longest, then a bar."""
    return f"{ui.paint(f'{label:<{width}}', color, bold=True)} {ui.paint('│', ui.STONE_DARK)} "


def relay(stream: IO[str] | None, prefix: str) -> None:
    """Copies a process's output, line by line, behind its prefix."""
    for line in stream or ():
        with _print_lock:
            sys.stdout.write(f"{prefix}{line.rstrip()}\n")
            sys.stdout.flush()
