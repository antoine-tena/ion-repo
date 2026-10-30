"""What `kiln update` converts when a project crosses kiln 0.4.0, the release that went English.

Copier carries the project's own changes onto the new template, but it cannot know that a key,
a file or a rule was renamed: left alone, it would ask the new questions again, delete the
`CLAUDE.md` files the project wrote into, and leave French rule identifiers everywhere. So:

- **before** Copier, the answers are given under their new names (with what a project of that time
  was: a French-speaking team, the Europe/Paris time zone, a Java package `fr.<name>`);
- **after** Copier, the project's `charte.toml` becomes `charter.toml` (its budgets and own rules
  kept), its additions to the old `CLAUDE.md` files are carried over into the new one, its waivers
  and its code cite the rules by their new identifiers.
"""

import difflib
import re
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

import copier
import yaml  # brought by copier

from kiln import renames
from kiln.charter.waivers import WAIVERS_FILE
from kiln.shell import KilnError, capture

LEGACY_KEYS = frozenset(renames.ANSWER_KEYS)
LEGACY_CHARTER = "charte.toml"
CHARTER = "charter.toml"
LEGACY_UNVERIFIED = Path("scripts") / "ci" / "charte-non-verifiee.txt"
INSTRUCTIONS = ("CLAUDE.md", "backend/CLAUDE.md", "frontend/CLAUDE.md")
CARRIED_OVER = "## Carried over from the instructions of kiln 0.3"
# What a project of kiln 0.3 was, whatever it said: its CLAUDE.md made the team French-speaking
# and its rules computed calendar notions in Europe/Paris.
LEGACY_DEFAULTS: Mapping[str, object] = {"language": "fr", "timezone": "Europe/Paris"}
GH_TIMEOUT = 10
# A citation, not a subscript: `arr[INDEX]` stays as it is.
RULE_REFERENCE = re.compile(r"(?<![\w\]])\[(" + "|".join(map(re.escape, renames.RULE_IDS)) + r")\]")
TEXT_SUFFIXES = frozenset(
    {".py", ".ts", ".tsx", ".vue", ".js", ".mjs", ".astro", ".java", ".md", ".toml", ".yml",
     ".yaml", ".sh", ".css", ".txt", ".json", ".jinja", ".cfg", ".ini", ".html"}
)  # fmt: skip


def raw_answers(root: Path) -> dict[str, object]:
    """The answers file as written, under the names of the release that wrote it."""
    path = root / ".copier-answers.yml"
    loaded = yaml.safe_load(path.read_text()) if path.exists() else {}
    return dict(loaded) if isinstance(loaded, dict) else {}


def is_legacy(answers: Mapping[str, object]) -> bool:
    """Answers written by kiln 0.3 (French keys)."""
    return any(key in LEGACY_KEYS for key in answers)


def answers_for_update(root: Path, changes: Mapping[str, object]) -> dict[str, object]:
    """The data given to Copier: the answers under their new names, then `changes`."""
    raw = raw_answers(root)
    data: dict[str, object] = {}
    current = renames.answers(raw)
    if is_legacy(raw):
        data = {key: value for key, value in current.items() if not key.startswith("_")}
        data.update(LEGACY_DEFAULTS)
        if current.get("backend") == "java":
            data["java_package"] = "fr." + str(current.get("name", "")).replace("-", "")
    elif current.get("size") != raw.get("size"):
        data["size"] = current["size"]  # a size named after the fire, before kiln 0.4.10
    if "ci_runner" not in raw and "ci_runner" not in changes:
        data["ci_runner"] = ci_runner_for(root)
    return {**data, **changes}


def ci_runner_for(root: Path) -> str:
    """Where a repo's CI runs when it never said: on GitHub for a public repo (free, unlimited),
    on the machine otherwise (private, or GitHub out of reach: no minutes spent by surprise)."""
    try:
        visibility = subprocess.run(
            ["gh", "repo", "view", "--json", "visibility", "--jq", ".visibility"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT,
            check=False,
        ).stdout.strip()
    except subprocess.TimeoutExpired, OSError:
        return "local"
    return "github" if visibility == "PUBLIC" else "local"


def convert(
    root: Path, previous_answers: Mapping[str, object], source: str, ref: str | None
) -> list[str]:
    """After Copier, which applied `source` at `ref`, what a project of kiln 0.3 still carries;
    returns what was converted."""
    if not is_legacy(previous_answers) or is_legacy(raw_answers(root)):
        return []
    previous = str(previous_answers.get("_commit", ""))
    with tempfile.TemporaryDirectory() as tmp:
        old = render(source, previous, previous_answers, Path(tmp) / "old")
        done = [
            *convert_charter(root, old),
            *carry_over_instructions(root, old, source, ref),
        ]
    done += convert_waivers(root)
    done += convert_rule_references(root)
    legacy_unverified = root / LEGACY_UNVERIFIED
    if legacy_unverified.exists():
        legacy_unverified.unlink()
    return done


def render(source: str, ref: str | None, answers: Mapping[str, object], destination: Path) -> Path:
    data = {key: value for key, value in answers.items() if not key.startswith("_")}
    copier.run_copy(
        source, destination, data=data, vcs_ref=ref, defaults=True, quiet=True, unsafe=False
    )
    return destination


def committed(root: Path, path: str) -> str | None:
    """The file as of the last commit, before Copier touched it."""
    try:
        return capture(["git", "show", f"HEAD:{path}"], root) + "\n"
    except KilnError:
        return None


# --- charte.toml → charter.toml -------------------------------------------------------------

SECTION = re.compile(r"^\[(\w+)(?:\.([\w-]+))?\]")
KEY = re.compile(r"^(\s*)(\w+)(\s*=)")
QUOTED = re.compile(r'"([^"]*)"')


def translate_charter(text: str, *, keep_ids: bool = False) -> str:
    """A `charte.toml` under the names of kiln 0.4, comments and values kept; `keep_ids` for an
    adopted repo, whose rule identifiers are its own, cited by its instructions."""
    lines = []
    for line in text.splitlines():
        if section := SECTION.match(line):
            name = renames.CHARTER_SECTIONS.get(section[1], section[1])
            rule = section[2]
            renamed = f"[{name}.{renames.CHARTER_RULES.get(rule, rule)}]" if rule else f"[{name}]"
            line = renamed + line[section.end() :]
        elif key := KEY.match(line):
            name = renames.CHARTER_KEYS.get(key[2], key[2])
            rest = line[key.end() :]
            if name == "id" and not keep_ids:
                rest = QUOTED.sub(lambda m: f'"{renames.rule_id(m[1])}"', rest, count=1)
            elif name == "rule":
                rest = QUOTED.sub(lambda m: f'"{renames.CHARTER_RULES.get(m[1], m[1])}"', rest)
            elif name == "unverified_rules":
                rest = rest.replace(str(LEGACY_UNVERIFIED), "scripts/ci/unverified-rules.txt")
            line = f"{key[1]}{name}{key[3]}{rest}"
        lines.append(line)
    return "\n".join(lines) + "\n"


def merge(base: str, ours: str, theirs: str) -> str:
    """Three-way merge of `git merge-file`; a conflict stays marked in the text."""
    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / name for name in ("ours", "base", "theirs")]
        for path, text in zip(paths, (ours, base, theirs), strict=True):
            path.write_text(text)
        merged = subprocess.run(
            ["git", "merge-file", "-p", "-L", "project", "-L", "kiln 0.3", "-L", "kiln 0.4",
             *map(str, paths)],
            capture_output=True, text=True, check=False,
        )  # fmt: skip
    return merged.stdout


def convert_charter(root: Path, old: Path) -> list[str]:
    project = committed(root, LEGACY_CHARTER)
    new_path = root / CHARTER
    if project is None or not new_path.exists() or not (old / LEGACY_CHARTER).exists():
        return []
    base = translate_charter((old / LEGACY_CHARTER).read_text())
    new_path.write_text(merge(base, translate_charter(project), new_path.read_text()))
    (root / LEGACY_CHARTER).unlink(missing_ok=True)
    return [f"{LEGACY_CHARTER} → {CHARTER} (budgets and the project's own rules kept)"]


# --- CLAUDE.md files ------------------------------------------------------------------------


HEADING = re.compile(r"^#{1,6}\s")
FENCE = re.compile(r"^\s*(```|~~~)")
# The notes of a file sit under its `### From` line: their own headings go one level below.
NOTES_LEVEL = 4
MAX_LEVEL = 6


def additions(rendered: str, project: str) -> list[str]:
    """Lines the project wrote into a generated file: what it has that the render has not. A block
    written inside a section of the file comes under that section's heading, and every heading
    goes below the `### From` line of the notes, so that the outline of `CLAUDE.md` holds."""
    lines = project.splitlines()
    marks = outline(lines)
    matcher = difflib.SequenceMatcher(a=rendered.splitlines(), b=lines)
    added: list[str] = []
    shown: str | None = None
    for tag, _, _, start, end in matcher.get_opcodes():
        if tag not in ("insert", "replace"):
            continue
        while start < end and not lines[start].strip():
            start += 1
        while end > start and not lines[end - 1].strip():
            end -= 1
        if start == end:
            continue
        is_heading, section = marks[start]
        if not is_heading and section is not None and section != shown and level(section) > 1:
            added += [demoted(section), ""]
        for index in range(start, end):
            added.append(demoted(lines[index]) if marks[index][0] else lines[index])
        added.append("")
        shown = marks[end - 1][1]
    return added


def outline(lines: list[str]) -> list[tuple[bool, str | None]]:
    """Each line: is it a heading (the `#` lines of a code block are not), and the heading of the
    section it is in."""
    marks: list[tuple[bool, str | None]] = []
    fenced, section = False, None
    for line in lines:
        if FENCE.match(line):
            fenced = not fenced
        is_heading = not fenced and HEADING.match(line) is not None
        if is_heading:
            section = line
        marks.append((is_heading, section))
    return marks


def level(heading: str) -> int:
    return len(heading) - len(heading.lstrip("#"))


def demoted(heading: str) -> str:
    """A heading of the old file, below the `### From` line: its sections at level 4, their
    subsections below."""
    depth = level(heading)
    return "#" * min(max(depth + 2, NOTES_LEVEL), MAX_LEVEL) + heading[depth:]


def carry_over_instructions(root: Path, old: Path, source: str, ref: str | None) -> list[str]:
    """The new `CLAUDE.md` (Copier keeps the project's old one: it now belongs to the project),
    with what the project had added to its kiln 0.3 instructions, then the old sub-project files
    removed."""
    notes: list[str] = []
    for name in INSTRUCTIONS:
        project = committed(root, name)
        if project is None or not (old / name).exists():
            continue
        added = additions((old / name).read_text(), project)
        if added:
            notes += [f"### From `{name}`", "", *added]
        if name != "CLAUDE.md":
            (root / name).unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        fresh = render(source, ref, raw_answers(root), Path(tmp) / "new") / "CLAUDE.md"
        fresh_text = fresh.read_text()
    text = fresh_text.rstrip("\n") + "\n"
    if notes:
        text += f"\n{CARRIED_OVER}\n\n" + "\n".join(notes).rstrip("\n") + "\n"
    (root / "CLAUDE.md").write_text(text)
    carried = ", the project's additions carried over" if notes else ""
    return [f"CLAUDE.md rewritten for kiln 0.4{carried}"]


# --- rule identifiers -----------------------------------------------------------------------


def convert_waivers(root: Path) -> list[str]:
    path = root / WAIVERS_FILE
    if not path.exists():
        return []
    text = path.read_text()
    converted = re.sub(
        r'^(\s*rule\s*=\s*)"([^"]+)"',
        lambda m: f'{m[1]}"{renames.rule_id(m[2])}"',
        text,
        flags=re.MULTILINE,
    )
    if converted == text:
        return []
    path.write_text(converted)
    return [f"{WAIVERS_FILE}: rules under their new identifiers"]


def convert_rule_references(root: Path) -> list[str]:
    """`[TAILLE-FICHIER]` → `[FILE-SIZE]` wherever the project cites a rule."""
    listed = capture(["git", "ls-files", "--cached", "--others", "--exclude-standard"], root)
    changed = 0
    for name in listed.splitlines():
        path = root / name
        if path.suffix not in TEXT_SUFFIXES or not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        converted = RULE_REFERENCE.sub(lambda m: f"[{renames.RULE_IDS[m[1]]}]", text)
        if converted != text:
            path.write_text(converted)
            changed += 1
    return [f"rules cited by their new identifiers in {changed} file(s)"] if changed else []
