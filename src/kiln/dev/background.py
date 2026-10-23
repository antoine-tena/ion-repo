"""`kiln dev`: the processes left in the background, then `status`, `logs` and `stop`.

Each process writes its output to `<label>.log` and its record (pid, port) to `<label>.json`, in
`kiln-dev/` of the git folder of the worktree: never committed, one set per worktree. `kiln dev`
returns once each server answers on its port (a process without a known port: once it has
lasted a moment), and stops everything if one of them dies on the way, showing the end of its
log.
"""

import contextlib
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from kiln import ui
from kiln.dev.foreground import PREFIX_COLORS, service_prefix, stop_all
from kiln.dev.processes import runs_beyond_front, signal_group, spawn
from kiln.shell import KilnError, capture, spinner_line
from kiln.stack import Command

STATE_DIR = "kiln-dev"
# Port each stack's server listens on, to know when it is ready and where to open it.
DEV_PORTS = {
    "django": 8000,
    "fastapi": 8000,
    "data": 2718,
    "nuxt": 3000,
    "next": 3000,
    "astro": 4321,
    "streamlit": 8501,
    "dash": 8050,
}
READY_SECONDS = 120
# A process without a known port is taken as started once it has lasted this long.
SETTLE_SECONDS = 3
POLL_SECONDS = 0.25
STOP_SECONDS = 10
TAIL_LINES = 40
# Both loopbacks: a server bound to `localhost` may listen on IPv6 only (Nuxt on macOS).
LOOPBACKS = (
    (socket.AF_INET, "127.0.0.1"),
    (socket.AF_INET6, "::1"),
)


def state_dir(root: Path) -> Path:
    return Path(capture(["git", "rev-parse", "--absolute-git-dir"], root)) / STATE_DIR


def records(root: Path) -> dict[str, dict[str, Any]]:
    return _records_in(state_dir(root))


def others_running(root: Path) -> bool:
    """Whether another worktree of the repo still runs processes, on the same databases."""
    common = Path(capture(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], root))
    folders = [common / STATE_DIR, *(common / "worktrees").glob(f"*/{STATE_DIR}")]
    own = state_dir(root).resolve()
    return any(
        is_alive(record["pid"])
        for folder in folders
        if folder.resolve() != own
        for record in _records_in(folder).values()
    )


def _records_in(folder: Path) -> dict[str, dict[str, Any]]:
    found = {}
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else ():
        with contextlib.suppress(ValueError, OSError):
            found[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return found


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return not _is_zombie(pid)


def _is_zombie(pid: int) -> bool:
    """Exited but not yet reaped by its parent (a process started by this very kiln)."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
    except OSError:
        return False
    return stat.rsplit(")", 1)[-1].split()[:1] == ["Z"]


def running(root: Path) -> list[str]:
    return [label for label, record in records(root).items() if is_alive(record["pid"])]


def start(root: Path, commands: list[Command]) -> None:
    folder = state_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    for stale in folder.glob("*.json"):
        stale.unlink()
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    full_stack = runs_beyond_front(commands)
    processes = []
    for command in commands:
        with (folder / f"{command.label}.log").open("w", encoding="utf-8") as output:
            processes.append(spawn(root, command, env, output, full_stack=full_stack))
        record = {"pid": processes[-1].pid, "port": DEV_PORTS.get(command.label)}
        (folder / f"{command.label}.json").write_text(json.dumps(record), encoding="utf-8")
    try:
        _wait_ready(root, commands, processes)
    except KilnError, KeyboardInterrupt:
        stop_all(processes)
        raise


def _wait_ready(
    root: Path, commands: list[Command], processes: list[subprocess.Popen[str]]
) -> None:
    started = time.monotonic()
    waiting = dict(zip([command.label for command in commands], processes, strict=True))
    with spinner_line(f"waiting for {', '.join(waiting)}"):
        while waiting:
            for label, process in list(waiting.items()):
                if process.poll() is not None:
                    raise KilnError(f"{label} stopped at start:\n{_tail(root, label, 15)}")
                if _is_ready(DEV_PORTS.get(label), time.monotonic() - started):
                    del waiting[label]
            if time.monotonic() - started > READY_SECONDS:
                raise KilnError(f"{', '.join(waiting)} not ready after {READY_SECONDS} s")
            time.sleep(POLL_SECONDS)


def _is_ready(port: int | None, elapsed: float) -> bool:
    if port is None:
        return elapsed >= SETTLE_SECONDS
    return _listens(port)


def _listens(port: int) -> bool:
    return any(_answers(family, host, port) for family, host in LOOPBACKS)


def _answers(family: socket.AddressFamily, host: str, port: int) -> bool:
    try:
        with socket.socket(family) as probe:
            probe.settimeout(POLL_SECONDS)
            return probe.connect_ex((host, port)) == 0
    except OSError:  # no IPv6 on this machine
        return False


def show_status(root: Path) -> None:
    found = records(root)
    if not found:
        ui.note("nothing runs in the background: kiln dev")
        return
    width = max(len(label) for label in found)
    for label, record in found.items():
        port = record.get("port")
        if not is_alive(record["pid"]):
            state = ui.paint("stopped", ui.EMBER, bold=True) + f"  kiln dev logs {label}"
        elif port and not _listens(port):
            state = ui.paint("starting", ui.GLOW, bold=True)
        else:
            url = f"  http://localhost:{port}" if port else ""
            state = ui.paint("running", ui.MOSS, bold=True) + url
        print(f"{label:<{width}}  {state}")


def show_logs(root: Path, service: str | None, *, follow: bool) -> None:
    labels = list(records(root))
    if service is not None and service not in labels:
        raise KilnError(f"no {service} in the background (known: {', '.join(labels) or 'none'})")
    shown = [service] if service else labels
    width = max((len(label) for label in shown), default=0)
    prefixes = {
        label: service_prefix(label, width, PREFIX_COLORS[index % len(PREFIX_COLORS)])
        for index, label in enumerate(shown)
    }
    for label in shown:
        for line in _tail(root, label, TAIL_LINES).splitlines():
            sys.stdout.write(f"{prefixes[label]}{line}\n")
    sys.stdout.flush()
    if follow:
        _follow(root, prefixes)


def _follow(root: Path, prefixes: dict[str, str]) -> None:
    folder = state_dir(root)
    streams = {
        label: (folder / f"{label}.log").open(encoding="utf-8", errors="replace")
        for label in prefixes
    }
    for stream in streams.values():
        stream.seek(0, os.SEEK_END)
    try:
        while True:
            for label, stream in streams.items():
                for line in stream.readlines():
                    sys.stdout.write(f"{prefixes[label]}{line.rstrip()}\n")
            sys.stdout.flush()
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print()
    finally:
        for stream in streams.values():
            stream.close()


def _tail(root: Path, label: str, count: int) -> str:
    log = state_dir(root) / f"{label}.log"
    if not log.is_file():
        return ""
    return "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-count:])


def stop(root: Path) -> list[str]:
    """Stops the background processes; returns those that were running."""
    found = records(root)
    alive = {label: record["pid"] for label, record in found.items() if is_alive(record["pid"])}
    for pid in alive.values():
        signal_group(pid)
    deadline = time.monotonic() + STOP_SECONDS
    while any(is_alive(pid) for pid in alive.values()) and time.monotonic() < deadline:
        time.sleep(POLL_SECONDS)
    for pid in alive.values():
        if is_alive(pid):
            signal_group(pid, signal.SIGKILL)
    for label in found:
        (state_dir(root) / f"{label}.json").unlink(missing_ok=True)
    return list(alive)
