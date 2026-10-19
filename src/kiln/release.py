"""`kiln version`: where kiln's releases stand, and what to ship next (kiln's own repo).

- **Number** (CLAUDE.md, Versions): in 0.x, each release bumps the patch, breaking ones
  included, like Claude Code; the minor only moves for a decided milestone
  (`kiln version --minor`). From 1.0, strict semver, like Next.js: breaking → major,
  `feat` → minor, the rest → patch.
- **Promotion**: a candidate (`vX.Y.Z-rc.N`, the last of its version) goes public when a
  candidate of a newer version exists and GitHub's CI of its commit is green: the next one
  ready, not a delay, avoids the emergency fix. The repos of the code folder tell who already
  took it.

Read only: `kiln version cut` and `kiln version promote` (shipping.py) tag and merge.
"""

import datetime
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from packaging.version import Version

from kiln import github_ci, ui
from kiln.config import load_config
from kiln.fleet import find_repos
from kiln.shell import KilnError, capture
from kiln.versions import release_version

BREAKING_SUBJECT = re.compile(r"^\w+(\([^)]*\))?!:")
FEATURE_SUBJECT = re.compile(r"^feat(\([^)]*\))?:")
INTEGRATION_REF = "origin/develop"
BACKLOG = Path("docs") / "backlog" / "backlog.md"
PLANNED_RELEASE = re.compile(r"^### v(\d+\.\d+\.\d+) · (.+)$")
VERSION_MODULE = Path("src") / "kiln" / "versions.py"


@dataclass(frozen=True)
class Tag:
    name: str
    version: Version
    created: datetime.datetime


def show_release_status(root: Path, *, milestone: bool = False) -> None:
    if not (root / VERSION_MODULE).is_file():
        raise KilnError("kiln version runs in the kiln repo")
    capture(["git", "fetch", "-q", "--tags", "origin"], root)
    tags = read_tags(root)
    public = [tag for tag in tags if not tag.version.is_prerelease]
    candidates = latest_candidates(tags)
    now = datetime.datetime.now(datetime.UTC)
    print(f"\n  {ui.paint('PUBLIC', ui.FIRE, bold=True)}")
    print(f"    {public[-1].name if public else ui.paint('none yet', ui.STONE)}")
    print(f"\n  {ui.paint('CANDIDATES', ui.FIRE, bold=True)}")
    if not candidates:
        print(f"    {ui.paint('none', ui.STONE)}")
    adopted = _adoption()
    for candidate in candidates:
        ci = github_ci.verdict(root, capture(["git", "rev-list", "-n", "1", candidate.name], root))
        verdict, ready = promotion_verdict(candidate, candidates, ci)
        mark = ui.paint("✓", ui.MOSS) if ready else ui.paint("·", ui.STONE)
        age = (now - candidate.created).days
        users = adopted.get(candidate.name, [])
        print(
            f"    {mark} {ui.paint(f'{candidate.name:<16}', bold=True)} {age} d  {verdict}"
            + (ui.paint(f"  · {', '.join(users)}", ui.STONE) if users else "")
        )
    last = tags[-1] if tags else None
    subjects = _subjects_since(root, last.name if last else None)
    baseline = last.version if last else _package_version(root)
    proposed = next_version(baseline, subjects, milestone=milestone)
    print(f"\n  {ui.paint('NEXT', ui.FIRE, bold=True)}")
    if subjects:
        detail = f"{len(subjects)} commits since {last.name}" if last else "first release"
        print(f"    v{proposed}-rc.1  {ui.paint(f'({detail})', ui.STONE)}")
        if Version(proposed).major == 0 and not milestone:
            print(f"    {ui.paint('a milestone? kiln version --minor', ui.STONE)}")
    else:
        print(f"    {ui.paint('nothing new on develop', ui.STONE)}")
    cut = {Version(tag.version.base_version) for tag in tags}
    plan = planned_release(root, cut)
    if plan:
        number, title, left = plan
        print(f"\n  {ui.paint('PLAN', ui.FIRE, bold=True)}  v{number} · {title}")
        for ticket in left:
            print(f"    {ui.paint('·', ui.STONE)} {ticket}")
        if not left:
            print(f"    {ui.paint('nothing left: kiln version cut', ui.MOSS)}")
    print()


def planned_release(root: Path, cut: set[Version]) -> tuple[str, str, list[str]] | None:
    """The first release of the backlog's `🚀 Releases` plan not cut yet: its number, its
    title and the tickets still listed under it (a closed ticket leaves the plan)."""
    backlog = root / BACKLOG
    if not backlog.is_file():
        return None
    section = backlog.read_text("utf-8").split("\n## 🚀 Releases\n", 1)
    if len(section) < 2:
        return None
    current: tuple[str, str, list[str]] | None = None
    for line in section[1].split("\n## ", 1)[0].splitlines():
        if match := PLANNED_RELEASE.match(line):
            if current:
                return current
            if Version(match.group(1)) not in cut:
                current = (match.group(1), match.group(2), [])
        elif current and line.startswith("- T-"):
            current[2].append(line.removeprefix("- "))
    return current


def read_tags(root: Path) -> list[Tag]:
    """Release tags of the repo, oldest first."""
    listing = capture(
        ["git", "tag", "-l", "v*", "--format=%(refname:short) %(creatordate:iso-strict)"], root
    )
    tags = []
    for line in listing.splitlines():
        name, _, created = line.partition(" ")
        version = release_version(name)
        if version is not None and created:
            tags.append(Tag(name, version, datetime.datetime.fromisoformat(created)))
    return sorted(tags, key=lambda tag: tag.version)


def latest_candidates(tags: list[Tag]) -> list[Tag]:
    """Last candidate of each version not yet promoted."""
    promoted = {tag.version for tag in tags if not tag.version.is_prerelease}
    latest: dict[Version, Tag] = {}
    for tag in tags:
        if tag.version.is_prerelease:
            final = Version(tag.version.base_version)
            if final not in promoted:
                latest[final] = tag
    return [latest[final] for final in sorted(latest)]


def promotion_verdict(candidate: Tag, candidates: list[Tag], ci: str) -> tuple[str, bool]:
    """Ready when a newer candidate exists and GitHub's CI of this one is green (`ci`, from
    `github_ci.verdict`)."""
    if ci != github_ci.SUCCESS:
        return f"CI not green ({ci}): not promotable", False
    if not any(other.version > candidate.version for other in candidates):
        return "waiting for a next release ready", False
    return f"ready: promote to v{candidate.version.base_version}", True


def next_version(last: Version, subjects: list[str], *, milestone: bool = False) -> str:
    """Number of the next release, from the commits since `last` (the last release, or the
    `pyproject.toml` version before the first). In 0.x, the next patch, except for a milestone
    (`milestone`); from 1.0, strict semver."""
    # A candidate counts as its version: its own fixes go to `-rc.N+1` on its branch, what
    # comes from develop prepares the release after.
    major, minor, patch = Version(last.base_version).release[:3]
    is_breaking = any(BREAKING_SUBJECT.match(s) or "BREAKING CHANGE" in s for s in subjects)
    has_feature = any(FEATURE_SUBJECT.match(s) for s in subjects)
    if major == 0:
        return f"0.{minor + 1}.0" if milestone else f"0.{minor}.{patch + 1}"
    if is_breaking:
        return f"{major + 1}.0.0"
    return f"{major}.{minor + 1}.0" if has_feature else f"{major}.{minor}.{patch + 1}"


def _package_version(root: Path) -> Version:
    """Version of `pyproject.toml`, the starting point while no release is tagged; the first
    one is breaking by principle (nothing precedes it publicly)."""
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    return Version(str(project["version"]))


def _subjects_since(root: Path, tag: str | None) -> list[str]:
    if tag is None:
        # Before the first release, everything is new: it counts as breaking.
        return ["feat!: first release"]
    log = capture(
        ["git", "log", "--no-merges", "--format=%s%n%b%x00", f"{tag}..{INTEGRATION_REF}"], root
    )
    return [entry.strip() for entry in log.split("\x00") if entry.strip()]


def _adoption() -> dict[str, list[str]]:
    """Template version of each repo of the code folder: who took which candidate."""
    code_dir = load_config().code_dir
    adopted: dict[str, list[str]] = {}
    if not code_dir.is_dir():
        return adopted
    for repo in find_repos(code_dir):
        adopted.setdefault(repo.template_commit, []).append(repo.root.name)
    return adopted
