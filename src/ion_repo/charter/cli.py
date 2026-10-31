"""charter: checks a repo against the rules of its charter, declared in the `charter.toml` at its
root. Installed with ion-repo, next to the `ion-repo` command (`charte`, its name before kiln 0.4.0,
still works).

A charter that nothing runs describes a project that does not exist. Two regimes, because a
check that fails on 47 files on day one ends up disabled:

- **ban** (`[bans.<name>]`): the rule holds everywhere, any reintroduction fails;
- **ratchet** (`[ratchets.<name>]`, `budget`): the rule has a debt, its current size becomes a
  ceiling. The check fails if the debt grows, and says so when it shrinks: the budget is then
  lowered in charter.toml, so the debt can never come back. A **floor** (`[floors.<name>]`,
  `floor`) is the reverse ratchet.

A section is named after its rule (see bans.py and ratchets.py); a `rule` key declares several
of the same kind. `local_rules`: Python modules of the repo, each with a function
`check(repo, params) -> list[str]`, for its own rules.

Waivers: `kiln-waivers.toml` (see waivers.py) lifts a rule from the whole repo or from some
paths, for a limited time; they are listed at each check.

Usage: charter [check]      the rules of the charter (default)
       charter file <path>… the bans on those files alone, fast (edit hook, ion repo check)
       charter types        mypy typing as a ratchet ([types])
       charter coverage     coverage floors of the backend ([coverage])
       charter --detail     value of each ratchet and floor, without judging
       charter --unverified rules of the instructions that no check enforces
Exit code non-zero when a rule is broken.
"""

from __future__ import annotations

import datetime
import importlib.util
import subprocess
import sys
from collections.abc import Callable, Iterator
from pathlib import Path

from ion_repo.charter.bans import BANS
from ion_repo.charter.config import CHARTER_FILE, charter_path, load
from ion_repo.charter.python_tools import coverage, types
from ion_repo.charter.ratchets import COUNTERS
from ion_repo.charter.repo import Params, Repo, failure
from ion_repo.charter.waivers import RULE_ID, WAIVERS_FILE, Waivers, check_targets
from ion_repo.charter.waivers import load as load_waivers
from ion_repo.rules import charter_rules

# A repo's own rule: `check(repo, params)` returns its failures.
LocalRule = Callable[[Repo, Params], list[str]]
RULE_SECTIONS = ("bans", "ratchets", "floors")
# Bans that look at the repo as a whole, not file by file: left to the full check.
REPO_WIDE_BANS = {"django-migrations", "forbidden-files", "identical-copies", "compose-profiles"}


def open_repo() -> Repo:
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
    ).stdout.strip()
    root = Path(top or ".")
    if charter_path(root) is None:
        sys.exit(f"charter: no {CHARTER_FILE} at the root of the repo ({root}).")
    return Repo(root, load(root))


def _local_rules(repo: Repo) -> list[LocalRule]:
    functions: list[LocalRule] = []
    for relative in repo.config.get("local_rules", []):
        spec = importlib.util.spec_from_file_location(Path(relative).stem, repo.root / relative)
        if spec is None or spec.loader is None:
            raise SystemExit(f"charter: unreadable local rule: {relative}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # `verifier`: its name before kiln 0.4.0.
        functions.append(getattr(module, "check", None) or module.verifier)
    return functions


def unverified_rules(repo: Repo) -> list[str]:
    """Rules of the instructions applied in review (no check enforces them), as listed by ion-repo
    in the file `unverified_rules` names."""
    relative = repo.config.get("unverified_rules")
    if not relative or not (repo.root / relative).is_file():
        return []
    lines = (repo.root / relative).read_text("utf-8").splitlines()
    return [line for line in lines if line and not line.startswith("#")]


def waivers_of(repo: Repo, today: datetime.date | None = None) -> Waivers:
    """Waivers of `kiln-waivers.toml` as of `today`, checked against the rules and the files of
    the repo; a rule of the grid counts (a false positive of `ion repo score` dismissed on its
    path)."""
    from ion_repo.grid.model import load_rules

    waivers = load_waivers(repo.root, today)
    known = [
        params["id"]
        for section in RULE_SECTIONS
        for params in repo.config.get(section, {}).values()
        if "id" in params
    ]
    check_targets(
        waivers,
        [*known, *charter_rules(repo.root), *(rule.id for rule in load_rules())],
        lambda pattern: repo.tracked(pattern, excluded=False),
    )
    return waivers


def rules(repo: Repo, section: str, waivers: Waivers) -> Iterator[tuple[str, Params]]:
    """Rules of a section, each checked outside the paths its waivers cover; a rule waived in
    the whole repo is skipped."""
    for name, params in repo.config.get(section, {}).items():
        waived = waivers.waived_paths(params.get("id", ""))
        if waived is None:
            continue
        repo.waived = waived
        try:
            yield name, params
        finally:
            repo.waived = []


def measures(
    repo: Repo, section: str, waivers: Waivers | None = None
) -> list[tuple[str, Params, int, list[str]]]:
    measured = []
    for name, params in rules(repo, section, waivers or Waivers()):
        value, detail = COUNTERS[params.get("rule", name)](repo, params)
        measured.append((name, params, value, detail))
    return measured


def _report_waivers(waivers: Waivers) -> None:
    if not (waivers.actives or waivers.warnings):
        return
    print(f"Waivers ({WAIVERS_FILE}): {len(waivers.actives)} active.")
    for waiver in waivers.actives:
        print(f"  {waiver.label}: {waiver.reason} ({waiver.by}, until {waiver.until or 'never'})")
    for warning in waivers.warnings:
        print(f"  ! {warning}")
    print()


def _ratchet_problems(repo: Repo, waivers: Waivers, to_tighten: list[str]) -> list[str]:
    problems = []
    for name, params, value, detail in measures(repo, "ratchets", waivers):
        budget = params["budget"]
        if value > budget:
            message = (
                f"{params.get('message', name)}: {value} offences, ceiling {budget}: "
                f"{value - budget} more than at the last lowering."
            )
            problems.append(failure(params.get("id", "RATCHET"), message, detail))
        elif value < budget:
            to_tighten.append(
                f"  {name}: {value} < {budget}: lower `budget` of [ratchets.{name}] to {value} "
                f"({CHARTER_FILE})."
            )
    for name, params, value, detail in measures(repo, "floors", waivers):
        floor = params["floor"]
        if value < floor:
            message = f"{params.get('message', name)}: {value}, floor {floor}. The value went down."
            problems.append(failure(params.get("id", "FLOOR"), message, detail))
        elif value > floor:
            to_tighten.append(
                f"  {name}: {value} > {floor}: raise `floor` of [floors.{name}] to {value} "
                f"({CHARTER_FILE})."
            )
    return problems


def check(repo: Repo) -> int:
    waivers = waivers_of(repo)
    _report_waivers(waivers)
    problems: list[str] = []
    if waivers.errors:
        problems.append(failure(RULE_ID, f"waivers to review ({WAIVERS_FILE})", waivers.errors))
    for name, params in rules(repo, "bans", waivers):
        problems.extend(BANS[params.get("rule", name)](repo, params))
    for local_rule in _local_rules(repo):
        problems.extend(local_rule(repo, {}))
    to_tighten: list[str] = []
    problems += _ratchet_problems(repo, waivers, to_tighten)
    if to_tighten:
        print("Debt reduced, budgets to tighten (the check stays green):")
        print("\n".join(to_tighten))
        print()
    unverified = unverified_rules(repo)
    in_review = (
        f"\n{len(unverified)} rules of the instructions are applied in review, not by this "
        "check (charter --unverified)."
        if unverified
        else ""
    )
    if problems:
        print("Charter violations:\n")
        print("\n\n".join(problems))
        print(
            "\nThe charter is the norm of this repo: fix the code, or amend the charter "
            "explicitly (ion repo waive for a deliberate deviation)." + in_review
        )
        return 1
    print("Checked rules of the charter: no violation, no ratchet exceeded." + in_review)
    return 0


def check_file(repo: Repo, file: str) -> int:
    """The bans on one file, for the hook after each edit: it has to answer in a blink, so the
    ratchets, the floors, the repo-wide bans and the local rules are left to the full check
    (commit and CI)."""
    path = Path(file).resolve()
    try:
        relative = str(path.relative_to(repo.root.resolve()))
    except ValueError:
        return 0
    if not path.is_file() or repo.git("check-ignore", "--", relative):
        return 0
    waivers = load_waivers(repo.root)
    repo.only = relative
    problems: list[str] = []
    for name, params in rules(repo, "bans", waivers):
        rule = params.get("rule", name)
        if rule not in REPO_WIDE_BANS:
            problems.extend(BANS[rule](repo, params))
    if not problems:
        return 0
    print(f"Charter violations in {relative}:\n")
    print("\n\n".join(problems))
    print(
        "\nFix the code, or waive the rule for this file if the deviation is deliberate: "
        f'ion repo waive <RULE> --paths {relative} --reason "…".'
    )
    return 1


def detail(repo: Repo) -> int:
    for section in ("ratchets", "floors"):
        for name, params, value, _ in measures(repo, section):
            threshold = params.get("budget", params.get("floor"))
            print(f"{section}.{name} = {value} (threshold {threshold})")
    return 0


def show_unverified(repo: Repo) -> int:
    print("Rules of the instructions applied in review (no check enforces them):")
    print("\n".join(f"  {rule}" for rule in unverified_rules(repo)) or "  (none)")
    return 0


ACTIONS: dict[str, Callable[[Repo], int]] = {
    "check": check,
    "types": types,
    "coverage": coverage,
    "--detail": detail,
    "--unverified": show_unverified,
    # Names before kiln 0.4.0.
    "verifier": check,
    "couverture": coverage,
}


def main() -> int:
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    if action == "file" and len(sys.argv) >= 3:
        repo = open_repo()
        return max(check_file(repo, path) for path in sys.argv[2:])
    if action not in ACTIONS:
        sys.exit(__doc__)
    return ACTIONS[action](open_repo())


def run() -> None:
    """Entry point of the `charter` command installed with ion-repo."""
    sys.exit(main())


if __name__ == "__main__":
    run()
