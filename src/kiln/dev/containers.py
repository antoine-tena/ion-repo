"""`kiln dev --containers`: the whole stack in podman, as in production, from its compose file.

The image of production rather than a place to code: what changes needs a new build. Podman
keeps it in the background (`--foreground`: in the terminal); a marker in the state folder
tells `status`, `logs` and `stop` to ask podman.
"""

import contextlib
from pathlib import Path

from kiln.dev.background import state_dir
from kiln.dev.backing import compose_file
from kiln.shell import KilnError, require_tools, run, step

DETACHED_MARKER = "containers"


def is_detached(root: Path) -> bool:
    return (state_dir(root) / DETACHED_MARKER).exists()


def up(root: Path, *, detached: bool) -> None:
    compose = _compose(root)
    step(f"podman stack ({compose.relative_to(root)})")
    command = _compose_command(compose, "up", "--build")
    if detached:
        run([*command, "-d"], root, live=True)
        state_dir(root).mkdir(parents=True, exist_ok=True)
        (state_dir(root) / DETACHED_MARKER).touch()
        return
    try:
        run(command, root, live=True)
    except KeyboardInterrupt:
        run(_compose_command(compose, "down"), root, live=True)


def show_status(root: Path) -> None:
    run(_compose_command(_compose(root), "ps"), root, live=True)


def show_logs(root: Path, service: str | None, *, follow: bool) -> None:
    options = ["--tail", "40", *(["-f"] if follow else [])]
    command = _compose_command(_compose(root), "logs", *options, *([service] if service else []))
    with contextlib.suppress(KeyboardInterrupt):
        run(command, root, live=True)


def stop(root: Path) -> None:
    run(_compose_command(_compose(root), "down"), root, live=True)
    (state_dir(root) / DETACHED_MARKER).unlink(missing_ok=True)


def _compose(root: Path) -> Path:
    compose = compose_file(root)
    if compose is None:
        raise KilnError("no podman in this project: kiln set podman=true, on a branch")
    require_tools("podman", "podman-compose")
    return compose


def _compose_command(compose: Path, *arguments: str) -> list[str]:
    return ["podman-compose", "-f", str(compose), *arguments]
