"""`ion repo update --rehearse`: the update played on a throwaway clone, the repo left untouched.

Measured on a copy first, never in the repo itself: annway's update to v0.4.0-rc.1 failed on a
copy in two minutes (ion-repo#T-147), where it would have failed halfway through the real one. The
clone takes the repo's last commit and its ignored `.env*` files; the update runs there with
its checks, and only the outcome comes back: files changed, conflicts, failure. A clone that
failed is kept for a look; a repo not under ion-repo is refused before any clone.
"""

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from ion_repo import ui
from ion_repo.shell import KilnError, capture, run, step
from ion_repo.update import conflicted_files, require_under_kiln, update_project

REHEARSAL_BRANCH = "chore/ion-repo-update-rehearsal"
# The local files ignored by git that the checks may need, as `prepare-worktree.sh` copies them.
ENV_PATTERNS = ("*.env", "*.env.*", ".env", ".env.*")


@dataclass(frozen=True)
class Rehearsal:
    succeeded: bool
    summary: str  # one line: what the real update would do, or why it fails


def rehearse(root: Path, *, should_update_deps: bool, allow_major: bool) -> Rehearsal:
    """The update of `root` played on a clone of its last commit, with the checks."""
    require_under_kiln(root)  # before the clone: nothing to rehearse, nothing left in /tmp
    directory = Path(tempfile.mkdtemp(prefix=f"kiln-rehearsal-{root.name}-"))
    clone = directory / root.name
    run(["git", "clone", "-q", "--no-local", str(root), str(clone)], directory)
    head = capture(["git", "rev-parse", "HEAD"], root)
    run(["git", "switch", "-q", "-c", REHEARSAL_BRANCH, head], clone)
    for name in _ignored_env_files(root):
        (clone / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, clone / name)
    try:
        update_project(
            clone,
            should_update_template=True,
            should_update_deps=should_update_deps,
            allow_major=allow_major,
        )
    except KilnError as error:
        return Rehearsal(False, f"the update fails: {error} (clone kept in {clone})")
    conflicted = conflicted_files(clone)
    if conflicted:
        return Rehearsal(False, f"conflicts to resolve: {', '.join(conflicted)} (clone {clone})")
    changed = _changed_files(clone)
    shutil.rmtree(directory, ignore_errors=True)
    if not changed:
        return Rehearsal(True, "already up to date")
    return Rehearsal(True, f"updates cleanly: {len(changed)} files changed, checks green")


def rehearse_project(root: Path, *, should_update_deps: bool, allow_major: bool) -> None:
    step(f"Rehearsal of the update of {root.name}, on a clone")
    outcome = rehearse(root, should_update_deps=should_update_deps, allow_major=allow_major)
    if not outcome.succeeded:
        raise KilnError(f"rehearsal: {outcome.summary}")
    ui.success(f"rehearsal: {outcome.summary}; the repo itself is untouched")


def _changed_files(clone: Path) -> list[str]:
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True, check=True
    )
    return [line[3:] for line in status.stdout.splitlines() if line.strip()]


def _ignored_env_files(root: Path) -> list[str]:
    listed = capture(
        ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "--", *ENV_PATTERNS],
        root,
    )
    return [
        name
        for name in listed.splitlines()
        if "node_modules/" not in name
        and not name.startswith(".claude/worktrees/")
        and not name.endswith((".example", ".sample"))
    ]
