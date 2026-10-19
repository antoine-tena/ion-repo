"""`kiln ci`: replays a commit's CI on this machine and keeps the verdict on the commit.

For a repo whose GitHub CI does not run (minutes used up, repo without Actions): the commit is
checked out in a detached worktree, outside the repo, its dependencies installed as on GitHub
(frozen locks), then the jobs of `ci.yml` replayed. The verdict goes as a git note to origin,
where the deployment script reads it. The worktree of a killed `kiln ci` (SIGKILL, closed window)
keeps its launcher's PID file, and the next run removes it.
"""

import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from kiln.ci.execution import Workspace, base_env, run_lanes, run_step, say
from kiln.ci.jobs import Plan, Step, plan_job
from kiln.ci.services import is_alive, remove_orphan_containers
from kiln.ci.verdict import (
    LEGACY_SUCCESS_LINE,
    SUCCESS_LINE,
    JobOutcome,
    Verdict,
    read_verdict,
    record_verdict,
)
from kiln.ci.workflow import load_jobs
from kiln.shell import KilnError, capture, require_tools

CACHE_DIR = Path.home() / ".cache" / "kiln" / "ci"
SHORT_SHA = 12
PREPARATION = "setup"


def run_local_ci(
    root: Path, revision: str, skipped_jobs: frozenset[str], should_push: bool, should_keep: bool
) -> Verdict:
    require_tools("git", "uv", "podman")
    if orphan_count := remove_orphan_containers():
        say(f"{orphan_count} containers of an interrupted kiln ci removed")
    if orphan_count := _remove_orphan_workspaces(root):
        say(f"{orphan_count} worktrees of an interrupted kiln ci removed")
    sha = capture(["git", "rev-parse", "--verify", f"{revision}^{{commit}}"], root)
    started_at, started = datetime.now().astimezone(), time.monotonic()
    workspace = _create_workspace(root, sha)
    try:
        jobs = load_jobs(workspace.root)
        replayed = [job for job in jobs if job.is_replayable and job.name not in skipped_jobs]
        plans = [plan_job(job) for job in replayed]
        skipped = [(job.name, job.reason) for job in jobs if not job.is_replayable]
        skipped += [(name, "left out by --skip") for name in sorted(skipped_jobs)]
        say(f"kiln ci {sha[:SHORT_SHA]}: {len(plans)} jobs replayed, {len(skipped)} not replayed")
        outcomes = _prepare(plans, workspace) or run_lanes(plans, workspace)
    finally:
        _owner_file(workspace.root).unlink(missing_ok=True)
        if not should_keep:
            _remove_workspace(root, workspace.root)
    verdict = Verdict(sha, tuple(outcomes), tuple(skipped), started_at, time.monotonic() - started)
    record_verdict(root, verdict, should_push)
    return verdict


def show_verdict(root: Path, revision: str) -> bool:
    """Shows the commit's `kiln ci` note; true if it says success."""
    sha = capture(["git", "rev-parse", "--verify", f"{revision}^{{commit}}"], root)
    note = read_verdict(root, sha)
    if note is None:
        print(f"{sha[:SHORT_SHA]} was never replayed by kiln ci (kiln ci {revision}).")
        return False
    print(note, end="")
    return note.startswith((SUCCESS_LINE, LEGACY_SUCCESS_LINE))


def _create_workspace(root: Path, sha: str) -> Workspace:
    name = f"{_repo_name(root)}-{sha[:SHORT_SHA]}"
    worktree, log_dir = CACHE_DIR / name, CACHE_DIR / "logs" / name
    _remove_workspace(root, worktree)
    shutil.rmtree(log_dir, ignore_errors=True)
    log_dir.mkdir(parents=True)
    capture(["git", "worktree", "add", "--detach", str(worktree), sha], root)
    _owner_file(worktree).write_text(str(os.getpid()))
    return Workspace(worktree, log_dir, f"kiln-ci-{name}")


def _repo_name(root: Path) -> str:
    # Name of the main tree, even when run from a worktree: the status line looks it up so.
    common_dir = capture(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], root)
    return Path(common_dir).parent.name


def _owner_file(worktree: Path) -> Path:
    """PID of the `kiln ci` using the worktree, next to it; gone once the run is over."""
    return worktree.with_name(f"{worktree.name}.pid")


def _remove_orphan_workspaces(root: Path) -> int:
    """Removes the repo's worktrees whose launching `kiln ci` is dead; returns their number.

    A worktree without a PID file (kept by --keep) is never touched.
    """
    orphans = [
        owner.with_suffix("")
        for owner in CACHE_DIR.glob(f"{_repo_name(root)}-*.pid")
        if not owner.read_text().strip().isdigit() or not is_alive(int(owner.read_text()))
    ]
    for worktree in orphans:
        _remove_workspace(root, worktree)
        _owner_file(worktree).unlink(missing_ok=True)
    return len(orphans)


def _remove_workspace(root: Path, worktree: Path) -> None:
    if worktree.exists():
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(worktree)],
            cwd=root,
            capture_output=True,
            check=False,
        )
        shutil.rmtree(worktree, ignore_errors=True)
    subprocess.run(["git", "worktree", "prune"], cwd=root, capture_output=True, check=False)


def _prepare(plans: list[Plan], workspace: Workspace) -> list[JobOutcome]:
    """Installs the dependencies once for all jobs; a failed outcome, otherwise nothing."""
    python_dirs = sorted({directory for plan in plans for directory in plan.python_dirs})
    pnpm_dirs = sorted({directory for plan in plans for directory in plan.pnpm_dirs})
    steps = [Step(f"uv sync {path}", "uv sync --locked", path) for path in python_dirs]
    install = "pnpm install --frozen-lockfile"
    steps += [Step(f"pnpm install {path}", install, path) for path in pnpm_dirs]
    env = base_env({})
    log_path = workspace.log_dir / f"{PREPARATION}.log"
    for step in steps:
        if not run_step(step, workspace.root, env, log_path, PREPARATION):
            return [JobOutcome(PREPARATION, is_success=False, failed_step=step.label)]
    return []


def require_known_jobs(root: Path, names: frozenset[str]) -> None:
    known = {job.name for job in load_jobs(root)}
    unknown = sorted(names - known)
    if unknown:
        raise KilnError(f"unknown jobs in ci.yml: {', '.join(unknown)}")
