"""`kiln fix`: every gap a script can close, closed on a work branch, with proof.

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

from kiln import ui
from kiln.grid import checks, detectors, score
from kiln.grid.facts import read_repo
from kiln.grid.fixers import FIXERS
from kiln.grid.model import Rule, load_rules
from kiln.shell import KilnError

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


@dataclass(frozen=True)
class Outcome:
    rule: str
    status: str  # fixed, reverted, unchanged
    files: tuple[str, ...] = ()
    note: str = ""


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


def fix(root: Path, *, dry_run: bool = False, only: str | None = None) -> list[Outcome]:
    root = Path(git(root, "rev-parse", "--show-toplevel").strip())
    if git(root, "status", "--porcelain"):
        ui.note("From the last commit: uncommitted changes left out, and left as they are.")
    if dry_run:
        with scratch_worktree(root, "--detach") as copy:
            rules = _announce(copy, only)
            return _dry_run(copy, rules) if rules else []
    branch, reused = _branch(root)
    with scratch_worktree(root, "-B" if reused else "-b", branch) as copy:
        rules = _announce(copy, only)
        outcomes = _run(copy, rules, branch, reused) if rules else []
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


def _run(root: Path, rules: list[Rule], branch: str, reused: bool) -> list[Outcome]:
    before = score.score_repo(root).score
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
    outcomes = [_apply(root, rule, judges, unverified) for rule in rules]
    after = score.score_repo(root).score
    where = f"{branch} (updated from the last commit)" if reused else branch
    _summary(outcomes, before, after, where, unverified, unusable if judges else [])
    return outcomes


def _branch(root: Path) -> tuple[str, bool]:
    """Today's branch, and whether it is taken over: one holding only `kiln fix` commits, and
    checked out nowhere, starts again from the last commit (what kiln-bot updates); any other
    gets a suffix (`kiln/fix-2026-10-24-2`)."""
    base = f"kiln/fix-{datetime.date.today().isoformat()}"
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
def scratch_worktree(root: Path, *options: str) -> Iterator[Path]:
    """A worktree of the last commit out of the user's tree (`options`: `--detach`, or `-b`
    and a branch), with what the checks need from the tree; removed afterwards, its branch kept."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="kiln-fix-", dir=SCRATCH))
    copy = scratch / "repo"
    try:
        git(root, "worktree", "add", "-q", *options, str(copy), "HEAD")
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
        except (OSError, ValueError, KilnError) as error:
            ui.note(f"{rule.id} left for kiln fix: {error}")
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


def _apply(root: Path, rule: Rule, judges: list[checks.Check], unverified: str) -> Outcome:
    """`unverified` says why the checks cannot judge this converter; empty when they can."""
    fixer = FIXERS[rule.fixer]
    ui.step(f"{rule.id}: {fixer.summary}")
    if _closed(root, rule):
        return Outcome(rule.id, "unchanged", note=CLOSED)
    try:
        changed = fixer.convert(read_repo(root))
    except (OSError, ValueError, KilnError) as error:
        git(root, "reset", "-q", "--hard")
        git(root, "clean", "-fdq")
        return Outcome(rule.id, "unchanged", note=str(error))
    _stage(root, changed)
    if not git(root, "diff", "--cached", "--name-only"):
        return Outcome(rule.id, "unchanged", note="nothing to change")
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
    if failure is not None:
        git(root, "reset", "-q", "--hard")
        git(root, "clean", "-fdq")
        log = checks.keep_log(root, rule.id, failure)
        where = f", log for Claude in {log} (kiln score --roadmap)" if log else ""
        note = f"`{failure.check}` turned red: undone{where}"
        return Outcome(rule.id, "reverted", tuple(changed), note)
    checks.forget_log(root, rule.id)
    source = rule.sources[0].url if rule.sources else ""
    body = f"{rule.why}\n\nSource: {source}\nRule: kiln grid {rule.id}"
    proven = [*map(str, judges), *(str(build) for build in builds if not unverified)]
    body += f"\n\n{unverified}" if unverified else f"\n\nChecked: {', '.join(proven)}"
    git(root, "commit", "-q", "-m", f"fix({rule.id}): {fixer.summary}", "-m", body)
    return Outcome(rule.id, "fixed", tuple(changed), unverified)


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
        except (OSError, ValueError, KilnError) as error:
            print(f"\n  {ui.paint(rule.id, ui.FIRE, bold=True)}  not changed: {error}")
            outcomes.append(Outcome(rule.id, "unchanged", note=str(error)))
            continue
        _stage(copy, changed)
        diff = git(copy, "diff", "--cached", "--stat")
        print(f"\n  {ui.paint(rule.id, ui.FIRE, bold=True)}  {fixer.summary}")
        print(git(copy, "diff", "--cached") or "  (nothing to change)")
        git(copy, "commit", "-q", "--allow-empty", "-m", rule.id)
        status = "fixed" if diff else "unchanged"
        outcomes.append(Outcome(rule.id, status, tuple(changed), "dry run"))
    ui.note("Dry run: nothing written. kiln fix to apply.")
    return outcomes


def _summary(
    outcomes: list[Outcome],
    before: int | None,
    after: int | None,
    branch: str,
    unverified: str,
    unusable: list[str],
) -> None:
    lines = [
        f"{found.rule}: {found.status}{f' ({found.note})' if found.note else ''}"
        for found in outcomes
    ]
    lines.append(f"score: {before} → {after} (kiln score for what is left to judgment)")
    if unverified:
        lines.append(f"{unverified}: read each commit before merging")
    lines += [f"not judging: {reason}" for reason in unusable]
    ui.panel(f"kiln fix on {branch}", lines)
