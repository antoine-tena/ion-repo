"""Releases by name, tickets that say their release (ion-repo#T-456), migrated by `ion repo update`.

Before: `releases/vX.Y.Z.md`, a `# vX.Y.Z · Title` heading and one line per ticket, the index
listing every release by hand, a session's effort ending a ticket's Effort line.
After: `releases/<slug>.md` (the slug of the title, kept for good), a `# Title` heading and a
`- **Version**: vX.Y.Z` line (renumbering edits that line alone), no ticket line; each ticket
holds `- **Release**: <slug>` and its own `- **Session**: <model> <effort>` line; the index no
longer lists the releases (`ion repo backlog` draws them). Nothing moves for a reader: every open
ticket stays under its release. Run twice, the second changes nothing.
"""

import re
from pathlib import Path

from packaging.version import Version

from ion_repo import ticket_names, tracker
from ion_repo.tickets import repo_name

SLUG_WORDS = 4
MAX_SLUG_WORDS = 10
DEFAULT_MODEL = "sonnet"
OLD_SESSION = re.compile(r" · \*\*Session\*\*: *([a-z]+)(?:, *([a-z]+/[a-z0-9./-]+))?[ \t]*$", re.M)
RELEASE_LINK = re.compile(r"^- \[[^\]]*\]\(releases/[^)]+\.md\)\n", re.M)
RELEASES_POINTER = "Planned releases and their tickets: `ion repo backlog`."


def migrate(root: Path) -> list[str]:
    """The backlog's releases and tickets brought to the named form; what was done, one line each
    (empty when nothing was left to do)."""
    if not tracker.is_folder(root) or not (root / tracker.RELEASES_DIR).is_dir():
        return []
    done = []
    if moved := _sessions(root):
        done.append(f"{moved} ticket Session fields moved to their own line (model, effort)")
    if renamed := _releases(root):
        done.append(
            f"{renamed} release files named after their title, each ticket names its release"
        )
    return done


def _sessions(root: Path) -> int:
    """`· **Session**: medium, fix/x` at the end of an Effort line becomes its own line."""
    moved = 0
    for path in sorted((root / tracker.TICKETS_DIR).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        found = OLD_SESSION.search(text)
        if found is None:
            continue
        effort, branch = found[1], found[2]
        own = f"- **Session**: {DEFAULT_MODEL} {effort}" + (f", {branch}" if branch else "")
        text = OLD_SESSION.sub("", text, count=1)
        text = re.sub(r"^(- \*\*Effort\*\*:.*)$", rf"\1\n{own}", text, count=1, flags=re.M)
        path.write_text(text, encoding="utf-8")
        moved += 1
    return moved


def _releases(root: Path) -> int:
    folder = root / tracker.RELEASES_DIR
    old = [
        path
        for path in folder.glob("v*.md")
        if tracker.RELEASE_HEADING.search(path.read_text(encoding="utf-8"))
        and not tracker.VERSION_LINE.search(path.read_text(encoding="utf-8"))
    ]
    old.sort(key=lambda path: Version(path.stem.removeprefix("v")))
    names = _names(old, {path.stem for path in folder.glob("*.md")} - {path.stem for path in old})
    claimed: set[int] = set()
    for path in old:
        _rewrite(root, path, names[path], claimed)
    _follow_links(root, {path.name: f"{name}.md" for path, name in names.items()})
    _index(root)
    return len(old)


def _names(old: list[Path], taken: set[str]) -> dict[Path, str]:
    """A name per release file: the first words of its title, more of them while another release
    (or a file already there) has the same, then a number."""
    titles = {}
    for path in old:
        heading = tracker.RELEASE_HEADING.search(path.read_text(encoding="utf-8"))
        assert heading is not None
        titles[path] = heading[2]
    width = dict.fromkeys(old, SLUG_WORDS)
    names: dict[Path, str] = {}
    while True:
        names = {
            path: ticket_names.slug(titles[path], width[path]) or path.stem.replace(".", "-")
            for path in old
        }
        count = {name: list(names.values()).count(name) for name in names.values()}
        clashing = [path for path in old if count[names[path]] > 1 or names[path] in taken]
        if not clashing or max(width.values()) >= MAX_SLUG_WORDS:
            break
        for path in clashing:
            width[path] += 1
    used = set(taken)
    for path in old:  # what still clashes takes a number
        candidate, number = names[path], 1
        while candidate in used:
            number += 1
            candidate = f"{names[path]}-{number}"
        names[path] = candidate
        used.add(candidate)
    return names


def _rewrite(root: Path, path: Path, name: str, claimed: set[int]) -> None:
    """The release file renamed and rewritten, its tickets pointed to it."""
    text = path.read_text(encoding="utf-8")
    heading = tracker.RELEASE_HEADING.search(text)
    assert heading is not None
    repo = repo_name(root)
    kept, listed = [], []
    for line in text[heading.end() :].strip("\n").splitlines():
        found = tracker.RELEASE_TICKET.match(line)
        prefix = re.match(rf"- ({tracker.REPO_PREFIX})?", line)
        own = prefix is not None and prefix[1] in (None, f"{repo}#")
        if found and own:
            listed.append(int(found[1]))
        else:
            kept.append(line)
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip("\n")
    content = f"# {heading[2].strip()}\n- **Version**: v{heading[1]}\n"
    path.with_name(f"{name}.md").write_text(content + (f"\n{body}\n" if body else ""), "utf-8")
    if path.name != f"{name}.md":
        path.unlink()
    for number in listed:
        if number not in claimed and _name_release(root, number, name):
            claimed.add(number)


def _name_release(root: Path, number: int, name: str) -> bool:
    """`- **Release**: <name>` in the ticket's file, before its Origin; False for a closed ticket
    or one that already names a release."""
    ticket = tracker.find(root, number)
    if ticket is None or ticket.release:
        return False
    text = ticket.path.read_text(encoding="utf-8")
    line = f"- **Release**: {name}"
    anchor = re.search(r"^- \*\*Origin\*\*:", text, re.M)
    if anchor:
        text = text[: anchor.start()] + line + "\n" + text[anchor.start() :]
    else:
        text = re.sub(r"^(- \*\*Effort\*\*:.*)$", rf"\1\n{line}", text, count=1, flags=re.M)
    if line not in text:  # a ticket with neither: the line goes under its heading
        text = text.replace("\n", f"\n{line}\n", 1)
    ticket.path.write_text(text, encoding="utf-8")
    return True


def _follow_links(root: Path, moves: dict[str, str]) -> None:
    """Links to a renamed release file, anywhere in the repo's Markdown, point to the new one."""
    renamed = {old: new for old, new in moves.items() if old != new}
    if not renamed:
        return
    pattern = re.compile(r"releases/(" + "|".join(map(re.escape, renamed)) + r")(?![\w-])")
    listed = ticket_names._tracked_files(root) or [
        path.relative_to(root).as_posix() for path in (root / "docs").rglob("*.md")
    ]
    for relative in listed:
        path = root / relative
        if not path.is_file() or not relative.endswith(ticket_names.LINKED_SUFFIXES):
            continue
        text = path.read_text(encoding="utf-8")
        moved = pattern.sub(lambda found: f"releases/{renamed[found[1]]}", text)
        if moved != text:
            path.write_text(moved, encoding="utf-8")


def _index(root: Path) -> None:
    """The index no longer lists the releases: a pointer to the command takes their place."""
    path = root / tracker.INDEX
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    cleared = RELEASE_LINK.sub("", text)
    if cleared == text:
        return
    cleared = re.sub(r"(## Releases\n)\n*", rf"\1\n{RELEASES_POINTER}\n\n", cleared, count=1)
    path.write_text(re.sub(r"\n{3,}", "\n\n", cleared), encoding="utf-8")
