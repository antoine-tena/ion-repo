"""The compressor (T-139): dead code and unused dependencies removed, each removal proven.

vulture, deptry and knip propose (`candidates`), guards keep what no static tool can see, and
`proof` decides: the type checker, then the tests compared one by one with a run before
anything was removed. Removals go in batches; a batch that breaks a step is split in halves
until the culprit stands alone and is put back (delta debugging: a few runs of the tests, not
one per candidate). Each kept batch is staged, so an undo restores the tree from the index.
Rounds repeat while removing code uncovers more: a helper only a dead function called.
"""

import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from ion_repo import ui
from ion_repo.grid.compressor import candidates, proof, removal
from ion_repo.grid.compressor.candidates import CODE, DEPENDENCY, Candidate, Skipped
from ion_repo.grid.facts import Repo, read_repo
from ion_repo.shell import KilnError

CODE_PHASE, DEPENDENCY_PHASE = "code", "dependencies"
MAX_ROUNDS = 5
# Test runs a compression may spend, the baseline aside: past it, what is left is said, not
# tried.
MAX_PROOFS = 60


@dataclass
class Report:
    kept: list[Candidate] = field(default_factory=list)
    rejected: list[tuple[Candidate, str]] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    untried: list[Candidate] = field(default_factory=list)
    proofs: int = 0


def compress(repo: Repo, phase: str) -> list[str]:
    """What `phase` finds, removed where the proof holds; the paths changed."""
    root = repo.root
    # The environments as their locks say: tests run on them, knip reads them.
    removal.sync_environment(
        root,
        {
            *proof.projects(root, repo.files, "pyproject.toml"),
            *proof.projects(root, repo.files, "package.json"),
        },
    )
    base = proof.baseline(root, proof.steps(root, repo.files))
    for dropped in base.dropped:
        ui.note(f"Left out of the proof: {dropped}")
    if not base.proves:
        raise KilnError("no tests to prove a removal with: nothing removed (write tests first)")
    ui.note("Proof: " + " → ".join(step.name for step in base.steps) + ", test by test")
    ui.note(
        f"One proof takes about {ui.format_duration(base.seconds)}: at most {MAX_PROOFS}, "
        "a batch that holds costs one"
    )
    _checkpoint(root)
    report = Report()
    tried: set[Candidate] = set()
    for _ in range(MAX_ROUNDS):
        found, skipped = _gather(read_repo(root), phase, base.executed)
        report.skipped += [item for item in skipped if item.candidate not in tried]
        fresh = [item for item in found if item not in tried]
        tried |= set(found) | {item.candidate for item in skipped}
        if not fresh:
            break
        ui.step(f"{len(fresh)} candidate(s) to prove")
        kept = _settle(root, fresh, base, report)
        if not kept or phase != CODE_PHASE:
            break
        # Lines moved: the coverage of the next round is measured again.
        base.executed = proof.coverage(root, base)
    _summary(report)
    return sorted({item.path for item in report.kept})


def _gather(
    repo: Repo, phase: str, executed: dict[str, set[int]] | None
) -> tuple[list[Candidate], list[Skipped]]:
    if phase == CODE_PHASE:
        found, skipped = candidates.dead_code(repo, executed)
        node_found, node_skipped = candidates.node_unused(repo)
        found += [item for item in node_found if item.kind != DEPENDENCY]
        skipped += [item for item in node_skipped if item.candidate.kind != DEPENDENCY]
        return found, skipped
    found, skipped = candidates.python_dependencies(repo)
    node_found, node_skipped = candidates.node_unused(repo)
    found += [item for item in node_found if item.kind == DEPENDENCY]
    skipped += [item for item in node_skipped if item.candidate.kind == DEPENDENCY]
    return found, skipped


def _settle(
    root: Path, batch: list[Candidate], base: proof.Baseline, report: Report
) -> list[Candidate]:
    """The batch removed if the proof holds; else split in halves, down to the one that
    breaks it, which stays."""
    if report.proofs >= MAX_PROOFS:
        report.untried += batch
        return []
    applied = [item for item in batch if removal.remove(root, item)]
    if not applied:
        return []
    removal.tidy_imports(root, [item.path for item in applied if item.kind == CODE])
    projects = {
        str(Path(item.path).parent).removeprefix(".") for item in applied if item.kind == DEPENDENCY
    }
    if projects:
        removal.sync_environment(root, projects)
    report.proofs += 1
    broke = proof.holds(root, base, [item.path for item in applied])
    if not broke:
        _checkpoint(root)
        report.kept += applied
        if len(applied) < 4:
            for item in applied:
                ui.success(f"removed {item.label}")
        else:
            ui.success(f"{len(applied)} removals proven together")
        return applied
    _undo(root)
    if projects:
        removal.sync_environment(root, projects)
    if len(applied) == 1:
        report.rejected.append((applied[0], broke))
        ui.note(f"kept {applied[0].label}: {broke}")
        return []
    middle = len(applied) // 2
    return _settle(root, applied[:middle], base, report) + _settle(
        root, applied[middle:], base, report
    )


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, capture_output=True, check=False)


def _checkpoint(root: Path) -> None:
    """The tree as proven so far, staged: the point an undo goes back to."""
    _git(root, "add", "--all")


def _undo(root: Path) -> None:
    _git(root, "restore", "--worktree", "--", ".")


def _summary(report: Report) -> None:
    lines = [
        f"removed: {len(report.kept)} ({sum(item.lines for item in report.kept)} lines of code "
        f"or files, {sum(item.kind == DEPENDENCY for item in report.kept)} dependencies)",
        f"kept by the proof: {len(report.rejected)}",
        f"kept by a guard: {len(report.skipped)}",
        f"test runs: {report.proofs}",
    ]
    reasons = Counter(item.reason.split(":")[0] for item in report.skipped)
    lines += [f"  {count}: {reason}" for reason, count in reasons.most_common()]
    if report.untried:
        lines.append(f"not tried, test budget spent: {len(report.untried)} (run again)")
    ui.panel("compressor", lines)


def remove_dead_code(repo: Repo) -> list[str]:
    return compress(repo, CODE_PHASE)


def remove_unused_dependencies(repo: Repo) -> list[str]:
    return compress(repo, DEPENDENCY_PHASE)
