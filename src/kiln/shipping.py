"""`kiln version cut` and `kiln version promote`: kiln's release in two commands (kiln's repo).

- **cut**, first run: branch `release/vX.Y.Z` from `origin/develop` in its own worktree, the
  `CHANGELOG.md` entry drafted from the commits since the last tag (breaking first), the number
  in `pyproject.toml` and `uv.lock`, the patch of each plugin changed since the last tag. The
  draft carries a marker: someone reads and rewrites it before anything is tagged.
- **cut**, next runs: the full checks on the branch, the branch pushed, GitHub's CI of its
  commit awaited (macOS and the end-to-end tests run only there), then tag `-rc.N` (the next N)
  pushed, only on green; a fix of the candidate is a `fix:` commit on the branch, then `cut`
  again.
- **promote**: a candidate whose CI is green, tag `vX.Y.Z` on its exact commit (its message is
  the changelog entry), merged into `main` and back into `develop`, pushed; `pypi.yml` publishes
  the package and the GitHub Release. `kiln update --all` stays a separate step, with consent.
"""

import datetime
import json
import os
import re
from collections.abc import Callable
from pathlib import Path

from packaging.version import Version

from kiln import github_ci, ui
from kiln.backlog import AFTER_UPDATING
from kiln.release import (
    VERSION_MODULE,
    Tag,
    _subjects_since,
    latest_candidates,
    next_version,
    promotion_verdict,
    read_tags,
)
from kiln.shell import KilnError, capture, run

CHANGELOG = "CHANGELOG.md"
DRAFT_MARKER = "<!-- draft: rewrite for users, breaking changes first, then delete this line -->"
ENTRY_HEADING = re.compile(r"^## v(\S+) — ", re.MULTILINE)
SUBJECT = re.compile(r"^(?P<type>\w+)(?:\([^)]*\))?(?P<bang>!)?:\s*(?P<text>.+)$")
# Commit types a user notices; the rest (docs, tests, chores) stays out of the notes.
VISIBLE_TYPES = {"feat", "fix", "perf"}
# A line of a commit's body that asks each repo for an action after `kiln update`.
AFTER_UPDATING_TRAILER = "After updating:"
LOCK = ["uv", "lock", "-q"]
CHECKS = (
    ["uv", "run", "pytest", "-q"],
    ["uv", "run", "ruff", "check"],
    ["uv", "run", "ruff", "format", "--check"],
)


def main_tree(root: Path) -> Path:
    """The main working tree, wherever the command runs (a worktree included)."""
    common = capture(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], root)
    return Path(common).parent


def release_worktree(root: Path, version: str) -> Path:
    return main_tree(root) / ".claude" / "worktrees" / f"release-v{version}"


def _require_kiln_repo(root: Path) -> None:
    if not (root / VERSION_MODULE).is_file():
        raise KilnError("kiln version runs in the kiln repo")
    capture(["git", "fetch", "-q", "--tags", "origin"], root)


def _open_release(root: Path, tags: list[Tag]) -> str | None:
    """Version of a `release/vX.Y.Z` branch not promoted yet: the release being cut."""
    promoted = {str(tag.version) for tag in tags if not tag.version.is_prerelease}
    branches = capture(["git", "branch", "--list", "release/v*", "--format=%(refname:short)"], root)
    open_versions = [
        name.removeprefix("release/v")
        for name in branches.split()
        if name.removeprefix("release/v") not in promoted
    ]
    return max(open_versions, key=Version) if open_versions else None


# --- cut ---------------------------------------------------------------------------------------


def cut(root: Path, *, milestone: bool = False) -> None:
    """Tags the open release when it has new commits (its draft rewritten, or a fix), otherwise
    starts the next one: a release whose last commit is already a candidate is done here."""
    _require_kiln_repo(root)
    tags = read_tags(root)
    version = _open_release(root, tags)
    if version is not None and not _is_candidate(root, version, tags):
        _tag_candidate(root, version, tags)
    else:
        _start_release(root, tags, milestone=milestone)


def _is_candidate(root: Path, version: str, tags: list[Tag]) -> bool:
    head = _commit_of(root, f"release/v{version}")
    return any(
        tag.version.is_prerelease
        and tag.version.base_version == version
        and _commit_of(root, tag.name) == head
        for tag in tags
    )


def _start_release(root: Path, tags: list[Tag], *, milestone: bool) -> None:
    last = tags[-1] if tags else None
    subjects = _subjects_since(root, last.name if last else None)
    if last and not subjects:
        raise KilnError(f"nothing new on develop since {last.name}")
    baseline = last.version if last else Version("0.0.0")
    version = next_version(baseline, subjects, milestone=milestone)
    tree = release_worktree(root, version)
    ui.step(f"Branch release/v{version}")
    branch = f"release/v{version}"
    run(["git", "worktree", "add", "-q", "-b", branch, str(tree), "origin/develop"], root)
    ui.step("Changelog draft and numbers")
    changelog = tree / CHANGELOG
    entry = draft_entry(version, subjects, today=_today())
    changelog.write_text(insert_entry(changelog.read_text("utf-8"), entry), "utf-8")
    bump_package(tree / "pyproject.toml", version)
    bumped = bump_changed_plugins(tree, last.name if last else None)
    run(LOCK, tree)
    run(["git", "add", "-A"], tree)
    run(["git", "commit", "-q", "-m", f"chore(release): v{version}, changelog and number"], tree)
    ui.success(f"release/v{version} cut in {tree}")
    if bumped:
        ui.note("plugins bumped: " + ", ".join(bumped))
    ui.note(
        f"next: rewrite the v{version} entry of {CHANGELOG} there (delete the draft line), "
        "commit, then `kiln version cut` again: checks, then tag -rc.1."
    )


def draft_entry(version: str, subjects: list[str], *, today: str) -> str:
    """`## vX.Y.Z — date`, then one line per visible commit, breaking ones first, then what each
    repo must do after updating (an `After updating: …` line in a commit's body)."""
    breaking, others, after_updating = [], [], []
    for subject in subjects:
        title, _, body = subject.partition("\n")
        after_updating += [
            AFTER_UPDATING + line.strip().removeprefix(AFTER_UPDATING_TRAILER).strip()
            for line in body.splitlines()
            if line.strip().startswith(AFTER_UPDATING_TRAILER)
        ]
        match = SUBJECT.match(title.strip())
        if match is None:
            continue
        text = match["text"].strip()
        text = text[:1].upper() + text[1:]
        if match["bang"] or "BREAKING CHANGE" in body:
            breaking.append(f"- **Breaking**: {text}")
        elif match["type"] in VISIBLE_TYPES:
            others.append(f"- {text}")
    lines = [*breaking, *others] or ["- Maintenance."]
    lines += after_updating
    return "\n".join([f"## v{version} — {today}", DRAFT_MARKER, *lines]) + "\n"


def insert_entry(changelog: str, entry: str) -> str:
    """The entry above the most recent one (after the file's header)."""
    first = ENTRY_HEADING.search(changelog)
    if first is None:
        return changelog.rstrip("\n") + "\n\n" + entry
    return changelog[: first.start()] + entry + "\n" + changelog[first.start() :]


def bump_package(pyproject: Path, version: str) -> None:
    text = pyproject.read_text("utf-8")
    pattern = r'^version = "[^"]*"'
    bumped, count = re.subn(pattern, f'version = "{version}"', text, count=1, flags=re.M)
    if not count:
        raise KilnError(f"no `version = ...` line in {pyproject}")
    pyproject.write_text(bumped, "utf-8")


def bump_changed_plugins(tree: Path, since: str | None) -> list[str]:
    """Patch of each plugin with a change since `since`: Claude Code only reinstalls a plugin
    whose version moved."""
    bumped = []
    for manifest in sorted(tree.glob("plugins/*/.claude-plugin/plugin.json")):
        plugin = manifest.parents[1]
        if since is not None:
            relative = str(plugin.relative_to(tree))
            changed = capture(["git", "diff", "--name-only", since, "HEAD", "--", relative], tree)
            # Unchanged, or its number already moved since: nothing to bump.
            if not changed or str(manifest.relative_to(tree)) in changed.splitlines():
                continue
        data = json.loads(manifest.read_text("utf-8"))
        if "version" not in data:
            continue
        major, minor, patch = Version(data["version"]).release[:3]
        data["version"] = f"{major}.{minor}.{patch + 1}"
        manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")
        bumped.append(f"{plugin.name} {data['version']}")
    return bumped


def _tag_candidate(root: Path, version: str, tags: list[Tag]) -> None:
    tree = release_worktree(root, version)
    if not tree.is_dir():
        raise KilnError(
            f"release/v{version} has no worktree: git worktree add {tree} release/v{version}"
        )
    if capture(["git", "status", "--porcelain"], tree):
        raise KilnError(f"uncommitted changes in {tree}: commit them first")
    if DRAFT_MARKER in (tree / CHANGELOG).read_text("utf-8"):
        raise KilnError(f"the v{version} entry of {CHANGELOG} is still a draft ({tree})")
    # A fix of a candidate that touches a plugin moves its number: Claude Code only reinstalls
    # a plugin whose version moved, the machines would keep the candidate's old hooks.
    previous = _last_candidate(version, tags)
    if previous is not None:
        bumped = bump_changed_plugins(tree, previous)
        if bumped:
            run(["git", "add", "-A", "plugins"], tree)
            run(["git", "commit", "-q", "-m", "chore(release): plugins of the fix bumped"], tree)
            ui.note("plugins bumped: " + ", ".join(bumped))
    # The release worktree has its own environment, not the one `uv run kiln` may have set.
    env = {key: value for key, value in os.environ.items() if key != "VIRTUAL_ENV"}
    for check in CHECKS:
        ui.step(" ".join(check[2:]))
        run(check, tree, env)
    # The tag waits for GitHub's verdict on the exact commit it will name.
    branch = f"release/v{version}"
    run(["git", "push", "-q", "origin", branch], tree)
    ui.step(f"GitHub CI of {branch} (macOS, end-to-end tests)")
    github_ci.wait_until_green(tree, capture(["git", "rev-parse", "HEAD"], tree), branch)
    rank = 1 + max(
        (
            tag.version.pre[1]
            for tag in tags
            if tag.version.pre and tag.version.base_version == version
        ),
        default=0,
    )
    name = f"v{version}-rc.{rank}"
    ui.step(f"Tag {name}")
    run(["git", "tag", "-a", name, "-m", f"Release candidate {name}"], tree)
    run(["git", "push", "-q", "origin", f"release/v{version}", name], tree)
    ui.success(f"{name} pushed: the internal channel follows it (kiln update --all, with consent)")


def _last_candidate(version: str, tags: list[Tag]) -> str | None:
    """The latest `-rc.N` of `version` already tagged, if any."""
    candidates = [
        tag for tag in tags if tag.version.is_prerelease and tag.version.base_version == version
    ]
    return max(candidates, key=lambda tag: tag.version).name if candidates else None


# --- promote -----------------------------------------------------------------------------------


def promote(root: Path, wanted: str | None = None) -> None:
    _require_kiln_repo(root)
    tags = read_tags(root)
    candidate = pick_candidate(
        latest_candidates(tags),
        wanted,
        lambda tag: github_ci.verdict(root, _commit_of(root, tag.name)),
    )
    version = candidate.version.base_version
    commit = _commit_of(root, candidate.name)
    package = capture(["git", "show", f"{commit}:pyproject.toml"], root)
    if f'version = "{version}"' not in package:
        raise KilnError(f"{candidate.name}: pyproject.toml does not say {version}")
    tree = main_tree(root)
    if capture(["git", "branch", "--show-current"], tree) != "develop":
        raise KilnError(f"the main tree ({tree}) must be on develop")
    if capture(["git", "status", "--porcelain", "--untracked-files=no"], tree):
        raise KilnError(f"uncommitted changes in {tree}")
    name = f"v{version}"
    entry = changelog_entry(capture(["git", "show", f"{commit}:{CHANGELOG}"], root), version)
    ui.step(f"Tag {name} on {candidate.name}")
    run(["git", "tag", "-a", name, commit, "-m", f"Release {name}", "-m", entry], root)
    _merge_into_main(root, name, entry)
    ui.step("Back into develop")
    run(["git", "pull", "-q", "--ff-only", "origin", "develop"], tree)
    run(["git", "merge", "-q", "--no-ff", name, "-m", f"Merge tag '{name}' into develop"], tree)
    run(["git", "push", "-q", "origin", "develop"], tree)
    _remove_release_branch(root, version)
    ui.success(f"{name} promoted: pypi.yml publishes kiln-cli and the GitHub Release")
    ui.note("then, with consent: kiln update --all")


def pick_candidate(candidates: list[Tag], wanted: str | None, ci_of: Callable[[Tag], str]) -> Tag:
    """The candidate asked for, or the oldest one ready; never one a newer candidate does not
    cover yet, nor one whose CI (`ci_of`, GitHub's verdict) is not green."""
    if wanted is not None:
        version = Version(wanted.removeprefix("v"))
        chosen = [tag for tag in candidates if Version(tag.version.base_version) == version]
        if not chosen:
            raise KilnError(f"no candidate of v{version} waiting for promotion")
        candidate = chosen[0]
        verdict, ready = promotion_verdict(candidate, candidates, ci_of(candidate))
        if not ready:
            raise KilnError(f"{candidate.name}: {verdict}")
        return candidate
    for candidate in candidates:
        if promotion_verdict(candidate, candidates, ci_of(candidate))[1]:
            return candidate
    raise KilnError(
        "no candidate ready: a newer candidate has to exist first (kiln version cut), and the CI "
        "of the one to promote must be green (kiln version)"
    )


def changelog_entry(changelog: str, version: str) -> str:
    """The body of the `## vX.Y.Z — date` entry, without its heading."""
    headings = list(ENTRY_HEADING.finditer(changelog))
    for index, heading in enumerate(headings):
        if heading.group(1) == version:
            end = headings[index + 1].start() if index + 1 < len(headings) else len(changelog)
            body = changelog[heading.end() : end].split("\n", 1)
            return body[1].strip() if len(body) > 1 else ""
    raise KilnError(f"no v{version} entry in {CHANGELOG}")


def _merge_into_main(root: Path, name: str, entry: str) -> None:
    tree = main_tree(root) / ".claude" / "worktrees" / "main"
    ui.step("Into main")
    run(["git", "worktree", "add", "-q", "-B", "main", str(tree), "origin/main"], root)
    try:
        summary = entry.splitlines()[0].removeprefix("- ")[:60] if entry else ""
        message = f"Version {name}" + (f": {summary}" if summary else "")
        run(["git", "merge", "-q", "--no-ff", name, "-m", message], tree)
        run(["git", "push", "-q", "origin", "main", name], tree)
    finally:
        run(["git", "worktree", "remove", "--force", str(tree)], root)


def _remove_release_branch(root: Path, version: str) -> None:
    branch = f"release/v{version}"
    if not capture(["git", "branch", "--list", branch], root):
        return
    tree = release_worktree(root, version)
    if tree.is_dir():
        run(["git", "worktree", "remove", str(tree)], root)
    try:
        run(["git", "branch", "-d", branch], root)
    except KilnError:
        ui.note(f"{branch} has commits after its last candidate: kept")
        return
    run(["git", "push", "-q", "origin", "--delete", branch], root)


def _commit_of(root: Path, ref: str) -> str:
    return capture(["git", "rev-list", "-n", "1", ref], root)


def _today() -> str:
    return datetime.date.today().isoformat()
