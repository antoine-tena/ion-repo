"""An adopted repo's names of kiln 0.3, moved to today's by `kiln update`, before they go.

A repo adopted before kiln 0.4.0 still carries what kiln named in French: its `charte.toml`, the
`charte` command in its hooks, the workflows `charte.yml`, `contrat-api.yml`, `securite.yml` and
their inputs. kiln reads them for now; `kiln update` converts them while it still can. Only what
belongs to kiln changes: the identifiers of the repo's own rules (`id = "TAILLE-FICHIER"`) are
cited by its instructions and stay; its prose is its own, listed for a reread, never rewritten.
"""

import re
import subprocess
from collections.abc import Callable
from pathlib import Path

from kiln.charter.config import CHARTER_FILE, LEGACY_CHARTER_FILE
from kiln.ci.jobs import LEGACY_INPUTS, RELAYS
from kiln.migrations import translate_charter

HOOKS_FILE = ".pre-commit-config.yaml"
WORKFLOW_DIR = Path(".github") / "workflows"
# `entry: charte`, `entry: charte couverture`: the command and its subcommand of kiln 0.3.
LEGACY_ENTRY = re.compile(r"^(\s*entry:\s*['\"]?)charte(?![\w-])(\s+(\w+))?")
LEGACY_ACTIONS = {"couverture": "coverage", "verifier": "check"}
LEGACY_WORKFLOW = re.compile(
    r"(antoine-tena/kiln/\.github/workflows/)(" + "|".join(map(re.escape, RELAYS)) + r")\.yml@"
)
INPUT_KEY = re.compile(r"^(\s+)([\w-]+)(\s*:)")
# What the repo's prose may still cite, for the list to reread.
LEGACY_MENTION = r"charte\.toml|\bcharte (types|couverture|verifier|file)\b"


def convert_legacy_names(root: Path) -> list[str]:
    """Each conversion done, in one line; nothing when the repo has none of these names."""
    done = []
    if (root / LEGACY_CHARTER_FILE).is_file() and not (root / CHARTER_FILE).exists():
        legacy = root / LEGACY_CHARTER_FILE
        charter = translate_charter(legacy.read_text(), keep_ids=True)
        # Its own name, in a rule's `exclude` (`^charte\.toml$`), follows it.
        charter = charter.replace(r"charte\.toml", r"charter\.toml")
        (root / CHARTER_FILE).write_text(charter.replace(LEGACY_CHARTER_FILE, CHARTER_FILE))
        legacy.unlink()
        done.append(f"{LEGACY_CHARTER_FILE} → {CHARTER_FILE} (the repo's rule identifiers kept)")
    if _rewrite(root / HOOKS_FILE, _hooks):
        done.append(f"{HOOKS_FILE}: the charter command")
    folder = root / WORKFLOW_DIR
    workflows = sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")]) if folder.is_dir() else []
    done += [
        f"{path.relative_to(root)}: kiln's workflows and their inputs"
        for path in workflows
        if _rewrite(path, _workflows)
    ]
    return done


def remaining_mentions(root: Path) -> list[str]:
    """Tracked files whose prose still cites `charte.toml` or a `charte` subcommand."""
    listed = subprocess.run(
        ["git", "grep", "-l", "-E", LEGACY_MENTION],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return listed.stdout.split()


def _rewrite(path: Path, convert: Callable[[str], str]) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    converted = convert(text)
    if converted == text:
        return False
    path.write_text(converted, encoding="utf-8")
    return True


def _hooks(text: str) -> str:
    def entry(match: re.Match[str]) -> str:
        action = match[3]
        if action is None:
            return f"{match[1]}charter"
        return f"{match[1]}charter {LEGACY_ACTIONS.get(action, action)}"

    return "".join(LEGACY_ENTRY.sub(entry, line) for line in text.splitlines(keepends=True))


def _workflows(text: str) -> str:
    """Old workflow names moved to today's; in the jobs that call them, the French inputs too."""
    lines = []
    job_indent: int | None = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if LEGACY_WORKFLOW.search(line):
            line = LEGACY_WORKFLOW.sub(lambda m: f"{m[1]}{RELAYS[m[2]]}.yml@", line)
            job_indent = indent
        elif job_indent is not None and stripped.strip() and not stripped.startswith("#"):
            if indent < job_indent:
                job_indent = None
            elif (key := INPUT_KEY.match(line)) and key[2] in LEGACY_INPUTS:
                line = f"{key[1]}{LEGACY_INPUTS[key[2]]}{line[key.end(2) :]}"
        lines.append(line)
    return "".join(lines)
