"""What `kiln dev` runs on the machine: the stack's servers and each folder's `Procfile.dev`.

A `Procfile.dev` (the format of foreman and of Rails' `bin/dev`) lists one process per line,
`name: command`, run in its folder (`backend/`, `frontend/` or the root) through `sh -c`: a Celery
worker, a scheduler, a CSS watcher. A name taken by the stack (`django`) replaces its server.

A folder the stack does not serve (an adopted repo: Vite and Express at the root) runs the
scripts of its `package.json` that keep running while one edits: `dev`, `dev:*`, `server`,
`serve`, `watch`, `watch:*`, else `start`; through the package manager its lock names (npm
without one). A `Procfile.dev` line of the same name replaces such a script. Its dependencies are
installed first when `node_modules/` is missing or older than the lock (a fresh clone): the
script would otherwise stop on `vite: not found`.

Each process gets the `.env` of its folder, then, when a process outside the front runs too, its
`.env.dev` (what the full local stack changes, such as the API's address or a production key to
blank out: an empty value is kept), the shell's environment winning over both. A front run alone
thus keeps its `.env`, which may name a remote API. Each process leads its own process group:
stopping it stops the children a `sh -c` or `uv run` started.
"""

import contextlib
import json
import os
import re
import signal
import subprocess
from pathlib import Path
from typing import IO

from kiln.stack import BACKEND_DIR, FRONTEND_DIR, Command, load_stack

ENV_FILE = ".env"
DEV_ENV_FILE = ".env.dev"
PROCFILE = "Procfile.dev"
PROCFILE_DIRS = (BACKEND_DIR, FRONTEND_DIR, ".")
_PROCFILE_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(\S.*)$")
PACKAGE_FILE = "package.json"
DEV_SCRIPTS = ("dev", "server", "serve", "watch")
DEV_SCRIPT_PREFIXES = ("dev:", "watch:")
# `start` often serves the build, as in production: only when nothing else is there.
FALLBACK_SCRIPT = "start"
# Lock file, in search order, and the package manager that wrote it.
LOCK_MANAGERS = (
    ("pnpm-lock.yaml", "pnpm"),
    ("yarn.lock", "yarn"),
    ("bun.lock", "bun"),
    ("bun.lockb", "bun"),
    ("package-lock.json", "npm"),
)
# Install from the lock, by package manager, and the file it writes once done.
NODE_INSTALLS = {
    "pnpm": (("pnpm", "install", "--frozen-lockfile"), ".modules.yaml"),
    "yarn": (("yarn", "install", "--frozen-lockfile"), ".yarn-integrity"),
    "bun": (("bun", "install", "--frozen-lockfile"), ""),
    "npm": (("npm", "ci"), ".package-lock.json"),
}
NPM_WITHOUT_LOCK = ("npm", "install")


def dev_processes(root: Path) -> list[Command]:
    """The stack's servers, then the processes of the `Procfile.dev`s; a same name replaces."""
    by_label = {command.label: command for command in load_stack(root).dev_commands()}
    served = {command.directory for command in by_label.values()}
    for directory in PROCFILE_DIRS:
        if directory not in served:
            for command in package_script_commands(root, directory):
                by_label.setdefault(command.label, command)
    for directory in PROCFILE_DIRS:
        for command in procfile_commands(root, directory):
            by_label[command.label] = command
    return list(by_label.values())


def runs_beyond_front(commands: list[Command]) -> bool:
    """Whether a process outside the front runs: the local stack, databases and `.env.dev`."""
    return any(command.directory != FRONTEND_DIR for command in commands)


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


def package_script_commands(root: Path, directory: str) -> list[Command]:
    """The scripts of a folder's `package.json` that keep running, run by its package manager."""
    path = root / directory / PACKAGE_FILE
    if not path.is_file():
        return []
    try:
        scripts = json.loads(path.read_text(encoding="utf-8")).get("scripts")
    except json.JSONDecodeError, AttributeError:
        return []
    if not isinstance(scripts, dict):
        return []
    names = [
        name for name in scripts if name in DEV_SCRIPTS or name.startswith(DEV_SCRIPT_PREFIXES)
    ] or [name for name in scripts if name == FALLBACK_SCRIPT]
    manager = package_manager(root / directory)
    prefix = "" if directory == "." else f"{directory}-"
    return [
        Command(prefix + name.replace(":", "-"), directory, (manager, "run", name))
        for name in names
    ]


def node_installs(root: Path, commands: list[Command]) -> list[Command]:
    """The installs the commands' folders need: a `package.json` whose `node_modules/` is
    missing or older than its lock."""
    installs = []
    for directory in dict.fromkeys(command.directory for command in commands):
        folder = root / directory
        if not (folder / PACKAGE_FILE).is_file():
            continue
        lock = next((folder / name for name, _ in LOCK_MANAGERS if (folder / name).is_file()), None)
        argv, marker = NODE_INSTALLS[package_manager(folder)]
        installed = folder / "node_modules" / marker
        if installed.exists() and (
            lock is None or lock.stat().st_mtime <= installed.stat().st_mtime
        ):
            continue
        installs.append(Command("dependencies", directory, argv if lock else NPM_WITHOUT_LOCK))
    return installs


def package_manager(directory: Path) -> str:
    return next((manager for lock, manager in LOCK_MANAGERS if (directory / lock).is_file()), "npm")


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
    root: Path, command: Command, env: dict[str, str], output: IO[str] | int, *, full_stack: bool
) -> subprocess.Popen[str]:
    directory = root / command.directory
    dev_env = read_env_file(directory / DEV_ENV_FILE) if full_stack else {}
    return subprocess.Popen(
        list(command.argv),
        cwd=directory,
        env={**read_env_file(directory / ENV_FILE), **dev_env, **env},
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
