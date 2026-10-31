"""`ion repo eval-skills`: does each skill of the repo plugin fire on the sentence meant for it?

A thin wrapper over `claude plugin eval`, whose cases live in `plugins/repo/evals/<case>/`. Each
case is one Claude session on the user's own quota, so it locks what the defaults would multiply:
one run per case (default 3), no no-plugin arm (default doubles the sessions), one at a time, a
cost ceiling, Opus (Haiku does not choose its skills as Opus does), the report kept local. Only
the cases of the skills changed against `develop` run, with the should-not-fire ones. Nothing
starts before the user, at a terminal, has typed ok three times.
"""

import re
import subprocess
import sys
from pathlib import Path

from ion_repo.shell import KilnError, repo_root

PLUGIN = Path("plugins/repo")
EVALS = PLUGIN / "evals"
SKILLS = PLUGIN / "skills"
INTEGRATION_BRANCH = "develop"
# The cases where no skill should fire: run with every selection, a shorter description can
# fire too often as well as too rarely.
NEGATIVE_TAG = "none"
MODEL = "opus"
DEFAULT_MAX_COST_USD = 2.0
CONFIRMATIONS = 3
TAGS = re.compile(r"^tags:\s*\[(?P<tags>[^\]]*)\]", re.MULTILINE)


def eval_skills(
    cwd: Path,
    skills: list[str],
    *,
    every: bool = False,
    max_cost_usd: float = DEFAULT_MAX_COST_USD,
    dry_run: bool = False,
) -> None:
    root = repo_root(cwd)
    if not (root / EVALS).is_dir():
        raise KilnError(f"no {EVALS}/ here: eval-skills runs in ion-repo's own repo")
    cases = case_tags(root / EVALS)
    wanted = sorted({tag for tags in cases.values() for tag in tags} if every else set(skills))
    if not wanted:
        wanted = changed_skills(root)
    if not wanted:
        raise KilnError(
            f"no skill changed against {INTEGRATION_BRANCH}: name one with --skill, or --all"
        )
    tags = [*wanted, NEGATIVE_TAG] if NEGATIVE_TAG not in wanted else wanted
    selected = [name for name, case in cases.items() if set(case) & set(tags)]
    command = eval_command(tags, max_cost_usd)
    print(f"Cases: {', '.join(selected)}")
    print(f"Sessions: {len(selected)} {MODEL} (one per case), at most ${max_cost_usd:g}")
    print("Command: " + " ".join(command))
    if dry_run:
        return
    confirm()
    launch(command, root)


def case_tags(evals: Path) -> dict[str, list[str]]:
    """The tags of each case, read from the `tags: [...]` line of its `prompt.md`."""
    cases: dict[str, list[str]] = {}
    for prompt in sorted(evals.glob("*/prompt.md")):
        found = TAGS.search(prompt.read_text())
        tags = found["tags"].split(",") if found else []
        cases[prompt.parent.name] = [tag.strip() for tag in tags if tag.strip()]
    return cases


def changed_skills(root: Path) -> list[str]:
    """Skills whose folder or case differs from the integration branch, uncommitted included."""
    listing = subprocess.run(
        ["git", "diff", "--name-only", INTEGRATION_BRANCH, "--", str(SKILLS), str(EVALS)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if listing.returncode != 0:
        raise KilnError(f"git diff against {INTEGRATION_BRANCH} failed: {listing.stderr.strip()}")
    names = set()
    for line in listing.stdout.splitlines():
        parts = Path(line).parts
        if len(parts) > 3 and parts[2] in {"skills", "evals"} and parts[3] != "results":
            names.add(parts[3])
    return sorted(names)


def eval_command(tags: list[str], max_cost_usd: float) -> list[str]:
    return [
        "claude",
        "plugin",
        "eval",
        str(PLUGIN),
        "--model",
        MODEL,
        "--runs",
        "1",
        "--ablation",
        "none",
        "-j",
        "1",
        "--max-cost-usd",
        f"{max_cost_usd:g}",
        "--no-publish",
        "--tag",
        *tags,
    ]


def launch(command: list[str], root: Path) -> None:
    returncode = subprocess.run(command, cwd=root, check=False).returncode
    if returncode != 0:
        raise KilnError(f"`claude plugin eval` failed (code {returncode})")


def confirm() -> None:
    """Three ok typed at a terminal: Claude's Bash has none, so it cannot answer for the user."""
    if not sys.stdin.isatty():
        raise KilnError(
            "eval-skills starts Claude sessions on your quota: run it yourself in a terminal"
        )
    for count in range(1, CONFIRMATIONS + 1):
        answer = input(f"Type ok to go on ({count}/{CONFIRMATIONS}): ").strip().lower()
        if answer != "ok":
            raise KilnError("stopped: nothing was started")
