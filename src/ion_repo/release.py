"""`ion repo version`: where ion-repo's releases stand, and what to ship next (ion-repo's own repo).

- **Number** (CLAUDE.md, Versions): in 0.x, each release bumps the patch, breaking ones
  included, like Claude Code; the minor only moves for a decided milestone
  (`ion repo version --minor`). From 1.0, strict semver, like Next.js: breaking → major,
  `feat` → minor, the rest → patch.
- **Promotion**: a candidate (`vX.Y.Z-rc.N`, the last of its version) goes public once it has
  proved itself, on facts: GitHub's CI of its commit green, then a day of soak since its tag and
  at least one repo of the code folder updated to it (`ion repo update` runs that repo's checks).
  A candidate of fixes only (no `feat`, nothing breaking since the last public release) takes
  the short lane: two hours, no repo required. The soak restarts at each `-rc.N`.

Read only: `ion repo version cut` and `ion repo version promote` (shipping.py) tag and merge.
"""

import datetime
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from packaging.version import Version

from ion_repo import github_ci, ui
from ion_repo.config import load_config
from ion_repo.fleet import find_repos
from ion_repo.shell import KilnError, capture
from ion_repo.versions import release_version

BREAKING_SUBJECT = re.compile(r"^\w+(\([^)]*\))?!:")
FEATURE_SUBJECT = re.compile(r"^feat(\([^)]*\))?:")
FIX_ONLY_SUBJECT = re.compile(r"^(fix|docs|test|chore|ci|build|style)(\([^)]*\))?:")
INTEGRATION_REF = "origin/develop"
SOAK = datetime.timedelta(hours=24)
FIX_SOAK = datetime.timedelta(hours=2)
BACKLOG = Path("docs") / "backlog" / "backlog.md"
PLANNED_TICKET = re.compile(r"- (?:[a-z][a-z0-9-]*#)?T-\d+")
PLANNED_RELEASE = re.compile(r"^### v(\d+\.\d+\.\d+) · (.+)$")
VERSION_MODULE = Path("src") / "ion_repo" / "versions.py"


@dataclass(frozen=True)
class Tag:
    name: str
    version: Version
    created: datetime.datetime


@dataclass(frozen=True)
class Evidence:
    """What a candidate has proved: GitHub's CI of its commit (`github_ci.verdict`), the repos
    of the code folder updated to it, and whether it holds fixes only."""

    ci: str
    users: tuple[str, ...] = ()
    is_fixes_only: bool = False


def show_release_status(root: Path, *, milestone: bool = False) -> None:
    if not (root / VERSION_MODULE).is_file():
        raise KilnError("ion repo version runs in the ion-repo repo")
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
        found = evidence(root, candidate, tags, adopted)
        verdict, ready = promotion_verdict(candidate, found, now)
        mark = ui.paint("✓", ui.MOSS) if ready else ui.paint("·", ui.STONE)
        age = (now - candidate.created).days
        users = found.users
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
            print(f"    {ui.paint('a milestone? ion repo version --minor', ui.STONE)}")
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
            print(f"    {ui.paint('nothing left: ion repo version cut', ui.MOSS)}")
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
        elif current and PLANNED_TICKET.match(line):
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


def promotion_verdict(
    candidate: Tag, found: Evidence, now: datetime.datetime, is_urgent: bool = False
) -> tuple[str, bool]:
    """Ready when its CI is green, its soak is over and, unless it holds fixes only, a repo of
    the code folder runs it; an urgent promotion (decided by the owner) only needs the CI."""
    if found.ci != github_ci.SUCCESS:
        return f"CI not green ({found.ci}): not promotable", False
    if is_urgent:
        return f"urgent: promote to v{candidate.version.base_version}", True
    left = candidate.created + (FIX_SOAK if found.is_fixes_only else SOAK) - now
    if left > datetime.timedelta(0):
        lane = "fixes only, " if found.is_fixes_only else ""
        return f"soaking ({lane}{_hours(left)} left)", False
    if not found.users and not found.is_fixes_only:
        return "soaked, but no repo runs it yet: ion repo update --all", False
    return f"ready: promote to v{candidate.version.base_version}", True


def evidence(
    root: Path, candidate: Tag, tags: list[Tag], adopted: dict[str, list[str]]
) -> Evidence:
    """What `candidate` has proved, read from GitHub, the code folder and its commits."""
    commit = capture(["git", "rev-list", "-n", "1", candidate.name], root)
    public = [
        tag for tag in tags if not tag.version.is_prerelease and tag.version < candidate.version
    ]
    since = f"{public[-1].name}..{candidate.name}" if public else candidate.name
    log = capture(["git", "log", "--no-merges", "--format=%s%n%b%x00", since], root)
    subjects = [entry.strip() for entry in log.split("\x00") if entry.strip()]
    return Evidence(
        github_ci.verdict(root, commit),
        tuple(adopted.get(candidate.name, [])),
        is_fixes_only(subjects),
    )


def is_fixes_only(subjects: list[str]) -> bool:
    """Commits that fix without adding or breaking anything (`fix`, `docs`, `chore`…)."""
    return bool(subjects) and all(
        FIX_ONLY_SUBJECT.match(subject) and "BREAKING CHANGE" not in subject for subject in subjects
    )


def _hours(left: datetime.timedelta) -> str:
    hours = max(1, round(left.total_seconds() / 3600))
    return f"{hours} h"


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
