"""`ion repo backlog`: the map of the backlog, computed and never written (ion-repo#T-456).

Production's version read from git, then each release in version order with its tickets (ID,
status, size, session, what they touch, title), then the tickets no release holds. Nothing here
lives in the index `README.md`: a state a command can compute drifts when written by hand.
"""

from pathlib import Path

from ion_repo import session, tracker
from ion_repo.shell import KilnError, capture

PRODUCTION_BRANCHES = ("origin/main", "main")
NO_VALUE = "—"


def production_version(root: Path) -> str:
    """The last tag reachable from `main` (the remote's first), `unknown` when git has none."""
    for branch in PRODUCTION_BRANCHES:
        try:
            tag = capture(
                ["git", "describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", branch], root
            )
        except KilnError:
            continue
        if tag.strip():
            return f"{tag.strip()} ({branch})"
    return "unknown (no tag on main)"


def draw(root: Path, only: str | None = None) -> list[str]:
    """The map's lines; `only` (a release's name or version) keeps that release alone."""
    planned = tracker.releases(root)
    chosen = [one for one in planned if only is None or only in _names(one)]
    if only is not None and not chosen:
        known = ", ".join(one.name for one in planned) or "none planned"
        raise KilnError(f"{only}: no such release (known: {known}).")
    by_number = {one.number: one for one in tracker.open_tickets(root)}
    lines = [f"Production: {production_version(root)}"] if only is None else []
    placed: set[int] = set()
    for release in chosen:
        lines += ["", _heading(release)]
        for line in release.tickets:
            number = tracker.RELEASE_TICKET.match(f"- {line}")
            ticket = by_number.get(int(number[1])) if number else None
            if ticket is not None:
                placed.add(ticket.number)
                lines.append(f"  {_row(ticket)}")
    if only is None:
        lines += _unplanned([one for number, one in by_number.items() if number not in placed])
    return lines[1:] if lines and not lines[0] else lines


def _names(release: tracker.Release) -> set[str]:
    return {release.name, release.version, f"v{release.version}"} - {""}


def _heading(release: tracker.Release) -> str:
    version = f"v{release.version}" if release.version else NO_VALUE
    if release.name == version:  # not named yet: the version says it
        return f"{version} · {release.title}"
    return f"{version} · {release.name} · {release.title}"


def _row(ticket: tracker.Ticket) -> str:
    """ID, priority and status, size, session, what it touches, title."""
    status = ticket.field("Status").split(" — ")[0]
    mark = tracker.PRIORITIES[ticket.priority]
    size = ticket.field("Effort") or "?"
    touches = ticket.line("Touches") or NO_VALUE
    head = f"{ticket.ticket_id} · {mark} {status} · {size} · {session.session_of(ticket)}"
    return f"{head} · {touches} · {ticket.title}"


def _unplanned(tickets: list[tracker.Ticket]) -> list[str]:
    """The tickets no release holds; one whose `Release` names a file that is not there says so."""
    if not tickets:
        return []
    lines = ["", "Unplanned"]
    for ticket in sorted(
        tickets, key=lambda one: (list(tracker.PRIORITIES).index(one.priority), one.number)
    ):
        lost = f" · release `{ticket.release}` not found" if ticket.release else ""
        lines.append(f"  {_row(ticket)}{lost}")
    return lines
