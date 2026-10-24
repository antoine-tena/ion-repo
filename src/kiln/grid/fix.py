"""`kiln fix`: every gap a script can close, closed on a work branch, with proof.

The repo's own checks run before and after each converter: one that turns them red is undone
and reported, never left in a commit. One commit per rule, its message giving the why and the
source. `--dry-run` shows the plan and the diff on a throwaway worktree, the repo untouched.
"""

import datetime
import os
import shutil
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path

from kiln import ui
from kiln.grid import score
from kiln.grid.facts import read_repo
from kiln.grid.fixers import FIXERS
from kiln.grid.model import Rule, load_rules
from kiln.shell import KilnError

UNVERIFIED = "unverified: no tests"


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


def check_commands(root: Path) -> list[list[str]]:
    """The repo's own checks: `kiln check --all` in a kiln repo, otherwise the tests, lint and
    types its manifests declare. The whole repo, before and after alike: `kiln check` alone
    looks at the branch's changes, and would blame a converter for the older debt of a file it
    touched (a Dockerfile the charter bans), then undo it."""
    if (root / ".copier-answers.yml").exists():
        return [["kiln", "check", "--all"]]
    commands: list[list[str]] = []
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            project = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            project = {}
        runner = ["uv", "run"] if (root / "uv.lock").exists() else []
        tools = project.get("tool", {})
        if "ruff" in tools:
            commands.append([*runner, "ruff", "check"])
        if "mypy" in tools:
            commands.append([*runner, "mypy", "."])
        if "pytest" in tools or (root / "tests").is_dir():
            commands.append([*runner, "pytest", "-q"])
    package = root / "package.json"
    if package.exists():
        manager = "pnpm" if (root / "pnpm-lock.yaml").exists() else "npm"
        text = package.read_text(encoding="utf-8")
        commands += [[manager, "run", name] for name in ("lint", "test") if f'"{name}"' in text]
    return commands


def run_checks(root: Path, commands: list[list[str]]) -> bool:
    for command in commands:
        if shutil.which(command[0]) is None:
            return False
        # No bytecode written: `git add --all` would commit it in a repo that does not ignore it.
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        done = subprocess.run(command, cwd=root, env=environment, capture_output=True, check=False)
        if done.returncode != 0:
            return False
    return True


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
    # A dry run works on a copy of the last commit: the tree's changes are neither needed nor
    # touched.
    is_dirty = bool(git(root, "status", "--porcelain"))
    if is_dirty and not dry_run:
        raise KilnError("the tree has uncommitted changes: commit or stash them first")
    rules = plan(root, only)
    before = score.score_repo(root).score
    if not rules:
        ui.note("Nothing a script can close here: kiln score lists what is left for judgment.")
        return []
    ui.step(f"{len(rules)} rule(s) a script can close: {', '.join(rule.id for rule in rules)}")
    reaching = [rule.id for rule in rules if FIXERS[rule.fixer].network]
    if reaching:
        ui.note(f"Network needed (commit SHAs, image digests) for: {', '.join(reaching)}")
    if dry_run:
        if is_dirty:
            ui.note("Dry run from the last commit: uncommitted changes left out.")
        return _dry_run(root, rules)
    branch = f"kiln/fix-{datetime.date.today().isoformat()}"
    git(root, "switch", "-c", branch)
    commands = check_commands(root)
    green_before = bool(commands) and run_checks(root, commands)
    outcomes = [_apply(root, rule, commands, green_before) for rule in rules]
    after = score.score_repo(root).score
    _summary(outcomes, before, after, branch, verified=green_before)
    return outcomes


def _apply(root: Path, rule: Rule, commands: list[list[str]], verified: bool) -> Outcome:
    fixer = FIXERS[rule.fixer]
    ui.step(f"{rule.id}: {fixer.summary}")
    try:
        changed = fixer.convert(read_repo(root))
    except (OSError, ValueError, KilnError) as error:
        git(root, "reset", "-q", "--hard")
        git(root, "clean", "-fdq")
        return Outcome(rule.id, "unchanged", note=str(error))
    _stage(root, changed)
    if not git(root, "diff", "--cached", "--name-only"):
        return Outcome(rule.id, "unchanged", note="nothing to change")
    if verified and not run_checks(root, commands):
        git(root, "reset", "-q", "--hard")
        git(root, "clean", "-fdq")
        return Outcome(rule.id, "reverted", tuple(changed), "the checks turned red: undone")
    source = rule.sources[0].url if rule.sources else ""
    body = f"{rule.why}\n\nSource: {source}\nRule: kiln grid {rule.id}"
    if not verified:
        body += f"\n\n{UNVERIFIED}"
    git(root, "commit", "-q", "-m", f"fix({rule.id}): {fixer.summary}", "-m", body)
    return Outcome(rule.id, "fixed", tuple(changed), "" if verified else UNVERIFIED)


def _stage(root: Path, changed: list[str]) -> None:
    """Everything the converter touched, files the repo's `.gitignore` would hide included:
    a repo that ignores `.*` still gets its `.github/dependabot.yml`."""
    git(root, "add", "--all")
    if changed:
        git(root, "add", "--force", "--", *changed)


def _dry_run(root: Path, rules: list[Rule]) -> list[Outcome]:
    outcomes = []
    with tempfile.TemporaryDirectory(prefix="kiln-fix-") as scratch:
        copy = Path(scratch) / "repo"
        git(root, "worktree", "add", "-q", "--detach", str(copy))
        try:
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
        finally:
            git(root, "worktree", "remove", "--force", str(copy), check=False)
    ui.note("Dry run: nothing written. kiln fix to apply.")
    return outcomes


def _summary(
    outcomes: list[Outcome], before: int | None, after: int | None, branch: str, *, verified: bool
) -> None:
    lines = [
        f"{found.rule}: {found.status}{f' ({found.note})' if found.note else ''}"
        for found in outcomes
    ]
    lines.append(f"score: {before} → {after} (kiln score for what is left to judgment)")
    if not verified:
        lines.append(f"{UNVERIFIED} (or already red): read each commit before merging")
    ui.panel(f"kiln fix on {branch}", lines)
