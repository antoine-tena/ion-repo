"""`kiln dev`: the project running on the machine, in the foreground or in the background.

What is edited runs on the machine, reloaded at each change: the stack's servers and the
processes of the `Procfile.dev`s (`processes`); a big project asks which ones (`menu`). What is
never edited runs in podman: the databases of the compose file (`backing`), started when a
process outside the front needs them. Everything runs in the background, then the logs are
offered (`background`); `kiln dev status`, `kiln dev logs [service] [-f]` and `kiln dev stop`
read and stop it. `--foreground` keeps it in the terminal, Ctrl+C stopping the processes and
keeping the databases (`foreground`). `--containers` runs the whole stack in podman instead
(`containers`).
"""

from pathlib import Path

from kiln import ui
from kiln.dev import background, containers, menu
from kiln.dev.backing import start_backing_services, stop_backing_services
from kiln.dev.foreground import run_foreground, service_prefix
from kiln.dev.processes import dev_processes, node_installs, read_env_file, runs_beyond_front
from kiln.shell import KilnError, run, step
from kiln.stack import load_stack

ACTIONS = ("status", "logs", "stop")

__all__ = ["ACTIONS", "read_env_file", "run_dev", "service_prefix"]


def run_dev(
    root: Path,
    action: str | None = None,
    *,
    in_containers: bool = False,
    foreground: bool = False,
    only: list[str] | None = None,
    follow: bool = False,
    service: str | None = None,
) -> None:
    if action is None:
        ask = input if menu.is_interactive() else None
        if background.running(root) or containers.is_detached(root):
            ui.note("already running in the background")
            _status(root)
            _offer_logs(root, ask)
        elif in_containers:
            containers.up(root, detached=not foreground)
            _offer_logs(root, None if foreground else ask)
        else:
            _start(root, foreground=foreground, only=only, ask=ask)
    elif action == "status":
        _status(root)
    elif action == "logs":
        _logs(root, service, follow=follow)
    elif action == "stop":
        _stop(root)


def _start(root: Path, *, foreground: bool, only: list[str] | None, ask: menu.Ask | None) -> None:
    every = dev_processes(root)
    if not every:
        raise KilnError(
            "nothing to run: no server of the stack, no dev script in package.json,"
            " no Procfile.dev (`name: command`, one per line)"
        )
    front_dir = load_stack(root).frontend_dir
    commands = menu.select(every, background.state_dir(root), only, ask, front_dir)
    background.check_ports_free(root, commands)
    for install in node_installs(root, commands):
        step(f"{install.directory}/: dependencies missing or older than the lock")
        run(list(install.argv), root / install.directory)
    if runs_beyond_front(commands, front_dir):
        start_backing_services(root)
    step(" · ".join(f"{command.label} ({command.directory}/)" for command in commands))
    if foreground:
        run_foreground(root, commands)
        return
    background.start(root, commands)
    background.show_status(root)
    _offer_logs(root, ask)


def _offer_logs(root: Path, ask: menu.Ask | None) -> None:
    if ask is not None and menu.wants_logs(ask):
        _logs(root, None, follow=True)
    ui.note("kiln dev logs [service] [-f] · kiln dev status · kiln dev stop")


def _status(root: Path) -> None:
    if containers.is_detached(root):
        containers.show_status(root)
    else:
        background.show_status(root)


def _logs(root: Path, service: str | None, *, follow: bool) -> None:
    if containers.is_detached(root):
        containers.show_logs(root, service, follow=follow)
    else:
        background.show_logs(root, service, follow=follow)


def _stop(root: Path) -> None:
    if containers.is_detached(root):
        containers.stop(root)
        return
    stopped = background.stop(root)
    if background.others_running(root):
        ui.note("databases kept: another worktree of this repo still uses them")
    else:
        stop_backing_services(root)
    ui.success(f"stopped: {', '.join(stopped)}" if stopped else "nothing was running")
