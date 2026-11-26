"""`ion repo session <repo>#T-NN…`: the one line that opens a Claude Code session on tickets.

The ticket is the brief, so the command only carries what launching needs: the repo's main tree,
the model, the effort, a session name, and a short prompt that sends the session to the ticket,
its worktree, its start in the backlog and its merge. Model, effort and branch come from the
ticket's optional `- **Session**: <model> <effort>[, <branch>]` line (`sonnet` by default; the
former `· **Session**: medium, fix/two-coaches` on the Effort line is still read), else from its
size and type. What only holds at launch (another session on the same files) is a `--note`, never
written in the ticket: it would go stale.

`--subagent` prints instead the brief an orchestrator gives the `ticket` agent (a Sonnet subagent
that starts cold): no merge, no question to the user, the report the agent defines at the end.
"""

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from ion_repo import tracker
from ion_repo.shell import KilnError
from ion_repo.shipping import main_tree
from ion_repo.tickets import repo_name

# `claude --model` takes these aliases: the command never pins a model's ID.
MODELS = ("sonnet", "opus")
DEFAULT_MODEL = "sonnet"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
EFFORT_BY_SIZE = {"XS": "low", "S": "low", "M": "medium", "L": "medium"}
DEFAULT_EFFORT = "low"
BRANCH_TYPE = {"bug": "fix", "improvement": "feat", "idea": "feat", "task": "chore"}
DEFAULT_BRANCH_TYPE = "chore"
# A branch says what it holds (`fix/t15-intitules-modules-abimes-jeux-donnees`), never `fix/t15`
# alone, which reads as nothing in `git branch` or a merge commit.
BRANCH_WORDS = 5
NOT_SLUG = re.compile(r"[^a-z0-9]+")
# Words that carry nothing in a branch name, French and English; single letters too.
STOP_WORDS = frozenset(
    [
        "le",
        "la",
        "les",
        "de",
        "des",
        "du",
        "un",
        "une",
        "et",
        "en",
        "au",
        "aux",
        "dans",
        "sur",
        "pour",
        "par",
        "est",
        "sont",
        "ne",
        "pas",
        "the",
        "an",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "is",
        "are",
        "be",
        "by",
        "with",
    ]
)
DONE = tracker.DONE.as_posix()
NUMBER = re.compile(r"^(?:[a-z][a-z0-9-]*#)?T-(\d+)$")
FIELD = r"- \*\*{}\*\*: *([^\n·]*)"
SESSION = re.compile(
    rf"(?:^- | · )\*\*Session\*\*: *(?:({'|'.join(MODELS)}) +)?({'|'.join(EFFORTS)})"
    r"(?:, *([a-z]+/[a-z0-9./-]+))?",
    re.M,
)
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
    path: str
    model: str = DEFAULT_MODEL


def find_ticket(root: Path, wanted: str) -> Ticket:
    """The open ticket `wanted` (`T-12`, `12` or `<repo>#T-12`) read from the backlog."""
    number = _number(wanted)
    name = repo_name(root)
    if not (root / tracker.BACKLOG_DIR).is_dir():
        raise KilnError(f"No {tracker.BACKLOG_DIR.as_posix()}/ here.")
    found = tracker.find(root, number)
    if found is None:
        done = root / DONE
        closed = done.is_file() and re.search(rf"#T-0*{number} ·", done.read_text("utf-8"))
        why = f"closed, see {DONE}" if closed else "not an open ticket of the backlog"
        raise KilnError(f"{name}#T-{number:02d}: {why}.")
    path = found.path.relative_to(root).as_posix()
    return _ticket(f"{name}#T-{number:02d}", number, found.title, found.body, path)


def _number(wanted: str) -> int:
    found = NUMBER.match(wanted if "T-" in wanted else f"T-{wanted}")
    if found is None:
        raise KilnError(f"{wanted}: not a ticket ID (T-12, 12 or <repo>#T-12).")
    return int(found[1])


def _ticket(ticket_id: str, number: int, title: str, block: str, path: str = "") -> Ticket:
    kind = re.search(FIELD.format("Type"), block)
    branch_type = BRANCH_TYPE.get(kind[1].strip() if kind else "", DEFAULT_BRANCH_TYPE)
    session = SESSION.search(block)
    size = SIZE.search(block)
    effort = session[2] if session else EFFORT_BY_SIZE.get(size[1] if size else "", DEFAULT_EFFORT)
    branch = session[3] if session and session[3] else _branch(branch_type, number, title)
    model = session[1] if session and session[1] else DEFAULT_MODEL
    return Ticket(ticket_id, number, title, effort, branch, path, model)


def _branch(branch_type: str, number: int, title: str) -> str:
    """`<type>/tNN-<first words of the title>`, in lowercase ASCII."""
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    words = [w for w in NOT_SLUG.sub(" ", ascii_title.lower()).split() if _carries(w)]
    words = words[:BRANCH_WORDS]
    return "-".join([f"{branch_type}/t{number:02d}", *words])


def _carries(word: str) -> bool:
    return len(word) > 1 and word not in STOP_WORDS


def effort_of(ticket: tracker.Ticket) -> str:
    """The effort of the session that works a ticket: its `Session` field, else its size."""
    return _ticket(ticket.ticket_id, ticket.number, ticket.title, ticket.body).effort


def session_of(ticket: tracker.Ticket) -> str:
    """`<model> <effort>` of the session that works a ticket, as its `Session` line or its size
    says."""
    one = _ticket(ticket.ticket_id, ticket.number, ticket.title, ticket.body)
    return f"{one.model} {one.effort}"


def command(
    root: Path, wanted: list[str], *, effort: str | None = None, notes: list[str] | None = None
) -> str:
    """The line to paste: `cd` to the main tree, then `claude` with name, effort and prompt."""
    tickets = [find_ticket(root, one) for one in wanted]
    chosen = effort or max((one.effort for one in tickets), key=EFFORTS.index)
    model = max((one.model for one in tickets), key=MODELS.index)
    folder = _home_relative(main_tree(root))
    return (
        f"cd {folder} && claude --model {model} --effort {chosen}"
        f" --name {_quote(_name(root, tickets))} {_quote(prompt(tickets, notes or []))}"
    )


def _name(root: Path, tickets: list[Ticket]) -> str:
    """One ticket by its display name, several by their IDs."""
    if len(tickets) > 1:
        return " ".join(one.ticket_id for one in tickets)
    one = tickets[0]
    return tracker.display_name(root, repo_name(root), one.number, one.title)


def prompt(tickets: list[Ticket], notes: list[str]) -> str:
    """Sends the session to its tickets, which hold the brief; the notes add what holds now."""
    named = ", then ".join(f"{one.ticket_id} ({one.title}) from {one.path}" for one in tickets)
    order = " in that order, one worktree and one merge per ticket" if len(tickets) > 1 else ""
    steps = "; ".join(
        f"for {one.ticket_id}: /repo:worktree {one.branch},"
        f" then /repo:backlog start {one.ticket_id}"
        for one in tickets
    )
    lines = [
        f"Work on {named}{order}. The ticket is the brief: read it whole and its"
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


def brief(
    root: Path, wanted: str, *, effort: str | None = None, notes: list[str] | None = None
) -> str:
    """What an orchestrator gives the `ticket` agent for one ticket: where it is, which session
    works it, what to leave alone, and the report to end with. The agent's own rules
    (`~/.claude/agents/ticket.md`) hold the rest; nothing here merges or asks."""
    ticket = find_ticket(root, wanted)
    tree = main_tree(root)
    lines = [
        f"Work the ticket {ticket.ticket_id} · {ticket.title}, and no other.",
        f"Session: {ticket.model}, effort {effort or ticket.effort}.",
        f"File: {tree / ticket.path}. Read it whole, then its Origin; its Files section lists the"
        " paths to open: go straight to them and explore no further than you must.",
        f"Branch {ticket.branch}, in its own worktree (/repo:worktree {ticket.branch}), then mark"
        f" the ticket started (/repo:backlog start {ticket.ticket_id}).",
        "Tick each box as it is done, commit each step on the branch. A bug starts with a failing"
        " test that reproduces it. The ticket's Done when section is what is checked after you.",
        "What the ticket leaves open (a value, a wording, a behaviour users see) you do not guess:"
        " stop and report it as a question.",
        "The merge, the release and every deploy are not yours: leave the branch committed and"
        " clean.",
        *(f"Note: {note}" for note in notes or []),
        "End with `ion repo check` in the worktree, then your report in at most 15 lines: status"
        " (done, partial or blocked), branch and last commit, check verdict, tests added,"
        " deviations from the ticket, questions for the user.",
    ]
    return "\n".join(lines)


def session(
    root: Path,
    wanted: list[str],
    effort: str | None = None,
    notes: list[str] | None = None,
    *,
    subagent: bool = False,
) -> None:
    if subagent:
        if len(wanted) != 1:
            raise KilnError("--subagent takes one ticket: a subagent never works a second.")
        print(brief(root, wanted[0], effort=effort, notes=notes))
        return
    print(command(root, wanted, effort=effort, notes=notes))
