"""Work tracking: moving the former `docs/a-faire/` (in French) to `docs/backlog/`, and splitting
the former single `backlog.md` into open tickets and `done.md`.

`ion repo update` calls it after Copier: the template laid down a blank `docs/backlog/`, which the
repo's tracking replaces, converted (headings, fields and statuses in English, `AF-NN` become
`T-NN`); the text of the tickets stays as written. Copier already deleted `docs/a-faire/`, even
changed: its content is read back from the last commit (`ion repo update` starts from a clean tree).
"""

import re
import shutil
from collections.abc import Callable
from pathlib import Path

from ion_repo import tracker
from ion_repo.shell import KilnError, capture
from ion_repo.tickets import NEXT_FREE, repo_name
from ion_repo.versions import ReleaseNotes

LEGACY_DIR = Path("docs/a-faire")
BACKLOG_DIR = Path("docs/backlog")

STATUSES = (
    ("à faire", "todo"),
    ("en cours — branche", "in progress — branch"),
    ("bloqué — attend", "blocked — waiting for"),
    ("à vérifier", "to verify"),
)
SECTIONS = (
    ("## 🔴 Critique", "## 🔴 Critical"),
    ("## 🟠 Important", "## 🟠 Important"),
    ("## 🟡 Normal", "## 🟡 Normal"),
    ("## ⚪ Fond", "## ⚪ Background — long-running work, debt and ideas"),
    ("## ✅ Fait", "## ✅ Done"),
    ("### Journal", "### Log"),
)
REJECTED_HEADINGS = (
    ("# Écarté", "# Rejected"),
    ("## Exclu pour de bon", "## Ruled out for good"),
    ("## Refusé pour cette saison", "## Declined for now"),
    ("## Sans suite", "## Dropped"),
)
LEGACY_INTROS = (
    "Trois catégories, à ne pas confondre.",
    "Décisions définitives : à ne pas reproposer, même si un audit le recommande.",
)


# The header a converted `a-faire.md` gets: the template no longer has a single `backlog.md`.
LEGACY_HEADER = """# Backlog

Everything left to do, in a single list ordered by priority. How to write a ticket:
[README.md](README.md); closed tickets are in [done.md](done.md), what was turned down in
[rejected.md](rejected.md). **Nothing else is open.**

North star: **—**.

**Next free: T-01.**

---

## 🔴 Critical
"""


def migrate_legacy_backlog(root: Path) -> bool:
    """Converts `docs/a-faire/` to `docs/backlog/` if it still exists; says whether it did."""
    old_backlog = read_legacy(root, "a-faire.md")
    if old_backlog is None:
        return False
    backlog = root / BACKLOG_DIR
    backlog.mkdir(parents=True, exist_ok=True)
    fresh = backlog / "backlog.md"
    template_text = fresh.read_text() if fresh.exists() else LEGACY_HEADER
    dates = opened(root, (LEGACY_DIR / "a-faire.md").as_posix())
    fresh.write_text(convert_backlog(old_backlog, template_text, dates))
    if (rejected := read_legacy(root, "ecarte.md")) is not None:
        (backlog / "rejected.md").write_text(convert_rejected(rejected))
    if (urgent := read_legacy(root, "urgent.md")) is not None:
        urgent_path = backlog / "urgent.md"
        intro = urgent_path.read_text() if urgent_path.exists() else "# Urgent\n"
        urgent_path.write_text(convert_urgent(urgent, intro))
    legacy = root / LEGACY_DIR
    if legacy.exists():
        for name in ("a-faire.md", "ecarte.md", "urgent.md", "README.md"):
            (legacy / name).unlink(missing_ok=True)
        # Comptes rendus d'audit en cours : ils suivent le suivi.
        for leftover in legacy.iterdir():
            shutil.move(leftover, backlog / leftover.name)
        legacy.rmdir()
    return True


def read_legacy(root: Path, name: str) -> str | None:
    """A file of the former tracking: on disk, otherwise in the last commit."""
    path = root / LEGACY_DIR / name
    if path.exists():
        return path.read_text()
    try:
        return capture(["git", "show", f"HEAD:{(LEGACY_DIR / name).as_posix()}"], root) + "\n"
    except KilnError:
        return None


def opened(root: Path, path: str) -> dict[str, str]:
    """Opening date of each ticket: the first commit where its title appears."""
    dates: dict[str, str] = {}
    try:
        log = capture(["git", "log", "--reverse", "--format=commit %as", "-p", "--", path], root)
    except KilnError:
        return dates
    day = ""
    for line in log.splitlines():
        if line.startswith("commit "):
            day = line.removeprefix("commit ")
        elif match := re.match(r"\+### AF-(\d+) ·", line):
            dates.setdefault(match[1], day)
    return dates


def convert_backlog(text: str, template_text: str, dates: dict[str, str]) -> str:
    """`a-faire.md` to `backlog.md`: the template's header and how-to, tickets converted."""
    # The next free number: the one written, unless a ticket already took it.
    written = re.search(r"prochain libre : AF-(\d+)", text, re.I)
    listed = text[text.index("## 🔴") :] if "## 🔴" in text else text
    taken = [int(number) for number in re.findall(r"\bAF-(\d+)\b", listed)]
    next_free = max(int(written[1]) if written else 0, max(taken, default=0) + 1)
    compass = re.search(r"La boussole est[^*\n]*\*\*(.+?)\*\*", text, re.S)
    started = re.search(r"Créée le\s+\*\*(.+?)\*\*", text)
    body = text[text.index("## 🔴") :] if "## 🔴" in text else text
    body = convert_tickets(body, dates)
    header = template_text[: template_text.index("## 🔴")] if "## 🔴" in template_text else ""
    if taken:
        header = re.sub(r"(Next free: (?:.*?#)?)T-\d+", rf"\g<1>T-{next_free:02d}", header)
    if compass:
        header = re.sub(r"North star: \*\*.*?\*\*", f"North star: **{compass[1]}**", header)
    if started:
        header = re.sub(r"Started on\s+\*\*.*?\*\*", f"Started on\n**{started[1]}**", header)
    return _with_legacy_notes(header, text) + body


def _with_legacy_notes(header: str, text: str) -> str:
    """The paragraphs the former introduction added (the state of production…) after the
    template's own, which replaces its first one and the compass."""
    intro = text[: text.index("\n---")] if "\n---" in text else ""
    blocks = [block.strip() for block in intro.split("\n\n") if block.strip()]
    paragraphs = [block for block in blocks if not block.startswith("#")][1:]
    notes = [
        re.sub(r"\bAF-(\d+)\b", r"T-\1", block)
        for block in paragraphs
        if not block.startswith("La boussole est")
    ]
    if not notes or "\n---" not in header:
        return header
    cut = header.index("\n---")
    return header[:cut].rstrip("\n") + "\n\n" + "\n\n".join(notes) + "\n" + header[cut:]


def convert_tickets(text: str, dates: dict[str, str]) -> str:
    lines: list[str] = []
    ticket = ""
    for line in text.splitlines():
        for old, new in SECTIONS:
            if line.startswith(old):
                line = new
        if match := re.match(r"### AF-(\d+) ·", line):
            ticket = match[1]
        elif line.startswith("- **État** : "):
            status = line.removeprefix("- **État** : ")
            for old, new in STATUSES:
                if status.startswith(old):
                    status = new + status.removeprefix(old)
            status = re.sub(r"depuis le ", "since ", status)
            status = re.sub(r"\bAF-(\d+)\b", r"T-\1", status)
            lines += ["- **Type**: task", f"- **Status**: {status}"]
            lines.append(f"- **Opened**: {dates.get(ticket) or '—'}")
            continue
        line = line.replace("- **Effort** : ", "- **Effort**: ")
        line = line.replace(" · **Qui** : ", " · **Owner**: ")
        # An agent is not an owner: its tickets become free.
        line = line.replace(" · **Owner**: Claude · ", " · **Owner**: — · ")
        line = line.replace(" · **Échéance** : ", " · **Due**: ")
        line = line.replace("- **Origine** : ", "- **Origin**: ")
        if line.startswith("Une ligne par entrée terminée"):
            line = "One line per closed ticket, most recent first:"
        line = line.replace(
            "`- **AAAA-MM-JJ** · AF-NN · Titre — ce qui a été fait (branche)`.",
            "`- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.",
        )
        lines.append(re.sub(r"\bAF-(\d+|NN)\b", r"T-\1", line))
    return "\n".join(lines) + "\n"


def convert_rejected(text: str) -> str:
    lines = []
    for line in text.splitlines():
        for old, new in REJECTED_HEADINGS:
            if line == old:
                line = new
        if line == LEGACY_INTROS[0]:
            line = "Three kinds, not to be confused."
        elif line == LEGACY_INTROS[1]:
            line = "Final decisions: do not propose them again, even if an audit recommends it."
        lines.append(re.sub(r"\bAF-(\d+)\b", r"T-\1", line))
    return "\n".join(lines) + "\n"


def convert_urgent(text: str, intro: str) -> str:
    """The checkboxes of `urgent.md` under the template's introduction, in English."""
    lines = text.splitlines()
    first_box = next((i for i, line in enumerate(lines) if line.startswith("- [")), len(lines))
    boxes = re.sub(r"\bAF-(\d+)\b", r"T-\1", "\n".join(lines[first_box:]).strip("\n"))
    body = intro.rstrip("\n") + "\n"
    return body + f"\n{boxes}\n" if boxes else body


DONE_HEADING = "## ✅ Done"
HOW_TO_HEADING = "## How to use"
FORMER_INTRO = re.compile(
    r'What is done is in the "✅ Done" section at\s+the bottom; what was turned\s+down is in'
    r"\s+\[rejected\.md\]\(rejected\.md\)\."
)
LOG_PREAMBLE = ("### Log", "One line per closed ticket", "`- **YYYY-MM-DD** · T-NN")


def split_backlog(root: Path, *, from_disk: bool = False) -> bool:
    """The former single `backlog.md` (how-to at the top, "✅ Done" log at the bottom) split:
    the open tickets stay, the log goes to `done.md`, the how-to to `README.md` (the template's
    has one; an adopted repo's own, kept, gets the repo's how-to at its end).
    Read from the last commit, as the repo kept it: Copier's merge of the template's new layout
    into it leaves the log loose at the bottom (`from_disk` after the move from `docs/a-faire/`,
    written this same run). Says whether it split."""
    path = root / BACKLOG_DIR / "backlog.md"
    if from_disk:
        text = path.read_text() if path.exists() else None
    else:
        try:
            text = capture(["git", "show", f"HEAD:{(BACKLOG_DIR / 'backlog.md').as_posix()}"], root)
        except KilnError:
            text = None
    if text is None or DONE_HEADING not in text:
        return False
    open_part, log = text.split(f"\n{DONE_HEADING}", 1)
    path.write_text(_open_backlog(open_part))
    _keep_how_to(root / BACKLOG_DIR / "README.md", _how_to(open_part))
    entries = "\n".join(
        line for line in log.splitlines()[1:] if not line.startswith(LOG_PREAMBLE)
    ).strip()
    done = root / BACKLOG_DIR / "done.md"
    intro = done.read_text() if done.exists() else "# Done\n"
    done.write_text(intro.rstrip("\n") + "\n" + (f"\n{entries}\n" if entries else ""))
    return True


def _how_to(text: str) -> str:
    """The how-to section of a former `backlog.md`, or an empty string."""
    if HOW_TO_HEADING not in text:
        return ""
    start = text.index(HOW_TO_HEADING)
    end = text.find("\n## ", start)
    return text[start : end if end != -1 else len(text)].rstrip().removesuffix("---").rstrip()


def _keep_how_to(readme: Path, how_to: str) -> None:
    """The how-to appended to a `README.md` that has none: never lost with the split."""
    if not how_to or not readme.exists() or HOW_TO_HEADING in readme.read_text():
        return
    readme.write_text(readme.read_text().rstrip("\n") + f"\n\n{how_to}\n")


def _open_backlog(text: str) -> str:
    """The open part of a former `backlog.md`: its how-to removed, the next free ID moved up to
    the header, the introduction pointing to the new files."""
    next_free = NEXT_FREE.search(text)
    if HOW_TO_HEADING in text:
        start = text.index(HOW_TO_HEADING)
        end = text.find("\n## ", start)
        text = text[:start] + (text[end + 1 :] if end != -1 else "")
    text = re.sub(r"\n---\n\s*\n---\n", "\n---\n", text)
    text = FORMER_INTRO.sub(
        "Closed tickets are in [done.md](done.md), what was turned down in\n"
        "[rejected.md](rejected.md); how to write a ticket: [README.md](README.md).",
        text,
    )
    if next_free and not NEXT_FREE.search(text) and "\n---" in text:
        cut = text.index("\n---")
        text = f"{text[:cut].rstrip()}\n\n**Next free: T-{next_free[1]}.**\n{text[cut:]}"
    return text.rstrip().removesuffix("---").rstrip() + "\n"


# A line of a changelog entry: what each repo crossing that release must do after updating.
AFTER_UPDATING = "- **After updating**: "


def add_after_update_ticket(root: Path, notes: list[ReleaseNotes], *, today: str) -> str | None:
    """A 🔴 ticket that gathers the `After updating` lines of the releases crossed: what only the
    team knows, to fill in right after the update. Its ID, or None when there is nothing to do
    (or no backlog folder to put it in)."""
    actions = [
        f"- [ ] {line.removeprefix(AFTER_UPDATING)} ({release.tag})"
        for release in reversed(notes)
        for line in release.lines
        if line.startswith(AFTER_UPDATING)
    ]
    title = f"Finish the ion-repo update to {notes[0].tag}" if notes else ""
    if not actions or not tracker.is_folder(root) or tracker.next_free(root) is None:
        return None
    if any(one.title == title for one in tracker.open_tickets(root)):
        return None
    fields = {
        "Type": "task",
        "Priority": "critical",
        "Status": "todo",
        "Opened": today,
        "Effort": "XS · **Owner**: — · **Due**: —",
        "Origin": "release notes of the ion-repo releases crossed (`ion repo update`)",
    }
    details = "\n".join([
        "What ion-repo cannot guess, to fill in right after the update (`/repo:update`):",
        *actions,
    ])  # fmt: skip
    ticket_id, _ = tracker.add_ticket(root, repo_name(root), title, fields, details)
    return ticket_id


# The single `backlog.md` split into a folder (ion-repo#T-453).
RELEASES_MARK = "🚀"
HOW_TO_TITLE = "How to use"
SINGLE_LIST = re.compile(r"in a single\s+list ordered by\s+priority")
HOW_TO_LINK = re.compile(r"How to write a\s+ticket:\s+\[README\.md\]\(README\.md\)")
RELATIVE_LINK = re.compile(r"\]\((?!https?:|mailto:|#|/)([^)\s]+)\)")
ANCHOR_LINK = re.compile(r"\]\(#([^)\s]+)\)")
TEMPLATE_README = "What is left to do on"


def split_into_folder(root: Path) -> bool:
    """The single `backlog.md` (on disk, else in the last commit: Copier may have deleted it)
    becomes `tickets/`, `releases/`, an index `README.md` and a file per other section; no line
    lost, links still pointing where they did. Says whether it split."""
    from ion_repo import session  # session needs shipping, which needs this module

    path = root / tracker.LEGACY
    text = path.read_text("utf-8") if path.is_file() else _from_head(root, tracker.LEGACY)
    if text is None:
        return False
    name = repo_name(root)
    parts = re.split(r"^(?=## )", text, flags=re.M)
    header, sections = _without_rule(parts[0]), parts[1:]
    tickets: dict[int, tuple[str, str]] = {}  # number: (priority, block)
    release_blocks: list[str] = []
    plan_notes: list[str] = []
    loose: list[str] = []
    extras: dict[str, tuple[str, str]] = {}  # file: (title, body)
    for section in sections:
        title, _, body = section.partition("\n")
        title, body = title.removeprefix("## ").strip(), _without_rule(body)
        if RELEASES_MARK in title:
            blocks = re.split(r"^(?=### )", body, flags=re.M)
            plan_notes += [blocks[0].strip()] if blocks[0].strip() else []
            for block in blocks[1:]:
                if tracker.RELEASE_HEADING.match(block):
                    release_blocks.append(block)
                else:
                    plan_notes.append(re.sub(r"^### ", "## ", block.strip()))
        elif _is_priority(title):
            _collect_tickets(body, tracker.priority_of(title), title, tickets, loose)
        else:
            extras[_extra_file(root, title, extras)] = (title, body)
    anchors = {_anchor(title): file for file, (title, _) in extras.items()}
    anchors[_anchor("🚀 Releases")] = "README.md#releases"
    written: dict[Path, str] = {}
    open_tickets: dict[int, tracker.Ticket] = {}
    for number, (priority, block) in tickets.items():
        file = root / tracker.TICKETS_DIR / tracker.ticket_name(name, number)
        written[file] = _links(_ticket_file(block, priority), anchors, 1)
        if ticket := tracker.read_ticket_text(written[file], file):
            open_tickets[number] = ticket
    releases = []
    for block in release_blocks:
        heading = tracker.RELEASE_HEADING.match(block)
        assert heading is not None
        version, title = heading[1], heading[2].strip()
        body = block.rstrip().splitlines()[1:]
        while body and not body[0].strip():
            body.pop(0)
        lines = [_release_line(line, name, open_tickets, session.effort_of) for line in body]
        content = "\n".join([f"# v{version} · {title}", "", *lines]).rstrip() + "\n"
        written[root / tracker.RELEASES_DIR / f"v{version}.md"] = _links(content, anchors, 1)
        releases.append(f"- [v{version} · {title}](releases/v{version}.md)")
    if plan_notes:
        notes = "\n\n".join(["# Releases", *plan_notes]) + "\n"
        written[root / tracker.RELEASES_DIR / "README.md"] = _links(notes, anchors, 1)
    for file, (title, body) in extras.items():
        promoted = re.sub(r"^#(#{2,}) ", r"\1 ", body, flags=re.M)
        written[root / tracker.BACKLOG_DIR / file] = f"# {title}\n{promoted.rstrip()}\n"
    index = _index(header, releases, bool(plan_notes), extras, loose)
    written[root / tracker.INDEX] = _links(index, anchors, 0) + _former_readme(root)
    for file, content in written.items():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")
    path.unlink(missing_ok=True)
    return True


def _from_head(root: Path, relative: Path) -> str | None:
    try:
        return capture(["git", "show", f"HEAD:{relative.as_posix()}"], root) + "\n"
    except KilnError:
        return None


def _without_rule(text: str) -> str:
    """A part of the former file without its closing `---` separator."""
    return re.sub(r"\n---\s*$", "\n", text.rstrip()) + "\n"


def _is_priority(title: str) -> bool:
    first = title.split()[0] if title.split() else ""
    return first in tracker.PRIORITIES.values() or first.lower() in tracker.PRIORITIES


def _collect_tickets(
    body: str,
    priority: str,
    title: str,
    tickets: dict[int, tuple[str, str]],
    loose: list[str],
) -> None:
    last = None
    for block in re.split(r"^(?=### )", body, flags=re.M):
        if heading := tracker.HEADING.match(block):
            last = int(heading[2])
            if last in tickets:
                raise KilnError(f"T-{last}: two tickets under that number, split by hand first.")
            tickets[last] = (priority, block)
        elif last is not None:  # a `###` inside a ticket stays in it
            tickets[last] = (priority, tickets[last][1] + block)
        elif block.strip():
            loose.append(f"## {title}\n\n{block.strip()}")


def _ticket_file(block: str, priority: str) -> str:
    """A former `### ` ticket as its own file: `# ` heading, the priority as a field."""
    lines = block.rstrip().splitlines()
    lines[0] = "# " + lines[0].removeprefix("### ")
    field = f"- **Priority**: {tracker.PRIORITIES[priority]} {priority}"
    after = next((i for i, line in enumerate(lines) if line.startswith("- **Type**:")), None)
    before = next((i for i, line in enumerate(lines) if line.startswith("- **")), 1)
    lines.insert(after + 1 if after is not None else before, field)
    return "\n".join(lines) + "\n"


def _release_line(
    line: str,
    name: str,
    tickets: dict[int, tracker.Ticket],
    effort_of: Callable[[tracker.Ticket], str],
) -> str:
    """A release's ticket line, with its session's effort and the command that opens it."""
    found = tracker.RELEASE_TICKET.match(line)
    if not found or tracker.SESSION_SUFFIX.search(line):
        return line
    ticket = tickets.get(int(found[1]))
    if ticket is None or not re.match(rf"- (?:{re.escape(name)}#)?T-", line):
        return line
    return tracker.release_line(ticket, effort_of(ticket), line.removeprefix("- "))


def _extra_file(root: Path, title: str, taken: dict[str, tuple[str, str]]) -> str:
    """The file of a section that is neither tickets nor releases (a vision, a how-to)."""
    how_to = tracker.HOW_TO.name
    if HOW_TO_TITLE in title and not (root / tracker.HOW_TO).exists() and how_to not in taken:
        return how_to
    slug = _anchor(title).strip("-") or "notes"
    return f"{slug}.md" if f"{slug}.md" not in taken else f"{slug}-{len(taken)}.md"


def _anchor(title: str) -> str:
    """GitHub's anchor of a heading: lower case, punctuation and emoji dropped, spaces dashed."""
    return re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")


def _links(text: str, anchors: dict[str, str], depth: int) -> str:
    """Links of a text moved `depth` folders down: relative ones climb back, anchors to a former
    section point to its file."""
    up = "../" * depth
    if depth:
        text = RELATIVE_LINK.sub(lambda found: f"]({up}{found[1]})", text)
    return ANCHOR_LINK.sub(
        lambda found: f"]({up}{anchors[found[1]]})" if found[1] in anchors else found[0], text
    )


def _index(
    header: str,
    releases: list[str],
    has_notes: bool,
    extras: dict[str, tuple[str, str]],
    loose: list[str],
) -> str:
    """The short index: the former header, the releases in order, the other files."""
    header = SINGLE_LIST.sub(
        "one file per ticket in [tickets/](tickets/), one per planned release in\n"
        "[releases/](releases/)",
        header,
    )
    header = HOW_TO_LINK.sub("How to write a ticket: [how-to.md](how-to.md)", header)
    lines = [header.rstrip(), "", "Open tickets, one line each: `ion repo backlog`.", ""]
    lines += ["## Releases", ""]
    lines += releases or ["None planned yet (`/repo:backlog plan`)."]
    if has_notes:
        lines += ["", "The plan's notes and what shipped: [releases/](releases/README.md)."]
    if extras:
        lines += ["", "## More", ""]
        lines += [f"- [{title}]({file})" for file, (title, _) in extras.items()]
    for block in loose:
        lines += ["", block]
    return "\n".join(lines) + "\n"


def _former_readme(root: Path) -> str:
    """What a former `README.md` of the folder holds beyond the template's how-to (an adopted
    repo's own), kept under the index."""
    path = root / tracker.INDEX
    if not path.is_file():
        return ""
    text = path.read_text("utf-8")
    if TEMPLATE_README in text[:300] or tracker.NEXT_FREE.search(text):
        return ""  # the template's former how-to, or its fresh index
    return "\n---\n\n" + re.sub(r"^#(?= )", "##", text, count=1, flags=re.M)
