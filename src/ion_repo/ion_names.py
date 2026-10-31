"""kiln's names in a project, moved to ion-repo's by `ion repo update` (the Ion family, 31 October
2026).

Copier brings the template's files under their new names; what the project wrote itself still
cites the old ones: its rules filed in `.claude/rules/kiln/`, a skill `/kiln:merge`, the rule
`[REPORT-TO-KILN]`, a variable `KILN_PROJECT`, a plugin `kiln@kiln`, the address
`antoine-tena/kiln`. Each is rewritten where it stands; the project's prose about "kiln" is its
own and stays. Nothing happens in a project that has none of them, so running it again is free.
"""

import re
import subprocess
from collections.abc import Callable
from pathlib import Path

from ion_repo import renames

# History is not rewritten: the changelog and closed tickets cite kiln as it was.
UNTOUCHED = ("CHANGELOG.md", "docs/backlog/done.md", ".copier-answers.yml")
TEXT_SUFFIXES = frozenset(
    {".py", ".ts", ".tsx", ".vue", ".js", ".mjs", ".astro", ".java", ".md", ".toml", ".yml",
     ".yaml", ".sh", ".css", ".txt", ".json", ".jinja", ".cfg", ".ini", ".html", ".env", ""}
)  # fmt: skip
Replacement = str | Callable[[re.Match[str]], str]
REWRITES: tuple[tuple[re.Pattern[str], Replacement], ...] = (
    (re.compile(r"(?<![\w/-])(/?)kiln:(" + "|".join(renames.ION_SKILLS) + r")\b"), r"\1repo:\2"),
    (re.compile(r"\[REPORT-TO-KILN\]"), "[REPORT-TO-ION-REPO]"),
    (re.compile(r"\bKILN_(" + "|".join(renames.ION_VARIABLES) + r")\b"), r"ION_REPO_\1"),
    (
        re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, renames.ION_PLUGINS)) + r")\b"),
        lambda match: renames.ION_PLUGINS[match[1]],
    ),
    (re.compile(re.escape(renames.LEGACY_RULES_DIR) + r"\b"), renames.RULES_DIR),
    (re.compile(r"antoine-tena/kiln(?![\w-])"), "antoine-tena/ion-repo"),
)


def convert_ion_names(root: Path) -> list[str]:
    """Each conversion done, in one line; nothing in a project without kiln's names."""
    done = []
    moved, left = move_rules(root)
    if moved:
        done.append(f"{renames.LEGACY_RULES_DIR}/ → {renames.RULES_DIR}/: {', '.join(moved)}")
    if left:
        done.append(
            f"left in {renames.LEGACY_RULES_DIR}/, merge them into {renames.RULES_DIR}/ by hand: "
            + ", ".join(left)
        )
    rewritten = [name for name in _tracked_texts(root) if _rewrite(root / name)]
    if rewritten:
        done.append("kiln's names (skills, plugins, variables, rules) in " + ", ".join(rewritten))
    return done


def rewrite(text: str) -> str:
    for pattern, replacement in REWRITES:
        text = pattern.sub(replacement, text)
    return text


def move_rules(root: Path) -> tuple[list[str], list[str]]:
    """The project's own rules filed among kiln's, moved next to ion-repo's (those of the template
    are already there, Copier removed the old ones); one that clashes stays, named."""
    legacy, current = root / renames.LEGACY_RULES_DIR, root / renames.RULES_DIR
    if not legacy.is_dir():
        return [], []
    moved, left = [], []
    for path in sorted(p for p in legacy.rglob("*") if p.is_file()):
        relative = path.relative_to(legacy)
        target = current / relative
        if target.exists():
            left.append(relative.as_posix())
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        path.rename(target)
        moved.append(relative.as_posix())
    for folder in sorted((p for p in legacy.rglob("*") if p.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()
    if not any(legacy.iterdir()):
        legacy.rmdir()
    return moved, left


def _tracked_texts(root: Path) -> list[str]:
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.splitlines()
    return [name for name in listed if name not in UNTOUCHED and Path(name).suffix in TEXT_SUFFIXES]


def _rewrite(path: Path) -> bool:
    try:
        text = path.read_text()
    except OSError, UnicodeDecodeError:
        return False
    converted = rewrite(text)
    if converted == text:
        return False
    path.write_text(converted)
    return True
