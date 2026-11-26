"""The backlog folder `docs/backlog/`: one file per ticket, one file per release (ion-repo#T-453).

- `tickets/<repo>-T-NN-<slug>.md` (slug from the title, `ticket_names`): a `# <repo>#T-NN ·
  Title` heading, the fixed fields (`Type`, `Priority`, `Status`, `Opened`, `Effort`, `Origin`),
  then the details;
- `releases/<release-name>.md` (stable slug of the title, ion-repo#T-456): a `# Title` heading, a
  `- **Version**: vX.Y.Z` line (renumbering edits that line alone), why its tickets go together,
  a `## Handoff`. It does not list its tickets: each ticket names its release in a `Release` line,
  and `ion repo backlog` draws the map. A release not migrated yet (`# vX.Y.Z · Title`, ticket
  lines in the file) is still read;
- `README.md`: the short index (north star, next free ID, pointers), the project's own;
- `how-to.md`: the format, ion-repo's; `done.md`, `rejected.md`, `urgent.md` stay single files.

Every command reads tickets and releases here. A repo not converted yet (a single `backlog.md`,
`ion repo update` splits it) is still read, never written.
"""

import re
from dataclasses import dataclass, replace
from pathlib import Path

from packaging.version import InvalidVersion, Version

from ion_repo import ticket_names

BACKLOG_DIR = Path("docs/backlog")
TICKETS_DIR = BACKLOG_DIR / "tickets"
RELEASES_DIR = BACKLOG_DIR / "releases"
INDEX = BACKLOG_DIR / "README.md"
HOW_TO = BACKLOG_DIR / "how-to.md"
DONE = BACKLOG_DIR / "done.md"
LEGACY = BACKLOG_DIR / "backlog.md"
# Priority word and its mark, in the order of the former sections.
PRIORITIES = {"critical": "🔴", "important": "🟠", "normal": "🟡", "background": "⚪"}
REPO_PREFIX = r"[a-z][a-z0-9-]*#"
NEXT_FREE = re.compile(rf"Next free: (?:{REPO_PREFIX})?T-(\d+)")
HEADING = re.compile(rf"^#{{1,3}} ((?:{REPO_PREFIX})?T-(\d+)) · (.+)$", re.M)
RELEASE_HEADING = re.compile(r"^#{1,3} v(\d+\.\d+\.\d+) · (.+)$", re.M)
ANY_HEADING = re.compile(r"^#{1,3} (.+)$", re.M)
VERSION_LINE = re.compile(r"^- \*\*Version\*\*: *v?(\d+\.\d+\.\d+)[ \t]*$", re.M)
RELEASE_TICKET = re.compile(rf"- (?:{REPO_PREFIX})?T-(\d+)\b")
# What a release line adds after the ticket: its session's effort and the command that opens it.
SESSION_SUFFIX = re.compile(r" · (?:low|medium|high|xhigh|max) · `ion repo session [^`]+`$")


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    number: int
    title: str
    priority: str
    body: str
    path: Path

    def field(self, name: str) -> str:
        """A fixed field's value (`Status`, `Type`…), up to the next `·`; empty when absent."""
        found = re.search(rf"\*\*{name}\*\*: *([^\n·]*)", self.body)
        return found[1].strip() if found else ""

    def line(self, name: str) -> str:
        """A fixed line's whole text (`Touches`, which may hold a `·`); empty when absent."""
        found = re.search(rf"^- \*\*{name}\*\*: *(.*)$", self.body, re.M)
        return found[1].strip() if found else ""

    @property
    def release(self) -> str:
        """The name of the release the ticket is planned in (its `Release` line), or empty."""
        return self.field("Release")


@dataclass(frozen=True)
class Release:
    """`name` is the file's stem (`unified-front`, or `v3.0.0` before migration), what a ticket's
    `Release` line says; `version` is empty for a release with no number yet."""

    name: str
    version: str
    title: str
    why: str
    tickets: list[str]
    path: Path


def is_folder(root: Path) -> bool:
    """The repo's backlog is a folder: no former single `backlog.md` left."""
    return not (root / LEGACY).is_file()


def ticket_name(name: str, number: int, title: str = "") -> str:
    """File name of a ticket: `<repo>-T-NN-<slug>.md`, `<repo>-T-NN.md` without a title."""
    return ticket_names.file_name(name, number, title)


def priority_of(text: str) -> str:
    """The priority word of a `Priority` field or a former section heading, `normal` if none."""
    for word, mark in PRIORITIES.items():
        if mark in text or re.search(rf"\b{word}\b", text, re.I):
            return word
    return "normal"


def read_ticket(path: Path) -> Ticket | None:
    return read_ticket_text(path.read_text(encoding="utf-8"), path)


def read_ticket_text(text: str, path: Path) -> Ticket | None:
    heading = HEADING.search(text)
    if heading is None:
        return None
    body = text[heading.end() :]
    found = re.search(r"\*\*Priority\*\*: *([^\n]*)", body)
    priority = priority_of(found[1]) if found else "normal"
    return Ticket(heading[1], int(heading[2]), heading[3].strip(), priority, body, path)


def open_tickets(root: Path) -> list[Ticket]:
    """Every open ticket, by priority then number in the folder, in file order in a former
    `backlog.md`."""
    if not is_folder(root):
        return _legacy_tickets(root / LEGACY)
    folder = root / TICKETS_DIR
    found = [one for path in sorted(folder.glob("*.md")) if (one := read_ticket(path))]
    order = list(PRIORITIES)
    return sorted(found, key=lambda one: (order.index(one.priority), one.number))


def _legacy_tickets(path: Path) -> list[Ticket]:
    text = path.read_text(encoding="utf-8")
    tickets, priority = [], "normal"
    blocks = re.split(r"^(?=#{2,3} )", text, flags=re.M)
    for block in blocks:
        if block.startswith("## "):
            priority = priority_of(block.splitlines()[0])
            continue
        heading = HEADING.match(block)
        if heading is None:
            continue
        title, body = heading[3].strip(), block[heading.end() :]
        tickets.append(Ticket(heading[1], int(heading[2]), title, priority, body, path))
    return tickets


def find(root: Path, number: int) -> Ticket | None:
    """The open ticket of that number."""
    if is_folder(root):
        folder = root / TICKETS_DIR
        named = [*folder.glob(f"*-T-{number:02d}.md"), *folder.glob(f"*-T-{number:02d}-*.md")]
        for path in named:
            ticket = read_ticket(path)
            if ticket and ticket.number == number:
                return ticket
        return None
    return next((one for one in open_tickets(root) if one.number == number), None)


def next_free(root: Path) -> int | None:
    """The next free ticket number, written in the index (or the former `backlog.md`)."""
    path = root / (INDEX if is_folder(root) else LEGACY)
    if not path.is_file():
        return None
    found = NEXT_FREE.search(path.read_text(encoding="utf-8"))
    return int(found[1]) if found else None


def add_ticket(
    root: Path, name: str, title: str, fields: dict[str, str], details: str
) -> tuple[str, Path]:
    """A new ticket under the next free number, which moves on in the index: its ID and file.
    `fields` in order (`Type`, `Priority`…); a `Priority` given as a word gets its mark."""
    number = next_free(root)
    if number is None or not is_folder(root):
        raise ValueError("no backlog folder with a next free ID")
    ticket_id = f"{name}#T-{number:02d}"
    lines = [f"# {ticket_id} · {title}"]
    for key, value in fields.items():
        if key == "Priority" and value in PRIORITIES:
            value = f"{PRIORITIES[value]} {value}"
        lines.append(f"- **{key}**: {value}")
    path = root / TICKETS_DIR / ticket_name(name, number, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([*lines, "", details.strip(), ""]), encoding="utf-8")
    index = root / INDEX
    text = index.read_text(encoding="utf-8")
    index.write_text(NEXT_FREE.sub(f"Next free: {name}#T-{number + 1:02d}", text, count=1), "utf-8")
    return ticket_id, path


def releases(root: Path) -> list[Release]:
    """Every planned release, by version (those with no number last, by name): the folder's
    files, or the former `## 🚀 Releases` section (its other headings, what shipped, are not
    releases). A release holds the tickets that name it in their `Release` line, then those its
    own file still lists (not migrated yet) and no ticket names elsewhere."""
    found = _release_files(root) if is_folder(root) else _legacy_releases(root)
    tickets = open_tickets(root)
    named = {one.number: one.release for one in tickets if one.release}
    planned = []
    for release in sorted(found, key=_order):
        own = [
            f"{one.ticket_id} · {one.title} ({_size(one)})"
            for one in tickets
            if one.release == release.name
        ]
        listed = [line for line in release.tickets if _number_of(line) not in named]
        planned.append(replace(release, tickets=[*own, *listed]))
    return planned


def _order(release: Release) -> tuple[int, Version, str]:
    version = Version(release.version) if release.version else Version("0")
    return (0 if release.version else 1, version, release.name)


def _size(ticket: Ticket) -> str:
    return ticket.field("Effort").split()[0] if ticket.field("Effort") else "?"


def _number_of(line: str) -> int | None:
    found = RELEASE_TICKET.match(f"- {line}")
    return int(found[1]) if found else None


def _release_files(root: Path) -> list[Release]:
    folder = root / RELEASES_DIR
    paths = [path for path in folder.glob("*.md") if path.name != "README.md"]
    return [one for path in paths if (one := read_release(path))]


def _legacy_releases(root: Path) -> list[Release]:
    path = root / LEGACY
    text = path.read_text(encoding="utf-8")
    if "\n## 🚀 Releases\n" not in text:
        return []
    section = text.split("\n## 🚀 Releases\n", 1)[1].split("\n## ", 1)[0]
    blocks = re.split(r"^(?=### )", section, flags=re.M)
    found = [block for block in blocks if RELEASE_HEADING.match(block)]
    return [one for block in found if (one := _release(block, path))]


def release_by_ticket(root: Path) -> dict[int, str]:
    """Each planned ticket's release (`v3.3.0`, its name when it has no number), by ticket
    number."""
    planned: dict[int, str] = {}
    for one in releases(root):
        for line in one.tickets:
            number = _number_of(line)
            if number is not None:
                planned.setdefault(number, f"v{one.version}" if one.version else one.name)
    return planned


def display_name(root: Path, name: str, number: int, title: str) -> str:
    """`<repo>#T-NN_vX.Y.Z_<slug>`, computed and never stored: the release may change, the ID
    stays. Without a planned release, `<repo>#T-NN_<slug>`."""
    version = release_by_ticket(root).get(number, "")
    parts = [f"{name}#T-{number:02d}", version, ticket_names.slug(title)]
    return "_".join(part for part in parts if part)


def read_release(path: Path) -> Release | None:
    return _release(path.read_text(encoding="utf-8"), path)


def _release(text: str, path: Path) -> Release | None:
    """A release file: `# Title` and a `Version` line, or the former `# vX.Y.Z · Title` with its
    ticket lines. None for a text with no heading or a version that is not one."""
    old = RELEASE_HEADING.search(text)
    heading = old or ANY_HEADING.search(text)
    if heading is None:
        return None
    stated = VERSION_LINE.search(text)
    version = old[1] if old else (stated[1] if stated else "")
    title = (old[2] if old else heading[1]).strip()
    if version:
        try:
            Version(version)
        except InvalidVersion:
            return None
    lines = text[heading.end() :].strip("\n").splitlines()
    why = " ".join(
        line
        for line in lines
        if line and not line.startswith(("- ", "  ", "#")) and not VERSION_LINE.match(line)
    )
    tickets = [
        SESSION_SUFFIX.sub("", line.removeprefix("- "))
        for line in lines
        if RELEASE_TICKET.match(line)
    ]
    name = f"v{version}" if path.name == LEGACY.name else path.stem
    return Release(name, version, title, why, tickets, path)


def release_line(ticket: Ticket, effort: str, text: str = "") -> str:
    """A release's line for a ticket: ID, title, size, then its session's effort and command."""
    size = ticket.field("Effort").split()[0] if ticket.field("Effort") else "?"
    text = text or f"{ticket.ticket_id} · {ticket.title} ({size})"
    return f"- {text} · {effort} · `ion repo session {ticket.ticket_id}`"
