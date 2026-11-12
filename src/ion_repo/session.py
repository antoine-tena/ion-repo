"""`ion repo session <repo>#T-NN…`: the one line that opens a Claude Code session on tickets.

The ticket is the brief, so the command only carries what launching needs: the repo's main tree,
the model, the effort, a session name, and a short prompt that sends the session to the ticket,
its worktree, its start in the backlog and its merge. Effort and branch come from the ticket's
optional `**Session**` field (`· **Session**: medium, fix/two-coaches` on the Effort line), else
from its size and type. What only holds at launch (another session on the same files) is a
`--note`, never written in the ticket: it would go stale.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from ion_repo.shell import KilnError
from ion_repo.shipping import main_tree
from ion_repo.tickets import repo_name

MODEL = "claude-opus-5-5"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
EFFORT_BY_SIZE = {"XS": "low", "S": "low", "M": "medium", "L": "medium"}
DEFAULT_EFFORT = "low"
BRANCH_TYPE = {"bug": "fix", "improvement": "feat", "idea": "feat", "task": "chore"}
DEFAULT_BRANCH_TYPE = "chore"
BACKLOG = "docs/backlog/backlog.md"
DONE = "docs/backlog/done.md"
NUMBER = re.compile(r"^(?:[a-z][a-z0-9-]*#)?T-(\d+)$")
FIELD = r"- \*\*{}\*\*: *([^\n·]*)"
SESSION = re.compile(rf"\*\*Session\*\*: *({'|'.join(EFFORTS)})(?:, *([a-z]+/[a-z0-9./-]+))?")
SIZE = re.compile(r"\*\*Effort\*\*: *(XS|S|M|L)\b")
# Single quotes hold the prompt whole in bash (no `$`, `!` nor backtick read); an apostrophe
# inside becomes a typographic one, which a model reads the same.
APOSTROPHE = "\u2019"


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    number: int
    title: str
    effort: str
    branch: str


def find_ticket(root: Path, wanted: str) -> Ticket:
    """The open ticket `wanted` (`T-12`, `12` or `<repo>#T-12`) read from the backlog."""
    number = _number(wanted)
    name = repo_name(root)
    backlog = root / BACKLOG
    if not backlog.is_file():
        raise KilnError(f"No {BACKLOG} here.")
    text = backlog.read_text(encoding="utf-8")
    heading = re.search(rf"^### (?:{re.escape(name)}#)?T-0*{number} · (.+)$", text, re.M)
    if heading is None:
        done = root / DONE
        closed = done.is_file() and re.search(rf"#T-0*{number} ·", done.read_text("utf-8"))
        why = f"closed, see {DONE}" if closed else f"not an open ticket of {BACKLOG}"
        raise KilnError(f"{name}#T-{number:02d}: {why}.")
    following = re.search(r"^##", text[heading.end() :], re.M)
    block = text[heading.end() : heading.end() + following.start() if following else None]
    return _ticket(f"{name}#T-{number:02d}", number, heading[1].strip(), block)


def _number(wanted: str) -> int:
    found = NUMBER.match(wanted if "T-" in wanted else f"T-{wanted}")
    if found is None:
        raise KilnError(f"{wanted}: not a ticket ID (T-12, 12 or <repo>#T-12).")
    return int(found[1])


def _ticket(ticket_id: str, number: int, title: str, block: str) -> Ticket:
    kind = re.search(FIELD.format("Type"), block)
    branch_type = BRANCH_TYPE.get(kind[1].strip() if kind else "", DEFAULT_BRANCH_TYPE)
    session = SESSION.search(block)
    size = SIZE.search(block)
    effort = session[1] if session else EFFORT_BY_SIZE.get(size[1] if size else "", DEFAULT_EFFORT)
    branch = session[2] if session and session[2] else f"{branch_type}/t{number:02d}"
    return Ticket(ticket_id, number, title, effort, branch)


def command(
    root: Path, wanted: list[str], *, effort: str | None = None, notes: list[str] | None = None
) -> str:
    """The line to paste: `cd` to the main tree, then `claude` with name, effort and prompt."""
    tickets = [find_ticket(root, one) for one in wanted]
    chosen = effort or max((one.effort for one in tickets), key=EFFORTS.index)
    folder = _home_relative(main_tree(root))
    return (
        f"cd {folder} && claude --model {MODEL} --effort {chosen}"
        f" --name {_quote(_name(tickets))} {_quote(prompt(tickets, notes or []))}"
    )


def _name(tickets: list[Ticket]) -> str:
    numbers = " ".join(f"T-{one.number:02d}" for one in tickets)
    return f"{numbers} {tickets[0].title}" if len(tickets) == 1 else numbers


def prompt(tickets: list[Ticket], notes: list[str]) -> str:
    """Sends the session to its tickets, which hold the brief; the notes add what holds now."""
    named = ", then ".join(f"{one.ticket_id} ({one.title})" for one in tickets)
    order = " in that order, one worktree and one merge per ticket" if len(tickets) > 1 else ""
    steps = "; ".join(
        f"for {one.ticket_id}: /repo:worktree {one.branch},"
        f" then /repo:backlog start {one.ticket_id}"
        for one in tickets
    )
    lines = [
        f"Work on {named} from {BACKLOG}{order}. The ticket is the brief: read it whole and its"
        " Origin before coding.",
        f"Start {steps}.",
        "A bug starts with a failing test that reproduces it. Tick each box as it is done.",
        "Ask the user before anything that changes production data or needs their decision.",
        "End with /repo:merge, the ticket closed or its open boxes left in the backlog.",
        *notes,
    ]
    return " ".join(lines)


def _home_relative(folder: Path) -> str:
    home = Path.home()
    return (
        f"~/{folder.relative_to(home).as_posix()}" if folder.is_relative_to(home) else str(folder)
    )


def _quote(text: str) -> str:
    return "'" + text.replace("'", APOSTROPHE) + "'"


def session(
    root: Path, wanted: list[str], effort: str | None = None, notes: list[str] | None = None
) -> None:
    print(command(root, wanted, effort=effort, notes=notes))
