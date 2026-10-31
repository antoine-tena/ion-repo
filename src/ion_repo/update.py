"""`ion repo update`: brings in the changes of the template, then updates the dependencies."""

import datetime
import re
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

import copier
from copier.errors import UserMessageError
from plumbum import ProcessExecutionError

from ion_repo import migrations, ui
from ion_repo.backlog import add_after_update_ticket, migrate_legacy_backlog, split_backlog
from ion_repo.check import check_project
from ion_repo.contract import generate_api_contract
from ion_repo.deps import lock_dependencies, sync_dependencies, update_dependencies
from ion_repo.frozen import frozen_files, report_frozen_drift
from ion_repo.grid.fix import convert_in_place
from ion_repo.ion_names import convert_ion_names
from ion_repo.rules import write_unverified_rules
from ion_repo.shell import (
    KilnError,
    capture,
    quiet_git,
    require_clean_tree,
    require_tools,
    run,
    step,
)
from ion_repo.stack import ANSWERS_FILE, kept_of, load_stack, read_answers
from ion_repo.template import DEFAULT_TEMPLATE_SOURCE, template_revision
from ion_repo.versions import (
    follows_candidates,
    latest_release,
    notes_between,
    read_changelog,
    release_version,
    tag_of,
    tool_release_tag,
    upgrade_command,
)

PROTECTED_BRANCHES = ("main", "master", "develop")
UPDATE_BRANCH = "chore/ion-repo-update"
# Start of a conflict left by Copier (`git merge-file`).
CONFLICT_MARKER = "<<<<<<< before updating"
# A reusable workflow of ion-repo cited at a tag: `antoine-tena/ion-repo/….yml@v0.3.1` (`kiln/`
# before the Ion family).
# `…/charter.yml@v0.4.1`, or `…/charter.yml@<sha> # v0.4.1` once pinned: the tag is in the comment.
ION_REPO_WORKFLOW_REF = re.compile(
    r"(antoine-tena/(?:ion-repo|kiln)/\S+?)@(\S+)(?:[ \t]+#[ \t]*(\S+))?"
)
# Former addresses of the template (init-repo, renamed kiln, renamed ion-repo): GitHub redirects,
# still replaced.
LEGACY_TEMPLATE_SOURCES = (
    "https://github.com/antoine-tena/init-repo.git",
    "https://github.com/antoine-tena/kiln.git",
)


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
    if is_adopted(root):
        from ion_repo.adopted import update_adopted

        update_adopted(root)
        ui.note(
            "adopted before kiln 0.4.6: ion repo adopt lays the rest of the template, "
            "then ion repo update serves it in full"
        )
        if should_check:
            check_project(root)
        return
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
        if conflicted := conflicted_files(root):
            # What follows reads these files (pnpm-workspace.yaml, pyproject.toml): stopped here.
            ui.note(
                f"conflicts left by the template in {', '.join(conflicted)}: resolve them "
                "(both sides often hold), commit, then ion repo update --no-template for the "
                "dependencies (it needs a clean tree)"
            )
            report_changes(root)
            return
    stack = load_stack(root)
    if should_update_deps:
        update_dependencies(root, stack, allow_major=allow_major)
    elif should_update_template:
        lock_dependencies(root, stack)
        sync_dependencies(root, stack)
    generate_api_contract(root, stack)
    write_unverified_rules(root, stack)
    if should_update_template:
        # What the template leaves to the repo (SHAs, digests, a lock): closed like ion repo fix.
        convert_in_place(root, [*frozen_files(root), *kept_of(root)])
    report_changes(root)
    if should_check:
        check_project(root)


def check_tool_not_older(root: Path) -> None:
    """Refuses to take a repo back to a version of ion-repo older than the one it comes from
    (updated by a teammate with a newer ion-repo): the tool must be upgraded first."""
    if _template_source(root) != DEFAULT_TEMPLATE_SOURCE:
        return
    project_ref = template_commit(root)
    tool_tag = tool_release_tag()
    project, tool = release_version(project_ref), release_version(tool_tag or "")
    if project is not None and tool is not None and project > tool:
        raise KilnError(
            f"this repo follows ion-repo {project_ref}, newer than the installed tool "
            f"({tool_tag}): "
            f"{upgrade_command(tag_of(project_ref) or project_ref)}"
        )


def mention_newer_release() -> None:
    """A version of ion-repo newer than the tool is out: say so, with the command."""
    tool = release_version(tool_release_tag() or "")
    latest = latest_release()
    newer = release_version(latest or "")
    if tool is not None and newer is not None and newer > tool and latest is not None:
        ui.note(f"ion-repo {latest} is out: {upgrade_command(latest)}, then ion repo update.")


def is_adopted(root: Path) -> bool:
    """Brought under ion-repo by `ion repo adopt`: a charter, no Copier answers to replay."""
    return not (root / ANSWERS_FILE).exists() and any(
        (root / name).is_file() for name in ("charter.toml", "charte.toml")
    )


def apply_template(root: Path, answers: Mapping[str, object] | None = None) -> None:
    """Template applied again (latest revision, answers possibly changed), without overwriting
    local changes: conflicts are marked in the files. Frozen files (`kiln-waivers.toml`) and
    what an adopted repo keeps as its own (`kept`) are left as they are."""
    previous_answers = migrations.raw_answers(root)
    try:
        with quiet_git():
            copier.run_update(
                root,
                # Under today's names: a project of kiln 0.3 wrote its answers in French.
                data=migrations.answers_for_update(root, answers or {}),
                vcs_ref=template_revision(_template_source(root)),
                use_prereleases=follows_candidates(),
                exclude=[*frozen_files(root), *kept_of(root)],
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
    for converted in convert_ion_names(root):
        ui.note(f"ion-repo: {converted}.")
    resolve_kiln_ref_conflicts(root)
    replace_legacy_source(root)
    if migrate_legacy_backlog(root):
        ui.note("Tracking moved from docs/a-faire/ to docs/backlog/ (T-NN tickets, in English).")
        split_backlog(root, from_disk=True)
    elif split_backlog(root):
        ui.note("Closed tickets moved from docs/backlog/backlog.md to docs/backlog/done.md.")


def resolve_kiln_ref_conflicts(root: Path) -> None:
    """Conflicts born of the `@<tag>` of ion-repo's workflows alone: merged again without it.

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
        project_refs, rendered_refs = _kiln_refs(ours), _kiln_refs(base)
        project_spellings, rendered_spellings = _kiln_spellings(ours), _kiln_spellings(base)
        if len(project_spellings) != 1 or len(rendered_spellings) != 1:
            continue
        if project_spellings == rendered_spellings or len(project_refs) != 1:
            continue
        # The tag also appears outside the `uses:` (header comment of ci.yml): it is replaced
        # everywhere, without touching a longer tag that extends it.
        rendered_tag = re.escape(rendered_refs.pop())
        aligned_base = re.sub(rf"{rendered_tag}(?![\w.-])", project_refs.pop(), base)
        # Pinned by ion repo fix (`@<sha> # v0.4.1`): the old render takes the pin, the new render
        # wins the merge, and the update's converters pin it again.
        aligned_base = ION_REPO_WORKFLOW_REF.sub(rf"\g<1>@{project_spellings.pop()}", aligned_base)
        merged = _merge_cleanly(aligned_base, ours, theirs)
        if merged is not None:
            (root / name).write_text(merged)
            # No more conflict in the index: a change of the template like any other.
            run(["git", "reset", "-q", "--", name], root)


def _kiln_refs(text: str) -> set[str]:
    return {match.group(3) or match.group(2) for match in ION_REPO_WORKFLOW_REF.finditer(text)}


def _kiln_spellings(text: str) -> set[str]:
    """What follows the `@` of ion-repo's workflows: `v0.4.1`, or `<sha> # v0.4.1` once pinned."""
    return {
        match.group(0)[len(match.group(1)) + 1 :] for match in ION_REPO_WORKFLOW_REF.finditer(text)
    }


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
    """Frame with what is new in each version passed, from ion-repo's changelog; what the repo must
    do after updating becomes a ticket of its backlog."""
    notes = notes_between(previous, current, read_changelog())
    if not notes:
        return
    lines: list[str] = []
    for release in notes:
        lines += [f"{release.tag}  {release.date}".rstrip(), *release.lines, ""]
    ui.panel(f"What's new in ion-repo: {previous or '?'} → {current}", lines[:-1])
    if ticket := add_after_update_ticket(root, notes, today=datetime.date.today().isoformat()):
        ui.note(f"to do right after this update: {ticket} in docs/backlog/backlog.md")


def check_working_branch(root: Path, work_branch: str = UPDATE_BRANCH) -> None:
    require_under_kiln(root)
    require_clean_tree(root)
    leave_protected_branch(root, work_branch)


def require_under_kiln(root: Path) -> None:
    if not (root / ANSWERS_FILE).exists() and not is_adopted(root):
        raise KilnError(
            f"no {ANSWERS_FILE} nor charter: this repo is not under ion-repo (ion repo adopt "
            f"brings it)"
        )


def leave_protected_branch(root: Path, work_branch: str) -> None:
    """On `main`, `master` or `develop`, the work branch is opened in place (clean tree checked
    first): ion-repo never writes on an integration branch, and the user has nothing to type."""
    current = capture(["git", "branch", "--show-current"], root)
    if current not in PROTECTED_BRANCHES:
        return
    branch = work_branch
    if _branch_exists(root, branch):
        branch = f"{work_branch}-{datetime.date.today().isoformat()}"
    if _branch_exists(root, branch):
        raise KilnError(f"on {current}: {work_branch} and {branch} exist, merge or delete them")
    run(["git", "switch", "-q", "-c", branch], root)
    ui.note(f"on {current}: work branch {branch} opened, to merge into {current} once reviewed")


def _branch_exists(root: Path, branch: str) -> bool:
    command = ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"]
    return subprocess.run(command, cwd=root, capture_output=True, check=False).returncode == 0


def report_changes(root: Path) -> None:
    step("Changed files")
    run(["git", "status", "--short"], root, live=True)
    print()
    ui.note(
        "Review the diff (conflicts marked <<<<<<<), commit, then merge into develop "
        "(skill /repo:merge)."
    )


def replace_legacy_source(root: Path) -> None:
    answers_path = root / ANSWERS_FILE
    text = answers_path.read_text()
    for legacy_source in LEGACY_TEMPLATE_SOURCES:
        text = text.replace(f"_src_path: {legacy_source}", f"_src_path: {DEFAULT_TEMPLATE_SOURCE}")
    answers_path.write_text(text)
