"""Ticket IDs written `<repo>#T-NN` everywhere, even in their own repo (antoine, 1 November 2026).

The prefix is the repo's name (`name` in `.copier-answers.yml`), the number never changes.
`ion repo tickets` converts what a repo wrote before that: it shows the plan, writes on a yes, and
a second run has nothing left to do. Only real IDs move:

- a bare `T-12` of a number this repo gave out becomes `<repo>#T-12`;
- a citation of another repo (`hearth's T-07`, `ion-repo T-394`, `Côté ion-repo : T-391`) takes
  that repo's current name; the old names of the Ion family count in the family's repos only,
  a client's `cone` is the client's;
- what cannot be told apart (an unknown owner, a number never given out, a countdown, a fenced
  code block) stays as it is, listed for the user. No other character of a file changes.

A renamed repo: `rename_prefix` moves its own prefix in its own files, numbers and the rest
untouched; other repos' citations of the old name stay (the forge redirects it).
"""

import re
import tomllib
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

from ion_repo import renames, ui
from ion_repo.shell import KilnError
from ion_repo.stack import read_answers

BACKLOG_FILES = tuple(
    f"docs/backlog/{name}.md" for name in ("backlog", "done", "rejected", "urgent")
)
TICKET_FILES = (*BACKLOG_FILES, "CLAUDE.md")
REPO_PREFIX = r"[a-z][a-z0-9-]*#"
NEXT_FREE = re.compile(rf"Next free: (?:{REPO_PREFIX})?T-(\d+)")
# Not `NT-01`, `MIT-0`, a path, a branch, an option's value, `x-T-1`, nor a prefixed one.
BARE = re.compile(r"(?<![\w#/.=-])T-(\d+)(?!\w|-\w|\.\w)")
COUNTDOWN = re.compile(r"\s(?:days?|hours?|minutes?|min|h|d|jours?|heures?|j)\b")
# What may stand right before an ID and own it: `hearth's T-07`, `ion-repo T-394`, `ion-repo : T-1`.
OWNER = re.compile("([A-Za-z][\\w-]*)(['\u2019]s)?(\\s?:)?\\s+`?$")
GOES_ON = re.compile(r"`?(?:,| and| et)\s+`?")
DECLARED = re.compile(
    rf"^(?:### |- (?:\*\*\d{{4}}-\d\d-\d\d\*\* · )?)((?:(?:{REPO_PREFIX})?T-\d+(?:, )?)+) ·", re.M
)
LOOK_BACK = 60
FENCE = re.compile(r"^ {0,3}```.*?^ {0,3}```[^\n]*$", re.M | re.S)
SAMPLES = 5


@dataclass
class Plan:
    """What a run would write (path to new text) and what it leaves, with why."""

    name: str
    writes: dict[Path, str] = field(default_factory=dict)
    converted: dict[Path, int] = field(default_factory=dict)
    samples: list[str] = field(default_factory=list)
    left: list[str] = field(default_factory=list)


def repo_name(root: Path) -> str:
    """The prefix of this repo's tickets: its answers, else its `pyproject.toml`, else the folder
    of its main tree, never the folder of a worktree."""
    try:
        name = read_answers(root).get("name")
    except KilnError:
        name = None
    if isinstance(name, str) and name:
        return name
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        declared = tomllib.loads(pyproject.read_text()).get("project", {}).get("name")
        if isinstance(declared, str) and declared:
            return declared
    from ion_repo.adopt import project_name  # adopt needs update, which needs this module

    return project_name(root)


def ticket_id(root: Path, number: int) -> str:
    return f"{repo_name(root)}#T-{number:02d}"


def plan(root: Path, also: Iterable[str] = ()) -> Plan:
    """The whole conversion, nothing written."""
    name = repo_name(root)
    result = Plan(name)
    texts = _read_all(root, (*TICKET_FILES, *also), result)
    given = _given_out(root)
    aliases = _aliases(name)
    for path, text in texts.items():
        relative = path.relative_to(root).as_posix()
        new, count = _convert(text, relative, name, given, aliases, result)
        if count:
            result.writes[path] = new
            result.converted[path] = count
    return result


def _read_all(root: Path, names: Iterable[str], result: Plan) -> dict[Path, str]:
    texts = {}
    for relative in dict.fromkeys(names):
        path = root / relative
        if not path.is_file():
            continue
        try:  # newline="": a CRLF file keeps its line ends
            with path.open(encoding="utf-8", newline="") as stream:
                texts[path] = stream.read()
        except UnicodeDecodeError:
            result.left.append(f"{relative}: not UTF-8, not read")
    return texts


def _given_out(root: Path) -> tuple[set[int], int | None]:
    """The numbers declared by a heading or a closing line, and the next free one."""
    declared: set[int] = set()
    next_free = None
    for relative in BACKLOG_FILES:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for found in DECLARED.finditer(text):
            declared |= {int(number) for number in re.findall(r"T-(\d+)", found[1])}
        if written := NEXT_FREE.search(text):
            next_free = int(written[1])
    return declared, next_free


def _aliases(name: str) -> dict[str, str]:
    """The names that own a citation: this repo's, and the family's in a family repo only."""
    aliases = {name.lower(): name}
    if name == "ion" or name.startswith("ion-"):
        aliases |= renames.FAMILY_TOOLS
        aliases |= {tool: tool for tool in renames.FAMILY_TOOLS.values()}
    return aliases


def _convert(
    text: str,
    relative: str,
    name: str,
    given: tuple[set[int], int | None],
    aliases: dict[str, str],
    result: Plan,
) -> tuple[str, int]:
    fences = [found.span() for found in FENCE.finditer(text)]
    pieces: list[str] = []
    position, count = 0, 0
    last_cited, cited_end = "", 0

    def leave(start: int, why: str) -> None:
        line = text.count("\n", 0, start) + 1
        result.left.append(f"{relative}:{line}: {why}")

    for found in BARE.finditer(text):
        start, end = found.span()
        before = text[max(0, start - LOOK_BACK) : start]
        if any(low <= start < high for low, high in fences):
            leave(start, f"{found[0]} in a code block")
            continue
        if COUNTDOWN.match(text, end):
            leave(start, f"{found[0]} reads as a countdown")
            continue
        replaced_from, owner = start, name
        owned = OWNER.search(before)
        known = aliases.get(owned[1].lower()) if owned else None
        goes_on = last_cited and GOES_ON.fullmatch(text, cited_end, start)
        if before.rstrip().endswith("Next free:"):
            pass
        elif owned and known:
            owner, last_cited, cited_end = known, known, end
            if not owned[3]:  # `Côté ion-repo : T-391` keeps its words
                replaced_from = start - len(before) + owned.start()
        elif owned and owned[2]:
            leave(start, f"{owned[0].strip()}{found[0]}: whose? unknown repo")
            continue
        elif not _is_given(int(found[1]), given):
            if not goes_on:
                leave(start, f"{found[0]}: number never given out here")
                continue
            owner, cited_end = last_cited, end
        pieces += [text[position:replaced_from], f"{owner}#{found[0]}"]
        position = end
        count += 1
        if len(result.samples) < SAMPLES and owner != name:
            result.samples.append(f"{text[replaced_from:end]} → {owner}#{found[0]}")
    return "".join(pieces) + text[position:], count


def _is_given(number: int, given: tuple[set[int], int | None]) -> bool:
    declared, next_free = given
    return number in declared or (next_free is not None and number < next_free)


def show(result: Plan, root: Path) -> None:
    """The plan, before anything is written."""
    lines = [
        f"{path.relative_to(root).as_posix()}: {count} IDs" for path, count in
        result.converted.items()
    ]  # fmt: skip
    lines += [f"e.g. {sample}" for sample in result.samples]
    if result.left:
        lines += [f"left as is ({len(result.left)}):", *result.left]
    ui.panel(f"Ticket IDs: T-NN → {result.name}#T-NN", lines or ["nothing to convert"])


def write(result: Plan) -> None:
    for path, text in result.writes.items():
        with path.open("w", encoding="utf-8", newline="") as stream:
            stream.write(text)


def migrate(
    root: Path,
    *,
    also: Iterable[str] = (),
    assume_yes: bool = False,
    dry_run: bool = False,
    ask: Callable[[str], str] | None = None,
) -> bool:
    """Shows the conversion, then writes it on a yes. Without anyone to ask, nothing is written.
    Says whether it wrote."""
    result = plan(root, also)
    show(result, root)
    if not result.writes or dry_run:
        return False
    if not assume_yes:
        if ask is None:
            ui.note("Not written, nobody to ask: `ion repo tickets --yes` writes them.")
            return False
        if ask("Write these changes? [y/N] ").strip().lower() not in ("y", "yes", "o", "oui"):
            ui.note("Nothing written; `ion repo tickets` offers it again.")
            return False
    write(result)
    ui.success(f"{sum(result.converted.values())} ticket IDs written as {result.name}#T-NN")
    return True


def rename_prefix(root: Path, old: str, new: str) -> int:
    """The repo's own prefix follows its new name in its own files; says how many moved."""
    pattern = re.compile(rf"(?<![\w-]){re.escape(old)}#(T-\d+)")
    moved = 0
    for relative in TICKET_FILES:
        path = root / relative
        if not path.is_file():
            continue
        with path.open(encoding="utf-8", newline="") as stream:
            text = stream.read()
        renamed, count = pattern.subn(rf"{new}#\1", text)
        if count:
            with path.open("w", encoding="utf-8", newline="") as stream:
                stream.write(renamed)
            moved += count
    return moved
