"""Running external commands (git, uv, pnpm, gh) and messages to the user."""

import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from typing import TextIO

from ion_score import ui
from ion_score.shell import (
    ENV_PREFIX,
    INSTALL_HINTS,
    LEGACY_ENV_PREFIX,
    VERBOSE_VARIABLE,
    IonError,
    capture,
    environment,
    run,
    run_status,
    shows_spinner,
    spinner_line,
)

# Running a command and its error live in ion-score, re-exported here for ion-repo's modules.
__all__ = [
    "ENV_PREFIX",
    "INSTALL_HINTS",
    "LEGACY_ENV_PREFIX",
    "QUIET_GIT_SETTINGS",
    "VERBOSE_VARIABLE",
    "KilnError",
    "capture",
    "environment",
    "output_to",
    "quiet_git",
    "repo_root",
    "require_clean_tree",
    "require_tools",
    "run",
    "run_status",
    "shows_spinner",
    "spinner_line",
    "step",
]


# ion-repo's expected error is ion-score's: one class, caught the same on both sides.
KilnError = IonError


def step(title: str) -> None:
    ui.step(title)


@contextmanager
def output_to(log: Path) -> Iterator[TextIO]:
    """Everything written meanwhile, by ion-repo and the commands it runs (pre-commit's hooks
    included), goes to `log`, as outside a terminal; yields the terminal, for one line of
    progress."""
    sys.stdout.flush()
    sys.stderr.flush()
    saved = os.dup(1), os.dup(2)
    terminal = os.fdopen(os.dup(saved[0]), "w")
    try:
        # Line by line, so that ion-repo's lines and its commands' stay in order.
        with log.open("w", buffering=1) as written:
            os.dup2(written.fileno(), 1)
            os.dup2(written.fileno(), 2)
            try:
                with redirect_stdout(written), redirect_stderr(written):
                    yield terminal
            finally:
                os.dup2(saved[0], 1)
                os.dup2(saved[1], 2)
    finally:
        terminal.close()
        for descriptor in saved:
            os.close(descriptor)


def require_clean_tree(root: Path) -> None:
    """Fails on uncommitted changes, naming the first files, so that the user knows what to set
    aside."""
    listing = subprocess.run(
        ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=False
    )
    changes = listing.stdout.splitlines()
    if not changes:
        return
    shown = [line[3:] for line in changes[:5]]
    if len(changes) > 5:
        shown.append(f"… {len(changes) - 5} more")
    listed = "\n".join(f"  {path}" for path in shown)
    raise KilnError(f"working tree not clean: commit or set aside the changes\n{listed}")


def require_tools(*tool_names: str) -> None:
    missing_tools = [name for name in tool_names if shutil.which(name) is None]
    if missing_tools:
        hints = "\n".join(f"  {name}: {INSTALL_HINTS.get(name, '')}" for name in missing_tools)
        raise KilnError(f"missing tools:\n{hints}")


def repo_root(start: Path) -> Path:
    try:
        return Path(capture(["git", "rev-parse", "--show-toplevel"], start))
    except KilnError:
        raise KilnError(f"{start} is not in a git repo: go into a repo, or ion repo new") from None


# Git's background housekeeping, off while Copier works in its throwaway repos: a detached
# `gc --auto` still writing in `.git/objects` made Copier's removal of the folder fail
# ("Directory not empty"), at random.
QUIET_GIT_SETTINGS = (("gc.auto", "0"), ("gc.autoDetach", "false"), ("maintenance.auto", "false"))


@contextmanager
def quiet_git() -> Iterator[None]:
    """The git commands started meanwhile run without background housekeeping, through the
    `GIT_CONFIG_COUNT` variables, added to those already set."""
    saved = {key: os.environ.get(key) for key in _quiet_git_keys()}
    count = int(os.environ.get("GIT_CONFIG_COUNT", "0") or 0)
    for offset, (key, value) in enumerate(QUIET_GIT_SETTINGS):
        os.environ[f"GIT_CONFIG_KEY_{count + offset}"] = key
        os.environ[f"GIT_CONFIG_VALUE_{count + offset}"] = value
    os.environ["GIT_CONFIG_COUNT"] = str(count + len(QUIET_GIT_SETTINGS))
    try:
        yield
    finally:
        for key in _quiet_git_keys():
            os.environ.pop(key, None)
        os.environ.update({key: value for key, value in saved.items() if value is not None})


def _quiet_git_keys() -> list[str]:
    count = int(os.environ.get("GIT_CONFIG_COUNT", "0") or 0) + len(QUIET_GIT_SETTINGS)
    indexes = range(count)
    return [
        "GIT_CONFIG_COUNT",
        *(f"GIT_CONFIG_KEY_{index}" for index in indexes),
        *(f"GIT_CONFIG_VALUE_{index}" for index in indexes),
    ]
