"""`kiln bot`: kiln-bot's weekly run (T-59), "Dependabot for your methods".

On the branch `kiln/bot`, started again from the last commit at each run: in a kiln repo
`kiln update` first (the template, then the converters after it), then `kiln fix`, each commit
proven. What it brings becomes the body of one pull request kept up to date by the reusable
workflow `bot.yml`: the score before and after, and the why of each commit. Nothing when nothing
changed. The user's tree is never touched: everything happens in throwaway worktrees.
"""

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from kiln import ui
from kiln.grid import fix, score
from kiln.shell import KilnError
from kiln.stack import ANSWERS_FILE

BRANCH = "kiln/bot"
# What kiln-bot commits: a branch holding anything else is a person's work, never reset.
BOT_SUBJECT = re.compile(r"^(fix\([A-Z0-9-]+\)|chore\(kiln\)): ")
GRID_URL = "https://github.com/antoine-tena/kiln/blob/develop/docs/reference.md"
UPDATE_SUBJECT = "chore(kiln): kiln update to {version}"


@dataclass
class Proposal:
    before: int | None
    after: int | None
    commits: list[tuple[str, str]] = field(default_factory=list)  # subject, body
    notes: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.commits)


def run(root: Path, *, update: bool = True) -> Proposal:
    root = Path(fix.git(root, "rev-parse", "--show-toplevel").strip())
    _start_branch(root)
    before = _score_of(root, "HEAD")
    notes = _update(root) if update and (root / ANSWERS_FILE).exists() else []
    fix.fix(root, on=BRANCH)
    log = fix.git(root, "log", "--reverse", "--format=%s%x1f%b%x1e", f"HEAD..{BRANCH}")
    commits = [
        (subject.strip(), body.strip())
        for entry in log.split("\x1e")
        if entry.strip()
        for subject, _, body in [entry.partition("\x1f")]
    ]
    if not commits:
        fix.git(root, "branch", "-D", BRANCH)
        ui.note("kiln-bot: nothing to propose, the repo is as kiln would make it.")
        return Proposal(before, before, [], notes)
    return Proposal(before, _score_of(root, BRANCH), commits, notes)


def _start_branch(root: Path) -> None:
    """`kiln/bot` from the last commit; refused when a person committed on it."""
    if fix.git(root, "branch", "--list", BRANCH).strip():
        subjects = fix.git(root, "log", "--format=%s", f"HEAD..{BRANCH}").splitlines()
        foreign = [subject for subject in subjects if not BOT_SUBJECT.match(subject)]
        if foreign:
            raise KilnError(
                f"{BRANCH} holds commits kiln-bot did not write ({foreign[0]}): "
                "merge or delete the branch, kiln-bot then starts it again"
            )
    fix.git(root, "branch", "-f", BRANCH, "HEAD")


def _score_of(root: Path, ref: str) -> int | None:
    with fix.scratch_worktree(root, "--detach", ref=ref) as copy:
        return score.score_repo(copy).score


def _update(root: Path) -> list[str]:
    """`kiln update` on the branch, committed as one commit; what stops it is said in the pull
    request, never half applied."""
    from kiln.update import conflicted_files, template_commit, update_project

    with fix.scratch_worktree(root, ref=BRANCH) as copy:
        try:
            update_project(
                copy,
                should_update_template=True,
                should_update_deps=False,
                allow_major=False,
                should_check=False,
            )
        except (KilnError, OSError, subprocess.CalledProcessError) as error:
            fix._reset(copy)
            return [f"`kiln update` did not run: {error}"]
        if conflicted_files(copy):
            fix._reset(copy)
            return ["`kiln update` leaves conflicts to resolve by hand: run it in a session"]
        if not fix.git(copy, "status", "--porcelain"):
            return []
        fix.git(copy, "add", "--all")
        subject = UPDATE_SUBJECT.format(version=template_commit(copy) or "the latest release")
        body = "The template's changes, then the converters of `kiln fix` after it."
        fix.git(copy, "commit", "-q", "-m", subject, "-m", body)
    return []


def body(proposal: Proposal) -> str:
    """The pull request's description, in Markdown."""
    before, after = proposal.before, proposal.after
    delta = f" ({after - before:+d})" if before is not None and after is not None else ""
    lines = [
        f"## kiln score: {before} → {after}{delta}",
        "",
        f"Each commit closes a rule of [kiln's grid]({GRID_URL}), proven: its rule passes again,"
        " no other rule turned red, and the repo's own checks judged it (named in the commit).",
        "",
        "### Commits",
    ]
    for subject, text in proposal.commits:
        why = text.split("\n\n", 1)[0].replace("\n", " ")
        points = re.search(r"^Score: .*$", text, re.MULTILINE)
        lines.append(f"- **{subject}**{f' · {points.group(0)}' if points else ''}")
        if why and not why.startswith(("Score:", "Checked:", "unverified")):
            lines.append(f"  {why}")
    if proposal.notes:
        lines += ["", "### Left for a person", *(f"- {note}" for note in proposal.notes)]
    lines += [
        "",
        "Opened by kiln-bot (`kiln bot`), started again from the default branch every run:"
        " merge it as a whole, or close it to skip this week.",
    ]
    return "\n".join(lines) + "\n"


def run_bot(root: Path, *, update: bool, body_path: Path | None) -> Proposal:
    proposal = run(root, update=update)
    if proposal.changed:
        text = body(proposal)
        if body_path is not None:
            body_path.write_text(text, encoding="utf-8")
        else:
            print(text)
    return proposal
