"""Rules of the charter that no check enforces, listed again by ion-repo at each `set` and `update`.

A rule is checked when `charter.toml` cites it (`id = "…"`) or when a CI tool holds it (mypy,
strict TypeScript, locked dependencies, audit, pre-commit). Every other rule, read in the
instructions, goes in the list of rules applied in review (`unverified_rules` of the charter):
a local rule added to the instructions appears there by itself, a rule that gains its check
leaves it.
"""

import re
from pathlib import Path

from ion_repo.charter.config import load
from ion_repo.renames import rule_id
from ion_repo.stack import PNPM_FRONTENDS, Stack

DEFAULT_UNVERIFIED_RULES_FILE = Path("scripts") / "ci" / "unverified-rules.txt"
# Where the rules are written: ion-repo's rules (`.claude/rules/`), and the `CLAUDE.md` files that
# held them before kiln 0.4.0 (adopted repos still do).
INSTRUCTION_FILES = ("CLAUDE.md", "backend/CLAUDE.md", "frontend/CLAUDE.md")
RULES_DIR = Path(".claude") / "rules"
RULE_PATTERN = re.compile(r"\*\*\[([A-Z0-9+-]+)\]\*\*")
RULE_SECTIONS = ("bans", "ratchets", "floors")

ALWAYS_VERIFIED = frozenset({"NO-COMMIT-ON-MAIN", "LOCKED-DEPENDENCIES", "VULNERABILITY-AUDIT"})
PYTHON_VERIFIED = frozenset({"TYPING", "STRICT-TYPING", "MYPY"})
PNPM_VERIFIED = frozenset({"STRICT-TS", "NO-ANY"})
# Held by the Maven build: `-Xlint:all -Werror` and the JaCoCo coverage floor.
MAVEN_VERIFIED = frozenset({"NO-RAW-TYPES", "TESTS"})

HEADER = """\
# Rules of the instructions that no check enforces: applied in review.
# File listed again by ion-repo (set, update) from the instructions and charter.toml: to take a rule
# out, give it a check in charter.toml, or amend it where it is written.
"""


def instruction_files(root: Path) -> list[Path]:
    rules_dir = root / RULES_DIR
    rule_files = sorted(rules_dir.rglob("*.md")) if rules_dir.is_dir() else []
    return [*(root / name for name in INSTRUCTION_FILES), *rule_files]


def charter_rules(root: Path) -> list[str]:
    """Identifiers of the rules written in the instructions, in their order, without
    duplicates."""
    rules: dict[str, None] = {}
    for path in instruction_files(root):
        if path.is_file():
            rules.update(dict.fromkeys(RULE_PATTERN.findall(path.read_text("utf-8"))))
    return list(rules)


def verified_rules(root: Path, stack: Stack) -> set[str]:
    """Rules a check enforces, under their current names."""
    config = load(root)
    verified = set(ALWAYS_VERIFIED)
    for section in RULE_SECTIONS:
        rules = config.get(section, {})
        verified |= {rule_id(str(rule["id"])) for rule in rules.values() if "id" in rule}
    if stack.python_dirs:
        verified |= PYTHON_VERIFIED
    if stack.frontend in PNPM_FRONTENDS:
        verified |= PNPM_VERIFIED
    if stack.maven_dir is not None:
        verified |= MAVEN_VERIFIED
    return verified


def unverified_rules_file(root: Path) -> Path:
    """Where the charter wants its list of rules applied in review."""
    return root / str(load(root).get("unverified_rules", DEFAULT_UNVERIFIED_RULES_FILE))


def write_unverified_rules(root: Path, stack: Stack) -> None:
    verified = verified_rules(root, stack)
    unverified = [rule for rule in charter_rules(root) if rule_id(rule) not in verified]
    path = unverified_rules_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + "".join(f"[{rule}]\n" for rule in unverified))
