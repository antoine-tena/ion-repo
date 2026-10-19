"""Work tracking: moving the former `docs/a-faire/` (in French) to `docs/backlog/`.

`kiln update` calls it after Copier: the template laid down a blank `docs/backlog/`, which the
repo's tracking replaces, converted (headings, fields and statuses in English, `AF-NN` become
`T-NN`); the text of the tickets stays as written. Copier already deleted `docs/a-faire/`, even
changed: its content is read back from the last commit (`kiln update` starts from a clean tree).
"""

import re
import shutil
from pathlib import Path

from kiln.shell import KilnError, capture
from kiln.versions import ReleaseNotes

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


def migrate_legacy_backlog(root: Path) -> bool:
    """Converts `docs/a-faire/` to `docs/backlog/` if it still exists; says whether it did."""
    old_backlog = read_legacy(root, "a-faire.md")
    if old_backlog is None:
        return False
    backlog = root / BACKLOG_DIR
    backlog.mkdir(parents=True, exist_ok=True)
    fresh = backlog / "backlog.md"
    template_text = fresh.read_text() if fresh.exists() else ""
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
    next_free = re.search(r"Prochain libre : AF-(\d+)", text)
    compass = re.search(r"La boussole est \*\*(.+?)\*\*", text, re.S)
    started = re.search(r"Créée le\s+\*\*(.+?)\*\*", text)
    body = text[text.index("## 🔴") :] if "## 🔴" in text else text
    body = convert_tickets(body, dates)
    header = template_text[: template_text.index("## 🔴")] if "## 🔴" in template_text else ""
    if next_free:
        header = re.sub(r"Next free: T-\d+", f"Next free: T-{next_free[1]}", header)
    if compass:
        header = re.sub(r"North star: \*\*.*?\*\*", f"North star: **{compass[1]}**", header)
    if started:
        header = re.sub(r"Started on\s+\*\*.*?\*\*", f"Started on\n**{started[1]}**", header)
    return header + body


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
            lines += ["- **Type**: task", f"- **Status**: {status}"]
            lines.append(f"- **Opened**: {dates.get(ticket) or '—'}")
            continue
        line = line.replace("- **Effort** : ", "- **Effort**: ")
        line = line.replace(" · **Qui** : ", " · **Owner**: ")
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
    boxes = "\n".join(lines[first_box:]).strip("\n")
    body = intro.rstrip("\n") + "\n"
    return body + f"\n{boxes}\n" if boxes else body


# A line of a changelog entry: what each repo crossing that release must do after updating.
AFTER_UPDATING = "- **After updating**: "
CRITICAL_HEADING = "## 🔴 Critical\n"
NEXT_FREE = re.compile(r"Next free: T-(\d+)")


def add_after_update_ticket(root: Path, notes: list[ReleaseNotes], *, today: str) -> str | None:
    """A 🔴 ticket that gathers the `After updating` lines of the releases crossed: what only the
    team knows, to fill in right after the update. Its ID, or None when there is nothing to do
    (or no backlog to put it in)."""
    path = root / BACKLOG_DIR / "backlog.md"
    actions = [
        f"- [ ] {line.removeprefix(AFTER_UPDATING)} ({release.tag})"
        for release in reversed(notes)
        for line in release.lines
        if line.startswith(AFTER_UPDATING)
    ]
    text = path.read_text() if path.exists() else ""
    next_free = NEXT_FREE.search(text)
    title = f"Finish the kiln update to {notes[0].tag}" if notes else ""
    if not actions or next_free is None or CRITICAL_HEADING not in text or title in text:
        return None
    number = int(next_free[1])
    ticket_id = f"T-{number:02d}"
    ticket = "\n".join([
        f"### {ticket_id} · {title}",
        "- **Type**: task",
        "- **Status**: todo",
        f"- **Opened**: {today}",
        "- **Effort**: XS · **Owner**: — · **Due**: —",
        "- **Origin**: release notes of the kiln releases crossed (`kiln update`)",
        "",
        "What kiln cannot guess, to fill in right after the update (`/kiln:update`):",
        *actions,
    ])  # fmt: skip
    text = NEXT_FREE.sub(f"Next free: T-{number + 1:02d}", text, count=1)
    text = text.replace(CRITICAL_HEADING, f"{CRITICAL_HEADING}\n{ticket}\n", 1)
    path.write_text(text)
    return ticket_id
