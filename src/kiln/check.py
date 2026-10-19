"""`kiln check`: runs the stack's checks and the charter, without stopping at the first failure."""

from pathlib import Path

from kiln import ui
from kiln.install import ensure_env_file
from kiln.shell import KilnError, run_status, step
from kiln.stack import BACKEND_DIR, load_stack


def run_checks(root: Path) -> list[str]:
    """Runs each check and returns the labels of those that failed."""
    failed_checks: list[str] = []
    stack = load_stack(root)
    # A worktree has no backend/.env (ignored by git): without it, Django does not start.
    if stack.has_api and not (root / BACKEND_DIR / ".env").exists():
        ensure_env_file(root / BACKEND_DIR)
    for command in stack.check_commands():
        step(f"Check: {command.label}")
        if run_status(list(command.argv), root / command.directory) != 0:
            failed_checks.append(command.label)
    return failed_checks


def check_project(root: Path) -> None:
    """Runs each check, then fails listing those that failed."""
    failed_checks = run_checks(root)
    if failed_checks:
        raise KilnError(f"failed checks: {', '.join(failed_checks)}")
    ui.success("All checks pass.")
