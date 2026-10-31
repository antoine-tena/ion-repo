"""Converters of `kiln fix`: containers and runtimes (T-128, T-159).

Images are not built here: `kiln fix` builds an image a converter touched when podman or docker
is there. Compose services are hardened only where podman proves they still start hardened, on a
throwaway copy of the repo.
"""

import contextlib
import datetime
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

import yaml  # brought by copier

from ion_repo import shell, ui
from ion_repo.grid import detectors
from ion_repo.grid.detectors import COMPOSE_FILES, CONTAINER_FILES
from ion_repo.grid.facts import Repo
from ion_repo.grid.fixers import Fixer, register, resolve
from ion_repo.shell import KilnError

FROM = re.compile(r"^(?P<head>\s*FROM\s+(?:--\S+\s+)*)(?P<image>\S+)(?P<tail>.*)$", re.I)
OLD_DEBIAN = re.compile(r"\b(bookworm|bullseye|buster|stretch)\b")
NODE_LTS = "24"
PYTHON_PIN = "3.13"
RUNTIME_TAG = re.compile(
    r"(?P<pre>(?:\S+/)?(?P<runtime>python|node)):v?(?P<v>\d+(?:\.\d+)?)(?P<rest>.*)"
)
# Bases where a plain user can run the app; others (php-apache binds port 80) are left out.
USER_READY = frozenset({"python", "node", "debian", "ubuntu", "alpine"})


def _write(repo: Repo, name: str, text: str) -> None:
    (repo.root / name).write_text(text, encoding="utf-8")


def _stages(lines: list[str]) -> set[str]:
    return {
        found.group(1).lower()
        for line in lines
        if (found := re.match(r"\s*FROM\s+.*\s+AS\s+(\S+)", line, re.I))
    }


def _edit_images(repo: Repo, edit: Callable[[str], str | None]) -> list[str]:
    changed = []
    for name in repo.matching(*CONTAINER_FILES):
        lines = repo.text(name).splitlines(keepends=True)
        stages = _stages(lines)
        edited = False
        for index, line in enumerate(lines):
            found = FROM.match(line.rstrip("\n"))
            if not found:
                continue
            image = found["image"]
            if image.lower() in stages or image == "scratch" or "$" in image:
                continue
            new = edit(image)
            if new and new != image:
                ending = "\n" if line.endswith("\n") else ""
                lines[index] = f"{found['head']}{new}{found['tail']}{ending}"
                edited = True
        if edited:
            _write(repo, name, "".join(lines))
            changed.append(name)
    return changed


def _pin(image: str) -> str:
    name = image.split("@")[0]
    tagged = name if ":" in name.rsplit("/", 1)[-1] else f"{name}:latest"
    return f"{name}@{resolve.image_digest(tagged)}"


def _runtime_moved(name: str) -> str:
    """The image's Python or Node moved to a supported line when past its end of life."""
    found = RUNTIME_TAG.fullmatch(name)
    if not found:
        return name
    runtime, version = found["runtime"], found["v"]
    line = ".".join(version.split(".")[:2]) if runtime == "python" else version.split(".")[0]
    if _supported(runtime, line):
        return name
    return f"{found['pre']}:{PYTHON_PIN if runtime == 'python' else NODE_LTS}{found['rest']}"


def _current(name: str) -> str:
    """An image moved to a supported runtime and to Debian 13 at once: either move alone may
    name an image that was never built (`python:3.8-trixie`, `python:3.13-buster`)."""
    return OLD_DEBIAN.sub("trixie", _runtime_moved(name))


def pin_images(repo: Repo) -> list[str]:
    """Each base image pinned by digest, its tag kept for the reader and for Dependabot."""
    return _edit_images(repo, lambda image: None if "@sha256:" in image else _pin(image))


def move_to_trixie(repo: Repo) -> list[str]:
    """Images on an older Debian moved to Debian 13 (trixie), re-pinned when they were."""

    def edit(image: str) -> str | None:
        if not OLD_DEBIAN.search(image.split("@")[0]):
            return None
        moved = _current(image.split("@")[0])
        return _pin(moved) if "@sha256:" in image else moved

    return _edit_images(repo, edit)


def add_user(repo: Repo) -> list[str]:
    """The stage that runs switches to a non-root user: `node` on Node images, a system user
    `app` elsewhere (Debian or Alpine)."""
    changed = []
    for name in repo.matching(*CONTAINER_FILES):
        lines = repo.text(name).splitlines(keepends=True)
        froms = [index for index, line in enumerate(lines) if FROM.match(line)]
        if not froms:
            continue
        last = froms[-1]
        found = FROM.match(lines[last].rstrip("\n"))
        base = found["image"].lower() if found else ""
        users = [line for line in lines[last:] if re.match(r"\s*USER\s+\S", line, re.I)]
        if users and users[-1].split()[1].lower() not in detectors.ROOT_USERS:
            continue
        image = base.split("/")[-1].split(":")[0]
        if image not in USER_READY:
            continue  # another base (Apache, nginx, a database): which user is judgment
        if image == "node":
            block = ["USER node\n"]
        elif "alpine" in base or image == "alpine":
            block = ["RUN addgroup -S app && adduser -S -G app app\n", "USER app\n"]
        else:
            block = [
                "RUN useradd --system --create-home --shell /usr/sbin/nologin app\n",
                "USER app\n",
            ]
        at = next(
            (
                index
                for index in range(last, len(lines))
                if re.match(r"\s*(CMD|ENTRYPOINT)\b", lines[index], re.I)
            ),
            len(lines),
        )
        if at == len(lines) and lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines[at:at] = block
        _write(repo, name, "".join(lines))
        changed.append(name)
    return changed


def _supported(runtime: str, line: str) -> bool:
    end = detectors.END_OF_LIFE[runtime].get(line)
    return end is None or end >= datetime.date.today().isoformat()


def _oldest_python() -> str:
    today = datetime.date.today().isoformat()
    lines = [line for line, end in detectors.END_OF_LIFE["python"].items() if end >= today]
    return min(lines, key=lambda line: tuple(map(int, line.split("."))))


def move_runtimes(repo: Repo) -> list[str]:
    """Node past its end of life moved to the current LTS, Python to a supported line, wherever
    they are named: version files, `engines`, image tags, `requires-python`."""
    changed: set[str] = set()
    for name in repo.matching("**/.nvmrc", "**/.node-version"):
        text = repo.text(name).strip()
        if text and not _supported("node", text.lstrip("v").split(".")[0]):
            _write(repo, name, NODE_LTS + "\n")
            changed.add(name)
    for name in repo.matching("**/.python-version"):
        text = repo.text(name).strip()
        if text and not _supported("python", ".".join(text.split(".")[:2])):
            _write(repo, name, PYTHON_PIN + "\n")
            changed.add(name)
    for name in repo.matching("**/package.json"):
        if "node_modules/" in name:
            continue
        text = repo.text(name)
        found = re.search(r'("node"\s*:\s*")([^"\d]*)(\d+)([^"]*")', text)
        if found and not _supported("node", found.group(3)):
            new = text[: found.start()] + f'{found.group(1)}>={NODE_LTS}"' + text[found.end() :]
            json.loads(new)  # still JSON
            _write(repo, name, new)
            changed.add(name)
    for name in repo.matching("**/pyproject.toml"):
        text = repo.text(name)
        found = re.search(r'(requires-python\s*=\s*["\'][^0-9]*)(\d+\.\d+)', text)
        if found and not _supported("python", found.group(2)):
            oldest = _oldest_python()
            _write(repo, name, text[: found.start(2)] + oldest + text[found.end(2) :])
            changed.add(name)

    def edit(image: str) -> str | None:
        name = image.split("@")[0]
        if _runtime_moved(name) == name:
            return None
        moved = _current(name)
        return _pin(moved) if "@sha256:" in image else moved

    changed.update(_edit_images(repo, edit))
    return sorted(changed)


# What a hardened service gets: no write outside its volumes (a tmpfs for /tmp, which most
# programs need), no capability, no privilege gained through setuid.
HARDENING = (
    ("read_only", "read_only: true"),
    ("cap_drop", "cap_drop: [ALL]"),
    ("security_opt", "security_opt: [no-new-privileges:true]"),
    ("tmpfs", "tmpfs: [/tmp]"),
)
START_TIMEOUT = 600
SETTLE_SECONDS = 5
_SERVICE = re.compile(r"^(?P<indent>\s+)(?P<name>[\w.-]+):\s*(#.*)?$")


def _unhardened(text: str) -> list[str]:
    try:
        compose = yaml.safe_load(text)
    except yaml.YAMLError:
        return []
    services = compose.get("services") if isinstance(compose, dict) else None
    return [
        service
        for service, settings in (services or {}).items()
        if isinstance(settings, dict) and not _is_hardened(settings)
    ]


def _is_hardened(settings: dict[str, object]) -> bool:
    caps = settings.get("cap_drop")
    options = settings.get("security_opt")
    return (
        settings.get("read_only") is True
        and isinstance(caps, list)
        and "ALL" in [str(cap).upper() for cap in caps]
        and isinstance(options, list)
        and any("no-new-privileges" in str(option) for option in options)
    )


def harden_text(text: str, services: list[str]) -> str:
    """The compose file with the keys a hardened service lacks added under each of `services`;
    a key it already sets is left as written (`read_only: false` is a choice: judgment's)."""
    try:
        compose = yaml.safe_load(text)
    except yaml.YAMLError:
        return text
    settings = (compose or {}).get("services") or {}
    lines = text.splitlines(keepends=True)
    in_services, depth = False, None
    out: list[str] = []
    for index, line in enumerate(lines):
        out.append(line)
        if line.strip() and not line[0].isspace():
            in_services = line.rstrip().startswith("services:")
            depth = None
            continue
        found = _SERVICE.match(line.rstrip("\n"))
        if not in_services or not found:
            continue
        depth = depth or len(found["indent"])
        if len(found["indent"]) != depth or found["name"] not in services:
            continue
        own = settings.get(found["name"]) or {}
        child = next(
            (
                len(later) - len(later.lstrip())
                for later in lines[index + 1 :]
                if later.strip() and not later.lstrip().startswith("#")
            ),
            depth + 2,
        )
        child = child if child > depth else depth + 2
        if not out[-1].endswith("\n"):
            out[-1] += "\n"
        out += [" " * child + f"{entry}\n" for key, entry in HARDENING if key not in own]
    return "".join(out)


def harden_compose(repo: Repo) -> list[str]:
    """Each compose service read-only, every capability dropped, no privilege escalation, kept
    only where podman starts it hardened on a throwaway copy; the others are left as they were
    and named."""
    targets = {
        name: found
        for name in repo.matching(*COMPOSE_FILES)
        if (found := _unhardened(repo.text(name)))
    }
    if not targets:
        return []
    if not _podman_ready():
        raise KilnError(
            "podman and podman-compose are needed to prove each service still starts hardened: "
            "https://podman.io/docs/installation"
        )
    changed: list[str] = []
    left: list[str] = []
    for name, services in targets.items():
        text = repo.text(name)
        started = _starts(repo.root, name, harden_text(text, services), services)
        final = harden_text(text, [service for service in services if service in started])
        if final != text:
            (repo.root / name).write_text(final, encoding="utf-8")
            changed.append(name)
        left += [f"{name} ({service})" for service in services if service not in started]
    if not changed:
        raise KilnError(f"no service starts hardened: {', '.join(left)}")
    if left:
        ui.note(f"left as they were, they do not start hardened: {', '.join(left)}")
    return changed


def _podman_ready() -> bool:
    return shutil.which("podman") is not None and shutil.which("podman-compose") is not None


def _starts(root: Path, name: str, hardened: str, services: list[str]) -> set[str]:
    """The services podman keeps running, hardened, on a copy of the repo: their own project
    name, no fixed container name, so that nothing the user runs is touched."""
    project = f"kiln-harden-{os.getpid()}"
    with tempfile.TemporaryDirectory(prefix="kiln-harden-") as scratch:
        copy = Path(scratch) / "repo"
        subprocess.run(
            ["git", "worktree", "add", "-q", "--detach", str(copy)],
            cwd=root,
            capture_output=True,
            check=False,
        )
        if not copy.is_dir():
            return set()
        compose = copy / name
        compose.write_text(re.sub(r"(?m)^\s+container_name:.*\n", "", hardened), encoding="utf-8")
        command = ["podman-compose", "-p", project, "-f", str(compose)]
        # Building the images can take minutes: said, so that the run does not look stuck.
        label = f"podman builds and starts {', '.join(services)} hardened, on a throwaway copy"
        if not shell.shows_spinner():
            ui.note(f"{label} (up to {START_TIMEOUT // 60} min)")
        try:
            with shell.spinner_line(label) if shell.shows_spinner() else contextlib.nullcontext():
                subprocess.run(
                    [*command, "up", "-d", *services],
                    cwd=compose.parent,
                    capture_output=True,
                    timeout=START_TIMEOUT,
                    check=False,
                )
                time.sleep(SETTLE_SECONDS)
            return {service for service in services if _running(project, service)}
        except subprocess.TimeoutExpired:
            return set()
        finally:
            subprocess.run(
                [*command, "down", "-v"], cwd=compose.parent, capture_output=True, check=False
            )
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(copy)],
                cwd=root,
                capture_output=True,
                check=False,
            )


def _running(project: str, service: str) -> bool:
    listed = subprocess.run(
        [
            "podman", "ps", "-q",
            "--filter", f"label=io.podman.compose.project={project}",
            "--filter", f"label=io.podman.compose.service={service}",
            "--filter", "status=running",
        ],
        capture_output=True,
        text=True,
        check=False,
    )  # fmt: skip
    return bool(listed.stdout.strip())


register(Fixer("harden_compose", harden_compose, "compose services hardened", network=True))
register(Fixer("pin_images", pin_images, "base images pinned by digest", network=True))
register(Fixer("move_to_trixie", move_to_trixie, "images moved to Debian 13", network=True))
register(Fixer("add_user", add_user, "images run as a non-root user"))
register(Fixer("move_runtimes", move_runtimes, "runtimes moved off their end of life"))
