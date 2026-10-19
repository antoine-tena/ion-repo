"""`kiln update`: brings in the changes of the template, then updates the dependencies."""

import datetime
import re
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

import copier
from copier.errors import UserMessageError
from plumbum import ProcessExecutionError

from kiln import migrations, ui
from kiln.backlog import add_after_update_ticket, migrate_legacy_backlog
from kiln.check import check_project
from kiln.contract import generate_api_contract
from kiln.deps import lock_dependencies, sync_dependencies, update_dependencies
from kiln.frozen import frozen_files, report_frozen_drift
from kiln.rules import write_unverified_rules
from kiln.shell import KilnError, capture, require_tools, run, step
from kiln.stack import ANSWERS_FILE, load_stack, read_answers
from kiln.template import DEFAULT_TEMPLATE_SOURCE, template_revision
from kiln.versions import (
    follows_candidates,
    latest_release,
    notes_between,
    read_changelog,
    release_version,
    tag_of,
    tool_release_tag,
    upgrade_command,
)

PROTECTED_BRANCHES = ("main", "develop")
# Start of a conflict left by Copier (`git merge-file`).
CONFLICT_MARKER = "<<<<<<< before updating"
# A reusable workflow of kiln cited at a tag: `antoine-tena/kiln/….yml@v0.3.1`.
KILN_WORKFLOW_REF = re.compile(r"(antoine-tena/kiln/\S+?)@(\S+)")
# Former address of the template (init-repo, renamed kiln): GitHub redirects, still replaced.
LEGACY_TEMPLATE_SOURCES = ("https://github.com/antoine-tena/init-repo.git",)


def update_project(
    root: Path,
    *,
    should_update_template: bool,
    should_update_deps: bool,
    allow_major: bool,
    should_check: bool = True,
) -> None:
    require_tools("git", "uv")
    check_working_branch(root)
    if should_update_template:
        check_tool_not_older(root)
        previous = template_commit(root)
        # Said before anything is touched: the release the repo is about to follow, or why not.
        target = template_revision(_template_source(root))
        step(f"Architecture: changes of the template ({previous or '?'} → {target})")
        apply_template(root)
        show_release_notes(root, previous, template_commit(root))
        report_frozen_drift(root, _template_source(root), previous, template_commit(root))
        mention_newer_release()
    stack = load_stack(root)
    if should_update_deps:
        update_dependencies(root, stack, allow_major=allow_major)
    elif should_update_template:
        lock_dependencies(root, stack)
        sync_dependencies(root, stack)
    generate_api_contract(root, stack)
    write_unverified_rules(root, stack)
    report_changes(root)
    if should_check:
        check_project(root)


def check_tool_not_older(root: Path) -> None:
    """Refuses to take a repo back to a version of kiln older than the one it comes from
    (updated by a teammate with a newer kiln): the tool must be upgraded first."""
    if _template_source(root) != DEFAULT_TEMPLATE_SOURCE:
        return
    project_ref = template_commit(root)
    tool_tag = tool_release_tag()
    project, tool = release_version(project_ref), release_version(tool_tag or "")
    if project is not None and tool is not None and project > tool:
        raise KilnError(
            f"this repo follows kiln {project_ref}, newer than the installed tool ({tool_tag}): "
            f"{upgrade_command(tag_of(project_ref) or project_ref)}"
        )


def mention_newer_release() -> None:
    """A version of kiln newer than the tool is out: say so, with the command."""
    tool = release_version(tool_release_tag() or "")
    latest = latest_release()
    newer = release_version(latest or "")
    if tool is not None and newer is not None and newer > tool and latest is not None:
        ui.note(f"kiln {latest} is out: {upgrade_command(latest)}, then kiln update.")


def apply_template(root: Path, answers: Mapping[str, object] | None = None) -> None:
    """Template applied again (latest revision, answers possibly changed), without overwriting
    local changes: conflicts are marked in the files. Frozen files (`kiln-waivers.toml`) are
    left as they are."""
    previous_answers = migrations.raw_answers(root)
    try:
        copier.run_update(
            root,
            # Under today's names: a project of kiln 0.3 wrote its answers in French.
            data=migrations.answers_for_update(root, answers or {}),
            vcs_ref=template_revision(_template_source(root)),
            use_prereleases=follows_candidates(),
            exclude=frozen_files(root),
            defaults=True,
            skip_answered=True,
            overwrite=True,
            conflict="inline",
            unsafe=False,
        )
    except UserMessageError as error:
        raise KilnError(f"template update refused: {error}") from error
    except ProcessExecutionError as error:
        raise KilnError(git_failure(error)) from error
    # After Copier, which requires a clean tree and rewrites the answers file.
    source = _template_source(root)
    for converted in migrations.convert(root, previous_answers, source, template_revision(source)):
        ui.note(f"kiln 0.4: {converted}.")
    resolve_kiln_ref_conflicts(root)
    replace_legacy_source(root)
    if migrate_legacy_backlog(root):
        ui.note("Tracking moved from docs/a-faire/ to docs/backlog/ (T-NN tickets, in English).")


def resolve_kiln_ref_conflicts(root: Path) -> None:
    """Conflicts born of the `@<tag>` of kiln's workflows alone: merged again without it.

    A promoted tag sits on the commit of its last candidate (`v0.3.1` = `v0.3.1-rc.1`); Copier
    renders the old version under the name `git describe` gives it, the promoted one, and no
    longer finds the project's `@v0.3.1-rc.1`: a conflict at each promotion, with nothing to
    decide. Copier leaves the three versions in the index (1: old render, 2: project, 3: new
    render); the merge is redone with the old render at the project's tag, and kept if clean."""
    for name in conflicted_files(root):
        stages = [_index_stage(root, stage, name) for stage in (1, 2, 3)]
        if None in stages:
            continue
        base, ours, theirs = (str(text) for text in stages)
        project_refs = _kiln_refs(ours)
        rendered_refs = _kiln_refs(base)
        if len(project_refs) != 1 or len(rendered_refs) != 1 or project_refs == rendered_refs:
            continue
        # The tag also appears outside the `uses:` (header comment of ci.yml): it is replaced
        # everywhere, without touching a longer tag that extends it.
        rendered_tag = re.escape(rendered_refs.pop())
        aligned_base = re.sub(rf"{rendered_tag}(?![\w.-])", project_refs.pop(), base)
        merged = _merge_cleanly(aligned_base, ours, theirs)
        if merged is not None:
            (root / name).write_text(merged)
            # No more conflict in the index: a change of the template like any other.
            run(["git", "reset", "-q", "--", name], root)


def _kiln_refs(text: str) -> set[str]:
    return {match.group(2) for match in KILN_WORKFLOW_REF.finditer(text)}


def _index_stage(root: Path, stage: int, name: str) -> str | None:
    shown = subprocess.run(
        ["git", "show", f":{stage}:{name}"], cwd=root, capture_output=True, text=True, check=False
    )
    return shown.stdout if shown.returncode == 0 else None


def _merge_cleanly(base: str, ours: str, theirs: str) -> str | None:
    """Three-way merge by `git merge-file`, or None if it leaves a conflict."""
    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / name for name in ("ours", "base", "theirs")]
        for path, text in zip(paths, (ours, base, theirs), strict=True):
            path.write_text(text)
        merged = subprocess.run(
            ["git", "merge-file", "-p", *map(str, paths)],
            capture_output=True,
            text=True,
            check=False,
        )
    return merged.stdout if merged.returncode == 0 else None


def conflicted_files(root: Path) -> list[str]:
    """Files where Copier left a conflict to resolve by hand."""
    found = subprocess.run(
        ["git", "grep", "-l", "--untracked", CONFLICT_MARKER],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return found.stdout.split()


# What git writes when the network or GitHub does not answer.
UNREACHABLE_MARKERS = ("could not resolve host", "unable to access", "connection timed out")


def git_failure(error: ProcessExecutionError) -> str:
    """One line for a git run by Copier (tags, clone of the template) that failed."""
    stderr = str(error.stderr or "")
    if any(marker in stderr.lower() for marker in UNREACHABLE_MARKERS):
        return "GitHub unreachable: check the network, then run again"
    last_line = next((line for line in reversed(stderr.splitlines()) if line.strip()), "")
    return f"git failed while updating the template: {last_line.strip() or error}"


def _template_source(root: Path) -> str:
    source = str(read_answers(root).get("_src_path", ""))
    return DEFAULT_TEMPLATE_SOURCE if source in LEGACY_TEMPLATE_SOURCES else source


def template_commit(root: Path) -> str:
    """Revision of the template the repo comes from: `v3`, or a commit before the first release."""
    return str(read_answers(root).get("_commit", ""))


def show_release_notes(root: Path, previous: str, current: str) -> None:
    """Frame with what is new in each version passed, from kiln's changelog; what the repo must
    do after updating becomes a ticket of its backlog."""
    notes = notes_between(previous, current, read_changelog())
    if not notes:
        return
    lines: list[str] = []
    for release in notes:
        lines += [f"{release.tag}  {release.date}".rstrip(), *release.lines, ""]
    ui.panel(f"What's new in kiln: {previous or '?'} → {current}", lines[:-1])
    if ticket := add_after_update_ticket(root, notes, today=datetime.date.today().isoformat()):
        ui.note(f"to do right after this update: {ticket} in docs/backlog/backlog.md")


def check_working_branch(root: Path) -> None:
    if not (root / ANSWERS_FILE).exists():
        raise KilnError(f"no {ANSWERS_FILE}: this repo was not generated by kiln")
    branch = capture(["git", "branch", "--show-current"], root)
    if branch in PROTECTED_BRANCHES:
        raise KilnError(f"on {branch}: create a branch first (e.g. chore/kiln-update)")
    if capture(["git", "status", "--porcelain"], root):
        raise KilnError("working tree not clean: commit or set aside the changes")


def report_changes(root: Path) -> None:
    step("Changed files")
    run(["git", "status", "--short"], root, live=True)
    print()
    ui.note(
        "Review the diff (conflicts marked <<<<<<<), commit, then merge into develop "
        "(skill /kiln:merge)."
    )


def replace_legacy_source(root: Path) -> None:
    answers_path = root / ANSWERS_FILE
    text = answers_path.read_text()
    for legacy_source in LEGACY_TEMPLATE_SOURCES:
        text = text.replace(f"_src_path: {legacy_source}", f"_src_path: {DEFAULT_TEMPLATE_SOURCE}")
    answers_path.write_text(text)
