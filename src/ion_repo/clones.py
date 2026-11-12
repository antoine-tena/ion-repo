"""`ion repo clones`: the duplicated code the branch brought, each beside the original to reuse.

jscpd (MIT, Rust engine, run by uvx) scans the whole repo in a second or two and compares it
with the commit where the branch left the integration branch: only the clones absent there are
shown, renamed copies included (`--ignore-identifiers`). Found without Claude, judged by it:
reuse the original, adapt it to serve both, or keep the copy. A report, never a failure: the
merge goes on whatever it finds.

Lockfiles, migrations and JSON data are left out; a repo's own `.jscpd.json` adds its `ignore`
patterns to those (jscpd's command line would replace them).
"""

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ion_score import ui

from ion_repo.check import branch_base, changed_files
from ion_repo.shell import KilnError, require_tools

JSCPD = "jscpd==5.4.3"
CONFIG = ".jscpd.json"
REPORT = "jscpd-report.json"
IGNORED = (
    "**/pnpm-lock.yaml",
    "**/package-lock.json",
    "**/yarn.lock",
    "**/bun.lock",
    "**/uv.lock",
    "**/poetry.lock",
    "**/Pipfile.lock",
    "**/Cargo.lock",
    "**/composer.lock",
    "**/Gemfile.lock",
    "**/go.sum",
    "**/migrations/**",
    "**/*.json",
)


@dataclass(frozen=True)
class Clone:
    copy: str
    original: str
    is_renamed: bool

    def line(self) -> str:
        return f"{self.copy} ← {self.original}{' (renamed)' if self.is_renamed else ''}"


def clones(root: Path, base: str | None = None) -> None:
    """Shows the branch's new clones, one line each: the copy, then the original."""
    found = new_clones(root, base)
    if not found:
        ui.success("No new duplicated code since the integration branch.")
        return
    blocks = "block" if len(found) == 1 else "blocks"
    ui.note(f"{len(found)} new duplicated {blocks}: reuse the original, adapt it, or keep the copy")
    for clone in found:
        print(clone.line())


def new_clones(root: Path, base: str | None = None) -> list[Clone]:
    """The clones absent from `base` (default: where the branch left the integration branch),
    the side the branch changed first."""
    require_tools("uv")
    base = base or branch_base(root)
    with tempfile.TemporaryDirectory(prefix="ion-repo-clones-") as output:
        command = [
            "uvx",
            "--from",
            JSCPD,
            "jscpd",
            ".",
            "--baseline-from-ref",
            base,
            "--ignore-identifiers",
            "--ignore",
            ",".join(ignored(root)),
            "--reporters",
            "json",
            "--output",
            output,
            "--no-colors",
        ]
        completed = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
        report = Path(output) / REPORT
        if completed.returncode != 0 or not report.is_file():
            raise KilnError(f"jscpd failed: {completed.stderr.strip() or completed.stdout.strip()}")
        duplicates = json.loads(report.read_text(encoding="utf-8"))["duplicates"]
    changed = set(changed_files(root))
    return [_oriented(duplicate, changed) for duplicate in duplicates if duplicate["isNew"]]


def ignored(root: Path) -> list[str]:
    """The default patterns, then the repo's own from `.jscpd.json`."""
    config = root / CONFIG
    own: list[str] = []
    if config.is_file():
        try:
            own = list(json.loads(config.read_text(encoding="utf-8")).get("ignore", []))
        except (json.JSONDecodeError, AttributeError) as error:
            raise KilnError(f"{CONFIG}: {error}") from error
    return [*IGNORED, *(pattern for pattern in own if pattern not in IGNORED)]


def _oriented(duplicate: dict[str, Any], changed: set[str]) -> Clone:
    first, second = (_place(duplicate[side]) for side in ("firstFile", "secondFile"))
    if duplicate["secondFile"]["name"] in changed and duplicate["firstFile"]["name"] not in changed:
        first, second = second, first
    return Clone(first, second, duplicate.get("kind") == "renamed")


def _place(side: dict[str, Any]) -> str:
    return f"{side['name']}:{side['start']}-{side['end']}"
