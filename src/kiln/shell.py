"""Running external commands (git, uv, pnpm, gh) and messages to the user."""

import os
import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from kiln import ui


class KilnError(Exception):
    """Expected error, shown to the user without a traceback."""


def step(title: str) -> None:
    ui.step(title)


# Full output of the commands, without the spinner (diagnosis).
VERBOSE_VARIABLE = "KILN_VERBOSE"


def run(
    command: list[str], cwd: Path, env: dict[str, str] | None = None, *, live: bool = False
) -> None:
    """Runs a command; fails if it fails. `live`: output shown as is, for an interactive command
    or one whose output is the result."""
    returncode = run_status(command, cwd, env, live=live)
    if returncode != 0:
        raise KilnError(f"`{' '.join(command)}` failed (code {returncode})")


def run_status(
    command: list[str], cwd: Path, env: dict[str, str] | None = None, *, live: bool = False
) -> int:
    """Runs a command and returns its code. In a terminal, a spinner replaces its output, shown
    in full only if it fails."""
    if live or not shows_spinner():
        return subprocess.run(command, cwd=cwd, env=env, check=False).returncode
    spinner = ui.Spinner(" ".join(command))
    output: list[str] = []
    spinner.start()
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
        )
        for line in process.stdout or ():
            output.append(line)
            spinner.show(line)
        returncode = process.wait()
    finally:
        spinner.stop()
    spinner.finish(succeeded=returncode == 0, output="".join(output))
    return returncode


def shows_spinner() -> bool:
    """Whether a spinner replaces what runs: in a terminal, unless the full output is asked for."""
    return ui.is_styled() and not os.environ.get(VERBOSE_VARIABLE)


@contextmanager
def spinner_line(label: str) -> Iterator[None]:
    """Work done in kiln itself shown like a command: the spinner, then ✓ or ✗ and its
    duration."""
    spinner = ui.Spinner(label)
    spinner.start()
    succeeded = False
    try:
        yield
        succeeded = True
    finally:
        spinner.finish(succeeded=succeeded)


def capture(command: list[str], cwd: Path) -> str:
    """Runs a command and returns its standard output, stripped."""
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise KilnError(f"`{' '.join(command)}` failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


INSTALL_HINTS = {
    "git": "https://git-scm.com/downloads",
    "uv": "curl -LsSf https://astral.sh/uv/install.sh | sh",
    "pnpm": "npm install -g pnpm (Node 24 required)",
    "gh": "https://cli.github.com, then gh auth login",
}


def require_tools(*tool_names: str) -> None:
    missing_tools = [name for name in tool_names if shutil.which(name) is None]
    if missing_tools:
        hints = "\n".join(f"  {name}: {INSTALL_HINTS.get(name, '')}" for name in missing_tools)
        raise KilnError(f"missing tools:\n{hints}")


def repo_root(start: Path) -> Path:
    try:
        return Path(capture(["git", "rev-parse", "--show-toplevel"], start))
    except KilnError:
        raise KilnError(f"{start} is not in a git repo: go into a repo, or kiln new") from None
