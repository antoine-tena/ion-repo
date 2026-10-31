"""Verdict of `ion repo ci`, kept as a git note on the commit (`refs/notes/ci`) and pushed to
origin.

The first line is authoritative: `kiln ci: success` or `kiln ci: failure`. It is the one
`scripts/ops/lib/green-ci.sh` reads before allowing a deployment (the French wording of kiln 0.3,
`kiln ci : succès`, is still read). The next lines say when, where, how long, and above all which
jobs of `ci.yml` were not replayed.
"""

import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ion_repo.shell import KilnError

NOTES_REF = "refs/notes/ci"
REMOTE_COPY_REF = "refs/notes/ci-origin"
SUCCESS_LINE = "kiln ci: success"
FAILURE_LINE = "kiln ci: failure"
# Written by kiln 0.3, still found on older commits.
LEGACY_SUCCESS_LINE = "kiln ci : succès"
SECONDS_PER_MINUTE = 60


@dataclass(frozen=True)
class JobOutcome:
    name: str
    is_success: bool
    failed_step: str = ""


@dataclass(frozen=True)
class Verdict:
    sha: str
    outcomes: tuple[JobOutcome, ...]
    skipped: tuple[tuple[str, str], ...]
    started_at: datetime
    duration_seconds: float

    @property
    def is_success(self) -> bool:
        return bool(self.outcomes) and all(outcome.is_success for outcome in self.outcomes)

    def render(self) -> str:
        minutes, seconds = divmod(round(self.duration_seconds), SECONDS_PER_MINUTE)
        lines = [
            SUCCESS_LINE if self.is_success else FAILURE_LINE,
            f"commit: {self.sha}",
            f"date: {self.started_at.isoformat(timespec='seconds')}",
            f"machine: {socket.gethostname()}",
            f"duration: {minutes} min {seconds:02d} s",
            "jobs replayed: " + ", ".join(_outcome_text(outcome) for outcome in self.outcomes),
        ]
        if self.skipped:
            skipped_text = ", ".join(f"{name} ({reason})" for name, reason in self.skipped)
            lines.append(f"not replayed: {skipped_text}")
        return "\n".join(lines) + "\n"


def _outcome_text(outcome: JobOutcome) -> str:
    if outcome.is_success:
        return f"{outcome.name} ok"
    return f"{outcome.name} FAILED ({outcome.failed_step})"


def record_verdict(root: Path, verdict: Verdict, should_push: bool) -> None:
    """Puts the note on the commit, after taking in origin's notes, then pushes it."""
    _merge_remote_notes(root)
    _git(root, "notes", f"--ref={NOTES_REF}", "add", "-f", "-m", verdict.render(), verdict.sha)
    if should_push:
        _git(root, "push", "-q", "origin", NOTES_REF)


def read_verdict(root: Path, sha: str) -> str | None:
    """The `ion repo ci` note on this commit, origin included; None if it was never replayed."""
    _merge_remote_notes(root)
    completed = subprocess.run(
        ["git", "notes", f"--ref={NOTES_REF}", "show", sha],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout if completed.returncode == 0 else None


def _merge_remote_notes(root: Path) -> None:
    """Takes in origin's notes; when a commit has one on both sides, the local one wins."""
    fetched = subprocess.run(
        ["git", "fetch", "-q", "origin", f"+{NOTES_REF}:{REMOTE_COPY_REF}"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if fetched.returncode == 0:
        _git(root, "notes", f"--ref={NOTES_REF}", "merge", "-q", "-s", "ours", REMOTE_COPY_REF)


def _git(root: Path, *arguments: str) -> None:
    completed = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True, check=False
    )
    if completed.returncode != 0:
        raise KilnError(f"`git {' '.join(arguments[:2])}` failed: {completed.stderr.strip()}")
