"""A ticket's file name says what it is about: `<repo>-T-NN-<slug>.md`.

The slug comes from the title when the ticket is written and never follows it afterwards: the
number stays the ticket's identity, the slug only lets a reader of the folder see the subject.
`ion repo update` gives one to the tickets named `<repo>-T-NN.md`, and moves the links to them.
"""

import re
import subprocess
import unicodedata
from pathlib import Path

SLUG_WORDS = 6
SLUG_LENGTH = 48
# Words that make a title read well and a file name long.
FILLERS = frozenset(
    {"a", "an", "the", "of", "to", "in", "on", "for", "and", "by", "with", "its", "is", "be",
     "le", "la", "les", "l", "un", "une", "des", "de", "du", "d", "et", "en", "au", "aux",
     "pour", "par", "sur", "dans", "ce", "qui", "que", "s"}
)  # fmt: skip
BARE_NAME = re.compile(r"^(?P<stem>[a-z][a-z0-9-]*-T-\d+)\.md$")
LINKED_SUFFIXES = (".md", ".jinja")


def slug(title: str, words: int = SLUG_WORDS) -> str:
    """Lowercase ASCII words of the title, fillers dropped, short enough for a file name."""
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    # A version (`v0.4.1`) counts as one word.
    found = re.findall(r"[a-z0-9]+(?:\.[0-9]+)*", ascii_title.lower())
    meaningful = [word.replace(".", "-") for word in found if word not in FILLERS]
    kept: list[str] = []
    for word in meaningful[:words]:
        if len("-".join([*kept, word])) > SLUG_LENGTH:
            break
        kept.append(word)
    return "-".join(kept)


def file_name(name: str, number: int, title: str) -> str:
    """`<repo>-T-NN-<slug>.md`, or `<repo>-T-NN.md` for a title with no word left."""
    stem = f"{name}-T-{number:02d}"
    subject = slug(title)
    return f"{stem}-{subject}.md" if subject else f"{stem}.md"


def name_ticket_files(root: Path) -> int:
    """Tickets still named `<repo>-T-NN.md` get their slug; links to them follow. How many."""
    from ion_repo import tracker  # tracker names new tickets with this module's slug

    folder = root / tracker.TICKETS_DIR
    moves: dict[str, str] = {}
    for path in sorted(folder.glob("*-T-*.md")) if folder.is_dir() else []:
        bare = BARE_NAME.match(path.name)
        ticket = tracker.read_ticket(path) if bare else None
        if bare is None or ticket is None:
            continue
        new_name = f"{bare['stem']}-{slug(ticket.title)}.md" if slug(ticket.title) else path.name
        if new_name != path.name and not (folder / new_name).exists():
            path.rename(folder / new_name)
            moves[path.name] = new_name
    if moves:
        _move_links(root, moves)
    return len(moves)


def _move_links(root: Path, moves: dict[str, str]) -> None:
    """Every Markdown file of the repo that names a moved ticket file names its new one."""
    pattern = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, moves)) + r")(?=[)#\s`'\"]|$)")
    for relative in _tracked_files(root):
        path = root / relative
        if not path.is_file() or not relative.endswith(LINKED_SUFFIXES):
            continue
        text = path.read_text(encoding="utf-8")
        moved = pattern.sub(lambda found: moves[found[1]], text)
        if moved != text:
            path.write_text(moved, encoding="utf-8")


def _tracked_files(root: Path) -> list[str]:
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=False,
    )
    return listed.stdout.splitlines()
