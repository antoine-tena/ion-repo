"""The dependencies of an ion-repo installed from its checkout (`uv tool install --editable`), kept
in step with the checkout's `pyproject.toml`.

Such a tool reads its code live, so a merge into `develop` reaches it at once; its dependencies
were resolved at install time and stay there. When the code asks for a newer one (ion-score
0.1.2 while 0.1.0 is installed), every command would fail on an import: so, before anything else
is imported, the tool is installed again from the same checkout and the command started anew.
Only in a uv tool environment (its `uv-receipt.toml`): a project's `.venv` is `uv sync`'s. Standard
library only (and `packaging` when present): what is missing may be anything else.
"""

import contextlib
import importlib
import json
import os
import subprocess
import sys
import tomllib
from collections.abc import Iterator
from importlib import metadata
from pathlib import Path

PACKAGE = "ion-repo"
RECEIPT = "uv-receipt.toml"
# Set before the command starts anew: one attempt per command, never a loop.
DONE_VARIABLE = "ION_REPO_RESYNCED"
INSTALL_TIMEOUT_SECONDS = 300


def editable_checkout() -> Path | None:
    """The checkout an ion-repo uv tool reads live; None for any other install."""
    if not (Path(sys.prefix) / RECEIPT).is_file():
        return None
    try:
        origin = json.loads(metadata.distribution(PACKAGE).read_text("direct_url.json") or "{}")
    except metadata.PackageNotFoundError, ValueError:
        return None
    if not origin.get("dir_info", {}).get("editable"):
        return None
    checkout = Path(str(origin.get("url", "")).removeprefix("file://"))
    return checkout if (checkout / "pyproject.toml").is_file() else None


def unmet(checkout: Path) -> list[str]:
    """The checkout's dependencies the environment does not satisfy (`ion-score>=0.1.2`)."""
    try:
        from packaging.requirements import Requirement
    except ImportError:
        return ["packaging"]
    try:
        project = tomllib.loads((checkout / "pyproject.toml").read_text())["project"]
    except OSError, tomllib.TOMLDecodeError, KeyError:
        return []
    missing = []
    for line in project.get("dependencies", []):
        requirement = Requirement(line)
        if requirement.marker is not None and not requirement.marker.evaluate():
            continue
        try:
            installed = metadata.version(requirement.name)
        except metadata.PackageNotFoundError:
            missing.append(line)
            continue
        if not requirement.specifier.contains(installed, prereleases=True):
            missing.append(f"{line} ({installed} installed)")
    return missing


@contextlib.contextmanager
def _locked() -> Iterator[None]:
    """One reinstall at a time on the machine; the others wait, then find nothing left to do."""
    try:
        import fcntl
    except ImportError:  # Windows
        yield
        return
    state = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")
    lock = state / "ion-repo" / "resync.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def ensure() -> None:
    """Installed again, then the command started anew, when the checkout outgrew the tool."""
    if os.environ.get(DONE_VARIABLE):
        return
    checkout = editable_checkout()
    if checkout is None or not unmet(checkout):
        return
    with _locked():
        importlib.invalidate_caches()  # another command may have installed it meanwhile
        missing = unmet(checkout)
        if not missing:
            return
        print(
            f"ion-repo: dependencies behind the checkout ({', '.join(missing)}), installing again…",
            file=sys.stderr,
        )
        if not _reinstall(checkout):
            return
    os.environ[DONE_VARIABLE] = "1"
    os.execv(sys.argv[0], sys.argv)


def _reinstall(checkout: Path) -> bool:
    command = ["uv", "tool", "install", "--reinstall", "--editable", str(checkout)]
    try:
        done = subprocess.run(
            command, capture_output=True, text=True, timeout=INSTALL_TIMEOUT_SECONDS, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        detail = str(error)
    else:
        if not done.returncode:
            return True
        detail = " ".join(done.stderr.strip().splitlines()[-1:])
    print(f"ion-repo: reinstall failed ({detail}); by hand: {' '.join(command)}", file=sys.stderr)
    return False
