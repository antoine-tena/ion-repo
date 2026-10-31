"""GitHub's verdict on a commit of kiln: a candidate is tagged, and promoted, only on green.

The checks of the machine (pytest, ruff) leave out what only GitHub runs: macOS and the
end-to-end tests of release branches. A candidate was once cut over a red end-to-end run
(v0.4.0-rc.1): `kiln version cut` now waits for that run, and `kiln version` and `promote` read
its verdict.
"""

import json
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from ion_repo.shell import KilnError

WORKFLOW = "kiln.yml"
SUCCESS = "success"
# A run appears a few seconds after the push; beyond that, something is wrong.
APPEAR_TIMEOUT = 180
POLL_SECONDS = 10
GH_TIMEOUT = 20


@dataclass(frozen=True)
class CiRun:
    run_id: int
    status: str  # queued, in_progress, completed
    conclusion: str  # success, failure, cancelled… ("" while running)
    url: str

    @property
    def verdict(self) -> str:
        """`success`, `failure`…, or `running`."""
        return self.conclusion if self.status == "completed" else "running"


def latest_run(root: Path, commit: str) -> CiRun | None:
    """The latest run of kiln's workflow on `commit`; None when there is none (or no gh)."""
    if shutil.which("gh") is None:
        return None
    fields = "databaseId,status,conclusion,url"
    try:
        listed = subprocess.run(
            ["gh", "run", "list", "--workflow", WORKFLOW, "--commit", commit, "--limit", "1",
             "--json", fields],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT,
            check=False,
        )  # fmt: skip
        runs = json.loads(listed.stdout) if listed.returncode == 0 else []
    except subprocess.TimeoutExpired, OSError, ValueError:
        return None
    if not runs:
        return None
    found = runs[0]
    return CiRun(
        int(found["databaseId"]), str(found["status"]), str(found["conclusion"]), str(found["url"])
    )


def verdict(root: Path, commit: str) -> str:
    """`success`, `failure`…, `running`, or `none` (never run, or GitHub out of reach)."""
    found = latest_run(root, commit)
    return found.verdict if found else "none"


def wait_until_green(root: Path, commit: str, what: str) -> str:
    """Waits for the run of kiln's workflow on `commit`, shown live; its URL when green, a
    `KilnError` otherwise."""
    if shutil.which("gh") is None:
        raise KilnError(f"gh is needed to wait for the CI of {what}: https://cli.github.com")
    deadline = time.monotonic() + APPEAR_TIMEOUT
    found = latest_run(root, commit)
    while found is None and time.monotonic() < deadline:
        time.sleep(POLL_SECONDS)
        found = latest_run(root, commit)
    if found is None:
        raise KilnError(f"no CI run of {WORKFLOW} on {commit[:7]} ({what}) after the push")
    if found.status != "completed":
        subprocess.run(
            ["gh", "run", "watch", str(found.run_id), "--interval", "30", "--compact"],
            cwd=root,
            check=False,
        )
        found = latest_run(root, commit) or found
    if found.verdict != SUCCESS:
        raise KilnError(
            f"the CI of {what} is not green ({found.verdict}): {found.url}. Fix it on the branch, "
            "commit, then run the same command again"
        )
    return found.url
