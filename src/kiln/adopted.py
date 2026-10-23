"""An adopted repo's references to kiln's reusable workflows, moved to the last public release.

A repo adopted by `kiln adopt` has no Copier answers: `kiln update` cannot replay a template
there. What it does take from kiln is its reusable workflows, quoted at a tag
(`antoine-tena/kiln/.github/workflows/charter.yml@v0.4.0`) so that what lands on `develop`
never reaches it before a release (antoine, 19 October 2026, T-04). `kiln update` moves those
references, and nothing else, to the latest public release, once each input the repo passes
(`with:`) is checked against the workflow it will call; a removed input stops it, untouched.
"""

import re
import urllib.request
from collections.abc import Callable
from pathlib import Path

import yaml  # brought by copier

from kiln import ui
from kiln.adopted_names import convert_legacy_names, remaining_mentions, ticket_mentions
from kiln.backlog import BACKLOG_DIR, LEGACY_DIR, migrate_legacy_backlog
from kiln.grid.fixers import resolve
from kiln.shell import KilnError, step
from kiln.versions import latest_release

WORKFLOW_DIR = Path(".github") / "workflows"
# `uses: antoine-tena/kiln/.github/workflows/charter.yml@v0.4.0`, a comment after it kept; or
# pinned, `…/charter.yml@<sha> # v0.4.0` ([PINNED-ACTIONS]), where the comment holds the tag.
KILN_USES = re.compile(
    r"(?P<lead>uses:\s*['\"]?)(?P<path>antoine-tena/kiln/(?P<file>\S+?))@(?P<ref>[^\s'\"#]+)"
    r"(?P<close>['\"]?)(?P<comment>[ \t]+#[ \t]*(?P<tag>\S+).*)?"
)
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
RAW_URL = "https://raw.githubusercontent.com/antoine-tena/kiln/{ref}/{file}"
FETCH_TIMEOUT = 10

Fetch = Callable[[str, str], str]  # (ref, path in kiln) -> the file's text
Resolve = Callable[[str], str]  # tag -> its commit SHA


def _quoted(match: re.Match[str]) -> str:
    """The release a reference quotes: its tag, read in the comment when pinned by SHA."""
    return match["tag"] if FULL_SHA.match(match["ref"]) and match["tag"] else match["ref"]


def quoted_refs(root: Path) -> set[str]:
    """The refs at which the repo's workflows quote kiln's: one when all agree."""
    return {
        _quoted(match)
        for path in _workflow_files(root)
        for match in KILN_USES.finditer(path.read_text(encoding="utf-8"))
    }


def move_to_release(
    root: Path, tag: str | None = None, fetch: Fetch | None = None, resolve: Resolve | None = None
) -> list[str]:
    """Every reference to kiln's workflows moved to `tag` (by default the latest public
    release), in the form the repo chose: a tag stays a tag, a SHA becomes the tag's SHA with
    the tag in its comment; returns the files changed. Refused, nothing written, when an input
    the repo passes does not exist in the workflow at that tag."""
    tag = tag or latest_release(candidates=False)
    if tag is None:
        raise KilnError("kiln's public releases are out of reach (network): run again later")
    fetch = fetch or _fetch
    texts = {path: path.read_text(encoding="utf-8") for path in _workflow_files(root)}
    problems = [
        problem
        for path, text in texts.items()
        for problem in _input_problems(path.relative_to(root), text, tag, fetch)
    ]
    if problems:
        raise KilnError(
            f"kiln's workflows at {tag} no longer take what this repo passes, nothing moved:\n  "
            + "\n  ".join(problems)
        )
    resolve = resolve or _commit_of

    def moved_ref(match: re.Match[str]) -> str:
        if FULL_SHA.match(match["ref"]):
            return f"{match['lead']}{match['path']}@{resolve(tag)}{match['close']} # {tag}"
        return f"{match['lead']}{match['path']}@{tag}{match['close']}{match['comment'] or ''}"

    changed = []
    for path, text in texts.items():
        moved = KILN_USES.sub(moved_ref, text)
        if moved != text:
            path.write_text(moved, encoding="utf-8")
            changed.append(str(path.relative_to(root)))
    return changed


def update_adopted(root: Path) -> None:
    """`kiln update` in an adopted repo: its names of kiln 0.3 converted, then the workflows' tag
    moved."""
    converted = convert_legacy_names(root)
    if converted:
        step("Adopted repo: kiln's names of 0.3 moved to today's")
        for line in converted:
            ui.success(line)
        mentions = remaining_mentions(root)
        if mentions:
            ui.note(f"still cited in the repo's own text, to reread: {', '.join(mentions)}")
    if (root / LEGACY_DIR / "a-faire.md").is_file():
        _move_legacy_backlog(root)
    step("Adopted repo: kiln's workflows moved to the last public release")
    before = quoted_refs(root)
    changed = move_to_release(root)
    if not changed:
        ui.success(f"already at {', '.join(sorted(before)) or 'no kiln workflow'}")
        return
    after = quoted_refs(root)
    ui.success(f"{', '.join(sorted(before))} → {', '.join(sorted(after))}: {', '.join(changed)}")


def _move_legacy_backlog(root: Path) -> None:
    """`docs/a-faire/` to kiln's `docs/backlog/`, as `kiln update` does in a generated repo: the
    template's backlog laid down first, then the tickets converted (`AF-NN` → `T-NN`)."""
    from kiln.adopt import copy_backlog  # kiln.adopt imports this module

    step("Adopted repo: docs/a-faire/ becomes docs/backlog/ (skill /kiln:backlog)")
    if not (root / BACKLOG_DIR).exists():
        copy_backlog(root, None)
    migrate_legacy_backlog(root)
    ui.success("tickets AF-NN are T-NN now, same numbers")
    cited = ticket_mentions(root)
    if cited:
        ui.note(f"still cited as AF-NN in {len(cited)} files, to rename: {', '.join(cited[:5])}…")


def _workflow_files(root: Path) -> list[Path]:
    folder = root / WORKFLOW_DIR
    return sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")]) if folder.is_dir() else []


def _input_problems(where: Path, text: str, tag: str, fetch: Fetch) -> list[str]:
    try:
        workflow = yaml.safe_load(text) or {}
    except yaml.YAMLError as error:
        return [f"{where}: unreadable ({error})"]
    found = []
    for job_name, job in (workflow.get("jobs") or {}).items():
        uses = str(job.get("uses", "")) if isinstance(job, dict) else ""
        match = KILN_USES.search(f"uses: {uses}")
        if match is None:
            continue
        passed = set((job.get("with") or {}).keys())
        accepted = _accepted_inputs(fetch(tag, match.group("file")))
        found += [
            f"{where}, job {job_name}: input `{name}` unknown to {match.group('file')}@{tag}"
            for name in sorted(passed - accepted)
        ]
    return found


def _accepted_inputs(workflow_text: str) -> set[str]:
    workflow = yaml.safe_load(workflow_text) or {}
    # PyYAML reads the `on` key as the boolean True.
    triggers = workflow.get(True) or workflow.get("on") or {}
    call = triggers.get("workflow_call") or {} if isinstance(triggers, dict) else {}
    return set((call.get("inputs") or {}).keys())


def _fetch(ref: str, file: str) -> str:
    url = RAW_URL.format(ref=ref, file=file)
    try:
        with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT) as response:
            return str(response.read().decode("utf-8"))
    except OSError as error:
        raise KilnError(f"{file} at {ref} unreachable ({error}): run again later") from error


def _commit_of(tag: str) -> str:
    return resolve.commit_of("antoine-tena/kiln", tag)
