"""`kiln fix`: every gap a script can close, closed on a work branch, with proof.

Each commit is proven: the rule's detector runs again (`fixed` when it passes, `partial` when a
gap is left), the whole grid is compared before and after (a converter that turns another rule
red is undone), and the repo's checks judge it. A rule a converter brings into play (a CI that
now needs an audit) joins the run. Each commit says the points it won.

The converters run in a throwaway worktree from the last commit: the user's tree, and its
uncommitted changes, are never touched; only the branch `kiln/fix-<date>` remains.

The repo's own checks (`checks`) run before and after each converter: one that turns them red is
undone and reported, never left in a commit, its log kept for `kiln score --roadmap`. One commit
per rule, its message giving the why and the source. `--dry-run` shows the plan and the diff on a
throwaway worktree, the repo untouched.
"""

import datetime
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import yaml  # brought by copier

from ion_repo import ui
from ion_repo.grid import checks, detectors, score
from ion_repo.grid.facts import read_repo
from ion_repo.grid.fixers import FIXERS
from ion_repo.grid.model import Rule, load_rules
from ion_repo.shell import KilnError

UNVERIFIED = "unverified: no check found"
CLOSED = "closed by an earlier converter"
# Throwaway worktrees go to the cache folder: /tmp may be in memory, a big repo would fill it.
SCRATCH = Path.home() / ".cache" / "kiln" / "worktrees"
# Out of git but needed by the checks, at the root and one folder down: the installed Node
# dependencies (linked) and the local settings (copied). Python's are made by `uv run` itself.
LINKED = ("node_modules",)
COPIED = (".env", ".env.local")
# A commit of `kiln fix`: a branch holding only these is updated rather than doubled.
FIX_SUBJECT = re.compile(r"^fix\([A-Z0-9-]+\): ")


FIXED, PARTIAL, REVERTED, UNCHANGED = "fixed", "partial", "reverted", "unchanged"


@dataclass(frozen=True)
class Outcome:
    rule: str
    status: str  # fixed, partial (committed, a gap left), reverted, unchanged
    files: tuple[str, ...] = ()
    note: str = ""
    points: int | None = None  # what the commit added to the score


def git(root: Path, *arguments: str, check: bool = True) -> str:
    done = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True, check=False
    )
    if check and done.returncode != 0:
        raise KilnError(f"git {' '.join(arguments)}: {done.stderr.strip() or done.stdout.strip()}")
    return done.stdout


def plan(root: Path, only: str | None = None) -> list[Rule]:
    """The failing scored rules a converter can close, waived ones aside. A rule out of the
    score (the compressor's, `trial`) runs only when `only` names it: its converter finds its
    own gaps, and spends test runs to prove each one."""
    report = score.score_repo(root)
    failing = {found.rule for found in report.findings if found.status == score.FAILED}
    rules = [rule for rule in load_rules() if rule.id in failing and rule.fixer in FIXERS]
    if only is not None:
        wanted = only.upper()
        named = [rule for rule in load_rules() if rule.id == wanted]
        if not named:
            raise KilnError(f"no rule {only}: kiln grid lists them")
        if not named[0].is_scored and named[0].fixer in FIXERS:
            return named
        rules = [rule for rule in rules if rule.id == wanted]
    return rules


def fix(
    root: Path, *, dry_run: bool = False, only: str | None = None, on: str = ""
) -> list[Outcome]:
    """`on`: an existing branch the commits go on (kiln-bot's), left to its caller."""
    root = Path(git(root, "rev-parse", "--show-toplevel").strip())
    if git(root, "status", "--porcelain"):
        ui.note("From the last commit: uncommitted changes left out, and left as they are.")
    if dry_run:
        with scratch_worktree(root, "--detach") as copy:
            rules = _announce(copy, only)
            return _dry_run(copy, rules) if rules else []
    if on:
        with scratch_worktree(root, ref=on) as copy:
            rules = _announce(copy, only)
            return _run(copy, rules, on, False, widen=only is None) if rules else []
    branch, reused = _branch(root)
    with scratch_worktree(root, "-B" if reused else "-b", branch) as copy:
        rules = _announce(copy, only)
        outcomes = _run(copy, rules, branch, reused, widen=only is None) if rules else []
    if not git(root, "rev-list", f"HEAD..{branch}"):
        git(root, "branch", "-D", branch)
    return outcomes


def _announce(root: Path, only: str | None) -> list[Rule]:
    rules = plan(root, only)
    if not rules:
        ui.note("Nothing a script can close here: kiln score lists what is left for judgment.")
        return []
    ui.step(f"{len(rules)} rule(s) a script can close: {', '.join(rule.id for rule in rules)}")
    reaching = [rule.id for rule in rules if FIXERS[rule.fixer].network]
    if reaching:
        ui.note(f"Network needed (commit SHAs, image digests) for: {', '.join(reaching)}")
    return rules


def _run(root: Path, rules: list[Rule], branch: str, reused: bool, *, widen: bool) -> list[Outcome]:
    """`widen`: a rule a converter brings into play joins the run (not under `--rule`)."""
    report = score.score_repo(root)
    before = report.score
    found = checks.find(root)
    ui.step(f"{len(found)} check(s) of the repo, run once before the first converter")
    results = [checks.run(root, check) for check in found]
    judges = [result.check for result in results if result.ok]
    unusable = [result.reason for result in results if not result.ok]
    # Why the checks cannot judge the converters; empty when some can.
    if not found:
        unverified = UNVERIFIED
    elif not judges:
        unverified = f"unverified: {'; '.join(unusable)}"
    else:
        unverified = ""
    outcomes = []
    pending, tried = list(rules), {rule.id for rule in rules}
    while pending:
        rule = pending.pop(0)
        outcome, report = _apply(root, rule, judges, unverified, report, branch)
        outcomes.append(outcome)
        # A gap the converter brought into play (the audit a new CI needs): closed in this run.
        brought = [found for found in _fixable_gaps(report) if widen and found.id not in tried]
        pending += brought
        tried |= {found.id for found in brought}
    where = f"{branch} (updated from the last commit)" if reused else branch
    _summary(outcomes, before, report.score, where, unverified, unusable if judges else [])
    return outcomes


def _fixable_gaps(report: score.Report) -> list[Rule]:
    failing = {found.rule for found in report.findings if found.status == score.FAILED}
    return [rule for rule in load_rules() if rule.id in failing and rule.fixer in FIXERS]


def _branch(root: Path, base: str = "") -> tuple[str, bool]:
    """Today's branch (or `base`), and whether it is taken over: one holding only `kiln fix`
    commits, and checked out nowhere, starts again from the last commit (what kiln-bot updates);
    any other gets a suffix (`kiln/fix-2026-10-24-2`)."""
    base = base or f"kiln/fix-{datetime.date.today().isoformat()}"
    checked_out = {
        line.removeprefix("branch refs/heads/")
        for line in git(root, "worktree", "list", "--porcelain").splitlines()
        if line.startswith("branch ")
    }
    name, number = base, 1
    while git(root, "branch", "--list", name).strip():
        subjects = git(root, "log", "--format=%s", f"HEAD..{name}").splitlines()
        if name not in checked_out and all(FIX_SUBJECT.match(subject) for subject in subjects):
            return name, True
        number += 1
        name = f"{base}-{number}"
    return name, False


@contextmanager
def scratch_worktree(root: Path, *options: str, ref: str = "HEAD") -> Iterator[Path]:
    """A worktree of the last commit out of the user's tree (`options`: `--detach`, or `-b`
    and a branch), with what the checks need from the tree; removed afterwards, its branch kept."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="kiln-fix-", dir=SCRATCH))
    copy = scratch / "repo"
    try:
        git(root, "worktree", "add", "-q", *options, str(copy), ref)
        _bring_local_files(root, copy)
        yield copy
    finally:
        git(root, "worktree", "remove", "--force", str(copy), check=False)
        shutil.rmtree(scratch, ignore_errors=True)


def _bring_local_files(root: Path, copy: Path) -> None:
    folders = [Path("."), *(child.relative_to(root) for child in root.iterdir() if child.is_dir())]
    for folder in folders:
        if folder.name == ".git" or not (copy / folder).is_dir():
            continue
        for name in LINKED:
            if (root / folder / name).is_dir() and not (copy / folder / name).exists():
                (copy / folder / name).symlink_to(root / folder / name, target_is_directory=True)
        for name in COPIED:
            if (root / folder / name).is_file() and not (copy / folder / name).exists():
                shutil.copy2(root / folder / name, copy / folder / name)


def convert_in_place(root: Path, spared: list[str]) -> list[str]:
    """`kiln update`'s pass: the same converters, after the template, left in the tree with its
    changes for the review the update asks for; no branch, no commit. The `spared` files (frozen,
    kept) come out as they went in. A converter that fails is named and skipped. Returns the
    rules converted."""
    before = {name: _read_bytes(root / name) for name in spared}
    converted = []
    for rule in plan(root):
        if _closed(root, rule):
            continue
        try:
            changed = FIXERS[rule.fixer].convert(read_repo(root))
        except Exception as error:  # a converter's bug never stops the update
            ui.note(f"{rule.id} left for kiln fix: {_failure(error)}")
            continue
        if set(changed) - set(spared):
            converted.append(rule.id)
    for name, content in before.items():
        path = root / name
        if content is not None:
            path.write_bytes(content)
        elif path.is_file():
            path.unlink()
    if converted:
        ui.note(f"Converted after the template (kiln fix's converters): {', '.join(converted)}")
    return converted


def _read_bytes(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


def _apply(
    root: Path,
    rule: Rule,
    judges: list[checks.Check],
    unverified: str,
    report: score.Report,
    branch: str,
) -> tuple[Outcome, score.Report]:
    """One converter, proven, and the grid after it. `unverified` says why the checks cannot
    judge it; empty when they can."""
    fixer = FIXERS[rule.fixer]
    ui.step(f"{rule.id}: {fixer.summary}")
    if _closed(root, rule):
        return Outcome(rule.id, UNCHANGED, note=CLOSED), report
    try:
        changed = fixer.convert(read_repo(root))
    except Exception as error:  # a converter's bug: the tree is put back, the run goes on
        _reset(root)
        return Outcome(rule.id, UNCHANGED, note=_failure(error)), report
    _stage(root, changed)
    if not git(root, "diff", "--cached", "--name-only"):
        return Outcome(rule.id, UNCHANGED, note="nothing to change"), report
    after = score.score_repo(root)
    broken = [
        found.rule
        for found in after.findings
        if found.status == score.FAILED and _status(report, found.rule) == score.PASSED
    ]
    if broken:
        _reset(root)
        note = f"turned {', '.join(broken)} red: undone (a converter bug, to report to kiln)"
        return Outcome(rule.id, REVERTED, tuple(changed), note), report
    failure = None if unverified else checks.first_failure(root, judges)
    builds = checks.image_builds(root, changed)
    build_failure = checks.first_failure(root, builds) if failure is None else None
    if build_failure is not None and not _built_before(root, build_failure.check):
        # The image did not build before the converter either: it cannot judge it.
        unverified = (unverified + "; " if unverified else "") + (
            f"unverified: `{build_failure.check}` was red before the fix"
        )
        build_failure = None
    failure = failure or build_failure
    points = None if after.score is None or report.score is None else after.score - report.score
    message = _message(rule, fixer.summary, report.score, after.score)
    if failure is not None:
        aside = _set_aside(root, rule, branch, failure, message)
        note = f"`{failure.check}` turned red: set aside on {aside} (kiln score --roadmap)"
        return Outcome(rule.id, REVERTED, tuple(changed), note), report
    checks.forget_log(root, rule.id)
    proven = [*map(str, judges), *(str(build) for build in builds if not unverified)]
    body = f"{unverified}" if unverified else f"Checked: {', '.join(proven)}"
    git(root, "commit", "-q", "-m", message[0], "-m", f"{message[1]}\n\n{body}")
    left = _status(after, rule.id) == score.FAILED
    notes = [*([unverified] if unverified else []), *(["a gap left for judgment"] if left else [])]
    status = PARTIAL if left else FIXED
    return Outcome(rule.id, status, tuple(changed), "; ".join(notes), points), after


def _message(rule: Rule, summary: str, before: int | None, after: int | None) -> tuple[str, str]:
    """The subject and body of a converter's commit: why, the source, the points won."""
    source = rule.sources[0].url if rule.sources else ""
    body = f"{rule.why}\n\nSource: {source}\nRule: kiln grid {rule.id}"
    if before is not None and after is not None:
        body += f"\nScore: {before} → {after} ({after - before:+d})"
    return f"fix({rule.id}): {summary}", body


def _set_aside(
    root: Path, rule: Rule, branch: str, failure: checks.Result, message: tuple[str, str]
) -> str:
    """A converter that turns the repo's checks red leaves the batch, never dropped: committed
    on a branch of its own with the failing output, the log kept for `kiln score --roadmap`."""
    aside, _ = _branch(root, f"{branch}-{rule.id.lower()}")
    log = checks.keep_log(root, rule.id, failure, aside)
    red = f"Red: `{failure.check}`, its output in {log}" if log else f"Red: `{failure.check}`"
    git(root, "commit", "-q", "-m", message[0], "-m", f"{message[1]}\n\n{red}")
    git(root, "branch", "-f", aside, "HEAD")
    git(root, "reset", "-q", "--hard", "HEAD~1")
    return aside


def _status(report: score.Report, rule_id: str) -> str:
    found = score.rule_finding(report, rule_id)
    return found.status if found is not None else score.LEFT_OUT


def _failure(error: Exception) -> str:
    """What a converter's error says: its own words, or a bug named as one."""
    if isinstance(error, (OSError, ValueError, KilnError)) and not isinstance(
        error, (UnicodeError, yaml.YAMLError)
    ):
        return str(error)
    return f"converter bug ({type(error).__name__}: {error}), to report to kiln"


def _reset(root: Path) -> None:
    git(root, "reset", "-q", "--hard")
    git(root, "clean", "-fdq")


def _closed(root: Path, rule: Rule) -> bool:
    """An earlier converter closed the rule too (the minimal CI runs the linters): nothing left
    to add."""
    return detectors.detect(rule.detector, read_repo(root)).status != detectors.FAIL


def _built_before(root: Path, build: checks.Check) -> bool:
    """Whether the image built from the last commit, the converter's change aside."""
    with scratch_worktree(root, "--detach") as copy:
        return checks.run(copy, build).ok


def _stage(root: Path, changed: list[str]) -> None:
    """Everything the converter touched, files the repo's `.gitignore` would hide included:
    a repo that ignores `.*` still gets its `.github/dependabot.yml`."""
    git(root, "add", "--all")
    if changed:
        git(root, "add", "--force", "--", *changed)


def _dry_run(copy: Path, rules: list[Rule]) -> list[Outcome]:
    outcomes = []
    for rule in rules:
        fixer = FIXERS[rule.fixer]
        try:
            changed = fixer.convert(read_repo(copy))
        except Exception as error:  # a converter's bug: the next one still shows its diff
            _reset(copy)
            print(f"\n  {ui.paint(rule.id, ui.FIRE, bold=True)}  not changed: {_failure(error)}")
            outcomes.append(Outcome(rule.id, UNCHANGED, note=_failure(error)))
            continue
        _stage(copy, changed)
        diff = git(copy, "diff", "--cached", "--stat")
        print(f"\n  {ui.paint(rule.id, ui.FIRE, bold=True)}  {fixer.summary}")
        print(git(copy, "diff", "--cached") or "  (nothing to change)")
        git(copy, "commit", "-q", "--allow-empty", "-m", rule.id)
        status = FIXED if diff else UNCHANGED
        outcomes.append(Outcome(rule.id, status, tuple(changed), "dry run"))
    ui.note("Dry run: nothing written. kiln fix to apply.")
    return outcomes


def _points(outcome: Outcome) -> str:
    return "" if outcome.points is None else f" {outcome.points:+d}"


def _summary(
    outcomes: list[Outcome],
    before: int | None,
    after: int | None,
    branch: str,
    unverified: str,
    unusable: list[str],
) -> None:
    lines = [
        f"{found.rule}: {found.status}{_points(found)}{f' ({found.note})' if found.note else ''}"
        for found in outcomes
    ]
    lines.append(f"score: {before} → {after} (kiln score for what is left to judgment)")
    if unverified:
        lines.append(f"{unverified}: read each commit before merging")
    lines += [f"not judging: {reason}" for reason in unusable]
    ui.panel(f"kiln fix on {branch}", lines)
