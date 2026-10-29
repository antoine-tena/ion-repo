"""Frozen files: the `file = "…"` waivers of `kiln-waivers.toml`. `kiln update` and `kiln set`
no longer touch them; but a frozen file must not drift silently, hence the report of what kiln
changed in them between two versions."""

import difflib
import tempfile
from pathlib import Path

import copier
from copier.errors import CopierError
from packaging.version import Version

from kiln import renames, ui
from kiln.charter.waivers import WAIVERS_FILE, load
from kiln.stack import read_answers
from kiln.versions import release_version

DIFF_LINES = 40
# First release whose template speaks English (answer keys included).
ENGLISH_TEMPLATE = Version("0.4.0")
# First release whose sizes are plain words (`small`, not `ember`), its candidates included.
PLAIN_SIZES = Version("0.4.10rc1")


def frozen_files(root: Path) -> list[str]:
    """Files frozen by an active waiver (an expired waiver freezes nothing)."""
    return [waiver.file for waiver in load(root).actives if waiver.file]


def report_frozen_drift(root: Path, source: str, previous: str, current: str) -> None:
    """What kiln changed, from `previous` to `current`, in the files the repo froze."""
    frozen = frozen_files(root)
    if not frozen or not previous or previous == current:
        return
    answers = {k: v for k, v in read_answers(root).items() if not k.startswith("_")}
    try:
        with tempfile.TemporaryDirectory() as tmp:
            before = _render(source, previous, answers_for(previous, answers), Path(tmp) / "before")
            after = _render(source, current, answers_for(current, answers), Path(tmp) / "after")
            diffs = {f: _diff(before / f, after / f, f) for f in frozen}
    except (CopierError, OSError) as error:  # OSError: revision not found (git)
        ui.note(f"Frozen files: cannot compare the versions of kiln ({error}).")
        return
    changed = {f: d for f, d in diffs.items() if d}
    if not changed:
        return
    ui.panel(
        f"kiln changed frozen files ({WAIVERS_FILE}): {previous} → {current}",
        [f"- {f}" for f in changed]
        + ["Carry over what fits, or lift the waiver to take the template again."],
    )
    for diff in changed.values():
        print("\n".join(diff[:DIFF_LINES]))
        if len(diff) > DIFF_LINES:
            print(f"… and {len(diff) - DIFF_LINES} more line(s)")


def answers_for(ref: str, answers: dict[str, object]) -> dict[str, object]:
    """The answers as the template at `ref` names them: French before kiln 0.4.0, the sizes
    after the fire before 0.4.10."""
    version = release_version(ref)
    if version is not None and version < ENGLISH_TEMPLATE:
        return renames.legacy_answers(answers)
    if version is not None and version < PLAIN_SIZES:
        return renames.fire_size(answers)
    return answers


def _render(source: str, ref: str, answers: dict[str, object], destination: Path) -> Path:
    copier.run_copy(
        source,
        destination,
        data=answers,
        vcs_ref=ref,
        defaults=True,
        quiet=True,
        unsafe=False,
    )
    return destination


def _diff(before: Path, after: Path, name: str) -> list[str]:
    old, new = (p.read_text().splitlines() if p.exists() else [] for p in (before, after))
    return list(
        difflib.unified_diff(old, new, f"kiln {name} (before)", f"kiln {name} (after)", lineterm="")
    )
