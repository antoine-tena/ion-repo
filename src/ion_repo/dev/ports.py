"""The port each server of `ion repo dev` listens on: its stack's own, or the next free one.

A server whose port another process holds (another project's `ion repo dev`) moves to the next
free port: told by its command (`runserver 8001`, `--port`, `--server.port`) or its environment
(`PORT`, `NUXT_PORT`). The other processes follow: a value of their environment naming a moved
port (`http://localhost:8000/api`) names the new one; a front without one gets the backend's real
address in the variables the template's configs read (`NUXT_BACKEND_URL`, `BACKEND_URL`,
`API_URL`), and in those its own config reads with a default on the old port
(`process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'`). A server that cannot be told
its port (a `Procfile.dev` line) is not moved.

A server is ready once its own process group listens on its port, read in `/proc` (#60):
another process answering there is not taken for it. Without `/proc` (macOS), anyone answering.
"""

import contextlib
import os
import re
import socket
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ion_repo.stack import Command

# Port each stack's server listens on, to know when it is ready and where to open it.
DEV_PORTS = {
    "django": 8000,
    "fastapi": 8000,
    "data": 2718,
    "nuxt": 3000,
    "next": 3000,
    "astro": 4321,
    "vite-react": 5173,
    "streamlit": 8501,
    "dash": 8050,
}
# Ports tried after a taken one.
PORT_TRIES = 100
# Servers told their port by their environment, and the variables they read it from.
PORT_VARIABLES = {
    "nuxt": ("NUXT_PORT", "PORT"),
    "next": ("PORT",),
    "dash": ("PORT",),
}
BACKENDS = ("django", "fastapi")
# Where the template's fronts read the backend's address (Nuxt, Next/Astro/Vite, Python).
BACKEND_ORIGIN_VARIABLES = ("NUXT_BACKEND_URL", "BACKEND_URL", "API_URL")
CONFIG_FILES = "*.config.*"
# `process.env.NAME || 'http://localhost:8000/api'` (or `??`) in a front's config.
_CONFIG_DEFAULT = re.compile(
    r"process\.env\.([A-Z][A-Z0-9_]*)\s*(?:\|\||\?\?)\s*(['\"`])(https?://[^'\"`\s]+)\2"
)
_LOCAL_PORT = re.compile(r"\b(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]):(\d+)\b")
POLL_SECONDS = 0.25
# Both loopbacks: a server bound to `localhost` may listen on IPv6 only (Nuxt on macOS).
LOOPBACKS = (
    (socket.AF_INET, "127.0.0.1"),
    (socket.AF_INET6, "::1"),
)
PROC = Path("/proc")
_TCP_TABLES = ("net/tcp", "net/tcp6")
_LISTEN = "0A"


@dataclass(frozen=True)
class Ports:
    """The port chosen for each server: its stack's own, or the next free one."""

    chosen: Mapping[str, int] = field(default_factory=dict)

    def of(self, label: str) -> int | None:
        return self.chosen.get(label, DEV_PORTS.get(label))

    def moves(self) -> dict[int, int]:
        """Each stack port left, and the port taken instead."""
        chosen = self.chosen.items()
        return {DEV_PORTS[label]: port for label, port in chosen if _moved(label, port)}

    def argv(self, command: Command) -> tuple[str, ...]:
        port = self.chosen.get(command.label)
        if port is None or not _moved(command.label, port):
            return command.argv
        return with_port(command, port) or command.argv

    def env(self, command: Command, current: Mapping[str, str], folder: Path) -> dict[str, str]:
        """What a process's environment changes for the ports moved."""
        moves = self.moves()
        if not moves:
            return {}
        changed = {
            key: moved
            for key, value in current.items()
            if (moved := moved_url(value, moves)) != value
        }
        port = self.chosen.get(command.label)
        if port is not None and _moved(command.label, port):
            changed |= dict.fromkeys(PORT_VARIABLES.get(command.label, ()), str(port))
        backend = next((label for label in BACKENDS if _moved(label, self.of(label))), None)
        if backend is None or command.label == backend:
            return changed
        origin = f"http://localhost:{self.of(backend)}"
        for name in BACKEND_ORIGIN_VARIABLES:
            if name not in current:
                changed[name] = origin
        for name, default in config_defaults(folder):
            if name not in current and (moved := moved_url(default, moves)) != default:
                changed[name] = moved
        return changed


def _moved(label: str, port: int | None) -> bool:
    return port is not None and port != DEV_PORTS.get(label)


def with_port(command: Command, port: int) -> tuple[str, ...] | None:
    """The command of a stack server on another port; None when it cannot be told one."""
    argv = command.argv
    label = command.label
    if argv[0] == "sh":  # a Procfile.dev line: its own command, never rewritten
        return None
    if label in PORT_VARIABLES:
        return argv
    if label == "django" and argv[-1] == "runserver":
        return (*argv, str(port))
    if label in ("fastapi", "data") and "--port" in argv:
        index = argv.index("--port") + 1
        return (*argv[:index], str(port), *argv[index + 1 :])
    if label == "streamlit":
        return (*argv, "--server.port", str(port))
    if label in ("astro", "vite-react"):
        separator = ("--",) if argv[0] == "npm" else ()  # npm keeps the options before `--`
        strict = ("--strictPort",) if label == "vite-react" else ()  # Vite would move alone
        return (*argv, *separator, "--port", str(port), *strict)
    return None


def moved_url(value: str, moves: Mapping[int, int]) -> str:
    """A value naming a local port that moved names the new one."""

    def replace(found: re.Match[str]) -> str:
        port = int(found[2])
        return f"{found[1]}:{moves.get(port, port)}"

    return _LOCAL_PORT.sub(replace, value)


def config_defaults(folder: Path) -> list[tuple[str, str]]:
    """The variables a folder's configs read with a URL as default: `process.env.X || 'url'`."""
    found = []
    for path in sorted(folder.glob(CONFIG_FILES)):
        with contextlib.suppress(OSError, UnicodeDecodeError):
            text = path.read_text(encoding="utf-8")
            found += [(match[1], match[3]) for match in _CONFIG_DEFAULT.finditer(text)]
    return found


def listens(port: int) -> bool:
    return any(_answers(family, host, port) for family, host in LOOPBACKS)


def _answers(family: socket.AddressFamily, host: str, port: int) -> bool:
    try:
        with socket.socket(family) as probe:
            probe.settimeout(POLL_SECONDS)
            return probe.connect_ex((host, port)) == 0
    except OSError:  # no IPv6 on this machine
        return False


def serves(port: int, leader: int) -> bool:
    """Whether the process group `leader` leads listens on the port; anyone, without `/proc`."""
    inodes = _listening_sockets(port)
    if inodes is None:
        return listens(port)
    return bool(inodes) and any(
        leader in _group_and_session(process) and _holds(process, inodes)
        for process in PROC.iterdir()
        if process.name.isdigit()
    )


def _listening_sockets(port: int) -> set[str] | None:
    """`socket:[inode]` of each socket listening on the port; None when `/proc` cannot tell."""
    tables = []
    for table in _TCP_TABLES:
        with contextlib.suppress(OSError):
            tables.append((PROC / table).read_text(encoding="utf-8"))
    if not tables:
        return None
    sockets = set()
    for line in "\n".join(tables).splitlines():
        fields = line.split()
        if len(fields) > 9 and fields[3] == _LISTEN and fields[1].endswith(f":{port:04X}"):
            sockets.add(f"socket:[{fields[9]}]")
    return sockets


def _group_and_session(process: Path) -> tuple[int, ...]:
    """Process group and session: pnpm 10 runs a script in a group of its own, same session."""
    try:
        stat = (process / "stat").read_text(encoding="utf-8")
    except OSError:
        return ()
    fields = stat.rsplit(")", 1)[-1].split()  # state, parent, group, session
    return tuple(int(field) for field in fields[2:4])


def _holds(process: Path, sockets: set[str]) -> bool:
    with contextlib.suppress(OSError):
        for descriptor in (process / "fd").iterdir():
            with contextlib.suppress(OSError):
                if os.readlink(descriptor) in sockets:
                    return True
    return False


def listener(port: int) -> str | None:
    """`name (pid N)` of the process listening on the port, when `ss` can tell."""
    try:
        listing = subprocess.run(
            ["ss", "-Hltnp", f"sport = :{port}"], capture_output=True, text=True, check=False
        ).stdout
    except OSError:  # no `ss` (macOS)
        return None
    found = re.search(r'users:\(\("([^"]+)",pid=(\d+)', listing)
    return f"{found[1]} (pid {found[2]})" if found else None
