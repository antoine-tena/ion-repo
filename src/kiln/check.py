"""`kiln check`: runs the stack's checks and the charter, without stopping at the first failure;
the test suites only with `--tests` (a merge skips them, the release runs them all).

A Django backend's tests run as in the CI when `ci.yml` has its Django job: against that job's
throwaway PostgreSQL and Redis, with its variables (`env`), as `kiln ci` replays them; never
against the machine's `.env`, which may lack what the CI gives, nor a test database another
session shares. Without such a job, they get the databases of the compose file.
"""

import os
from pathlib import Path

import yaml

from kiln import ui
from kiln.charter import config as charter_config
from kiln.ci.execution import base_env
from kiln.ci.jobs import RELAYS, Plan, plan_job
from kiln.ci.services import running_services
from kiln.ci.workflow import CI_WORKFLOW, load_jobs
from kiln.dev.backing import start_backing_services
from kiln.install import ensure_env_file, moved_from, pnpm_behind, sync_command
from kiln.shell import KilnError, run, run_status, step
from kiln.stack import BACKEND_DIR, Command, Stack, load_stack


def run_checks(root: Path, with_tests: bool = False) -> list[str]:
    """Runs each check and returns the labels of those that failed; the test suites only
    `with_tests`, the release runs them all."""
    failed_checks: list[str] = []
    stack = load_stack(root)
    # A worktree has no backend/.env (ignored by git): without it, Django does not start.
    if stack.has_api and not (root / BACKEND_DIR / ".env").exists():
        ensure_env_file(root / BACKEND_DIR)
    # Nor node_modules, or older ones than the lockfile (uv run syncs Python by itself).
    if stack.pnpm_dir is not None and pnpm_behind(root / stack.pnpm_dir):
        step(f"{stack.pnpm_dir}: pnpm dependencies, as the lockfile says")
        run(["pnpm", "install", "--frozen-lockfile"], root / stack.pnpm_dir)
    # A repo moved since its venv was created: the tools' scripts call the old folder's Python.
    for directory in stack.python_dirs:
        if moved_from(root / directory / ".venv") is not None:
            step(f"{directory}: venv moved, packages reinstalled")
            run(sync_command(root / directory / ".venv"), root / directory)
    for command in _check_commands(root, stack, with_tests):
        step(f"Check: {command.label}")
        if _run_check(root, command) != 0:
            failed_checks.append(command.label)
    return failed_checks


def _run_check(root: Path, command: Command) -> int:
    is_tests = command.label == f"{command.directory} pytest"
    plan = _ci_django_job(root, command.directory) if is_tests else None
    if plan is None or plan.services is None:
        return run_status(list(command.argv), root / command.directory)
    images = ", ".join(image for image in (plan.services.postgres, plan.services.redis) if image)
    ui.note(f"as the CI job {plan.job.name}: {images}, its variables")
    try:
        with running_services(plan.services, f"kiln-check-{os.getpid()}") as urls:
            env = base_env({**plan.env, **urls})
            return run_status(list(command.argv), root / command.directory, env)
    except KilnError as error:
        print(error)
        return 1


def _ci_django_job(root: Path, directory: str) -> Plan | None:
    """The plan of the `ci.yml` job that tests `directory` with kiln's Django workflow."""
    if not (root / CI_WORKFLOW).exists():
        return None
    try:
        jobs = load_jobs(root)
    except KilnError, yaml.YAMLError:
        return None
    for job in jobs:
        if job.is_replayable and RELAYS.get(job.kind, job.kind) == "django":
            plan = plan_job(job)
            if directory in plan.python_dirs:
                return plan
    return None


def _check_commands(root: Path, stack: Stack, with_tests: bool = False) -> list[Command]:
    """The stack's checks; mypy as the CI types, through `charter types`, when the charter
    declares its packages and environment (`[types]`): a bare `mypy .` knows neither."""
    types = charter_config.load(root).get("types")
    typed_directory = types.get("directory", BACKEND_DIR) if isinstance(types, dict) else None
    return [
        Command(command.label, ".", ("charter", "types"))
        if command.label == f"{typed_directory} mypy"
        else command
        for command in stack.check_commands(with_tests)
    ]


def check_project(root: Path, with_tests: bool = False) -> None:
    """Runs each check, then fails listing those that failed; the tests get their databases."""
    start_backing_services(root)
    failed_checks = run_checks(root, with_tests)
    if failed_checks:
        raise KilnError(f"failed checks: {', '.join(failed_checks)}")
    ui.success("All checks pass.")
