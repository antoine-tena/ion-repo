"""The databases a project's code needs on the machine, started by `ion repo dev`, `check`,
`install`.

They are the `db`, `postgres` and `redis` services of the project's compose file. A container
already created (a stopped `annski-db` after a reboot) is restarted as it is, its data kept;
otherwise `podman-compose up -d` creates it. Then each one with a health check is waited for, so
that Django never meets a database still starting. Without podman, nothing is started. They
outlive a Ctrl+C, ready for the next `ion repo dev`; `ion repo dev stop` stops them.
"""

import re
import shutil
import subprocess
import time
from pathlib import Path

from ion_repo.shell import KilnError, run, spinner_line, step
from ion_repo.stack import PODMAN_MARKERS

COMPOSE_FILES = ("compose.yaml", *PODMAN_MARKERS)
BACKING_SERVICES = ("db", "postgres", "redis")
HEALTHY_SECONDS = 60
POLL_SECONDS = 0.5
_SERVICE_LINE = re.compile(r"^  ([\w.-]+):\s*$")
_CONTAINER_NAME_LINE = re.compile(r"^    container_name:\s*[\"']?([\w.-]+)")
_PROJECT_NAME_LINE = re.compile(r"^name:\s*[\"']?([\w.-]+)")


def compose_file(root: Path) -> Path | None:
    return next((root / name for name in COMPOSE_FILES if (root / name).is_file()), None)


def backing_services(compose: Path) -> dict[str, str]:
    """Backing services of a compose file, each with its container: its `container_name`, or
    the name podman-compose gives it (`<project>_<service>_1`)."""
    named: dict[str, str | None] = {}
    project = compose.parent.name
    in_services = False
    current = ""
    for line in compose.read_text(encoding="utf-8").splitlines():
        if project_match := _PROJECT_NAME_LINE.match(line):
            project = project_match.group(1)
        if line and not line[0].isspace():
            in_services = line.rstrip() == "services:"
            continue
        if not in_services:
            continue
        if service_match := _SERVICE_LINE.match(line):
            current = service_match.group(1)
            if current in BACKING_SERVICES:
                named[current] = None
        elif (name_match := _CONTAINER_NAME_LINE.match(line)) and current in named:
            named[current] = name_match.group(1)
    return {service: name or f"{project}_{service}_1" for service, name in named.items()}


def app_services(compose: Path) -> list[str]:
    """The services of a compose file that are the project itself, databases aside."""
    services: list[str] = []
    in_services = False
    for line in compose.read_text(encoding="utf-8").splitlines():
        if line and not line[0].isspace():
            in_services = line.rstrip() == "services:"
        elif in_services and (found := _SERVICE_LINE.match(line)):
            services.append(found.group(1))
    return [service for service in services if service not in BACKING_SERVICES]


def start_backing_services(root: Path) -> None:
    compose = compose_file(root)
    if compose is None or shutil.which("podman") is None:
        return
    services = backing_services(compose)
    if not services:
        return
    step(f"databases ({', '.join(services)})")
    existing = [container for container in services.values() if _exists(container)]
    to_create = [service for service, container in services.items() if container not in existing]
    if existing:
        run(["podman", "start", *existing], root)
    if to_create:
        run(["podman-compose", "-f", str(compose), "up", "-d", *to_create], root)
    _wait_healthy(list(services.values()))


def stop_backing_services(root: Path) -> None:
    compose = compose_file(root)
    if compose is None or shutil.which("podman") is None:
        return
    existing = [name for name in backing_services(compose).values() if _exists(name)]
    if existing:
        run(["podman", "stop", *existing], root)


def _wait_healthy(containers: list[str]) -> None:
    """Runs each health check until it passes; a container without one is not waited for."""
    waiting = [container for container in containers if _has_health_check(container)]
    if not waiting:
        return
    deadline = time.monotonic() + HEALTHY_SECONDS
    with spinner_line(f"waiting for {', '.join(waiting)}"):
        while waiting:
            waiting = [container for container in waiting if not _passes_check(container)]
            if waiting and time.monotonic() > deadline:
                raise KilnError(f"{', '.join(waiting)} not healthy after {HEALTHY_SECONDS} s")
            if waiting:
                time.sleep(POLL_SECONDS)


def _has_health_check(container: str) -> bool:
    template = "{{if .Config.Healthcheck}}yes{{end}}"
    inspected = _podman("inspect", "--format", template, container)
    return inspected.returncode == 0 and inspected.stdout.strip() == "yes"


def _passes_check(container: str) -> bool:
    return _podman("healthcheck", "run", container).returncode == 0


def _exists(container: str) -> bool:
    return _podman("container", "exists", container).returncode == 0


def _podman(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["podman", *arguments], capture_output=True, text=True, check=False)
