"""Counters of [CONSTANTS]: module constants of Python, TypeScript and Vue, judged on their name.

Read from the source: the module's own assignments, never those of a class or a function.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from ion_repo.charter.repo import Params, Repo, outside_tests

SCREAMING = re.compile(r"_?[A-Z][A-Z0-9_]*$")
TS_CONSTANT = re.compile(
    r"^(?P<export>export )?const (?P<name>[A-Z][A-Z0-9_]*)(?::[^=\n]+)?\s*=\s*(?P<value>.*)", re.M
)
VUE_SCRIPT = re.compile(r"<script[^>]*>(.*?)</script>", re.S)
TS_SUFFIXES = {".ts", ".tsx", ".vue", ".mjs"}
TEST_FILE = re.compile(r"\.(spec|test)\.")
NUMBER = re.compile(r"-?[\d(][\d_.\s*/+()-]*;?\s*(?:(?:#|//).*)?$")
# Words that need a subject: alone, they do not say what they hold.
BARE_WORD = re.compile(
    r"(?:MAX|MIN|LIMIT|SIZE|SIZES|WIDTH|HEIGHT|DELAY|LABEL|LABELS|OPTION|"
    r"OPTIONS|ITEM|ITEMS|VALUE|VALUES|DATA|CONFIG|URL|PATH|COLOR|COLORS|"
    r"STEP|STEPS|TITLE|DURATION|DATE|RADIUS|KEY|PREFIX|TTL|TIMEOUT|RES|"
    r"INFO|TMP|STATUS|LIST|DEFAULT|DEFAULTS|TABS|COLUMNS|ROWS|BASE|ERRORS|"
    r"RESPONSES|FIELDS|LINKS|BODY|NOTE|EMPTY|SALT|TONES|KINDS|VARIANTS|"
    r"ENTRIES|ROUTE|HEADERS|MARGIN|PADDING|EXTENSIONS|SEPARATOR|HEADING|ROOT|"
    r"NAMES|TYPES|CODES|KEYS|TEXT|MESSAGE|COUNT)$"
)
TECHNICAL_TYPE = re.compile(r"_(LISTE?|DICT|STR|ARRAY|TUPLE|OBJ)$")
DURATION = re.compile(
    r"(^|_)(TIMEOUT|DELAY|DURATION|INTERVAL|TTL|MAX_AGE|COOLDOWN|DEBOUNCE|GRACE|RETENTION)$"
)


@dataclass(frozen=True)
class Constant:
    name: str
    value: str
    path: Path
    line: int
    is_exported: bool

    @property
    def word(self) -> str:
        return self.name.lstrip("_")


def _python(path: Path, text: str) -> list[Constant]:
    found = []
    for node in ast.parse(text).body:
        targets = node.targets if isinstance(node, ast.Assign) else []
        if isinstance(node, ast.AnnAssign) and node.value:
            targets = [node.target]
        for target in targets:
            if isinstance(target, ast.Name) and SCREAMING.match(target.id):
                value = ast.unparse(node.value)
                found.append(Constant(target.id, value, path, node.lineno, target.id[0] != "_"))
    return found


def _script(path: Path, text: str) -> list[Constant]:
    blocks = [(0, text)]
    if path.suffix == ".vue":
        blocks = [(match.start(1), match[1]) for match in VUE_SCRIPT.finditer(text)]
    return [
        Constant(
            match["name"],
            match["value"].strip(),
            path,
            text.count("\n", 0, offset + match.start()) + 1,
            bool(match["export"]),
        )
        for offset, block in blocks
        for match in TS_CONSTANT.finditer(block)
    ]


@cache
def _read(path: Path) -> tuple[str, tuple[Constant, ...]]:
    text = path.read_text("utf-8")
    return text, tuple((_python if path.suffix == ".py" else _script)(path, text))


def _sources(repo: Repo, params: Params) -> list[Path]:
    return [
        path
        for path in outside_tests(repo.tracked(params["files"]))
        if (path.suffix == ".py" or path.suffix in TS_SUFFIXES)
        and not TEST_FILE.search(path.name)
        and not repo.is_generated(path)
    ]


def _report(repo: Repo, constants: list[Constant]) -> tuple[int, list[str]]:
    lines = [f"{repo.rel(found.path)}:{found.line}  {found.name}" for found in constants]
    return len(lines), sorted(lines)


def constant_names(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """A bare word (`LABEL`, `W`) or a technical type at the end (`_LIST`)."""
    words = set(params.get("words", []))
    return _report(
        repo,
        [
            found
            for path in _sources(repo, params)
            for found in _read(path)[1]
            if BARE_WORD.match(found.word)
            or found.word in words
            or len(found.word) <= 2
            or TECHNICAL_TYPE.search(found.word)
        ],
    )


def constant_units(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """A numeric duration whose name ends without its unit (`REQUEST_TIMEOUT = 5`)."""
    return _report(
        repo,
        [
            found
            for path in _sources(repo, params)
            for found in _read(path)[1]
            if DURATION.search(found.word) and NUMBER.match(found.value)
        ],
    )


def _python_imports(path: Path) -> set[tuple[str, str]]:
    """(last part of the module, name) of each `from … import`."""
    return {
        ((node.module or "").rsplit(".", 1)[-1], alias.name)
        for node in ast.walk(ast.parse(_read(path)[0]))
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }


def constant_homonyms(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """One name defined by several modules that other files read. TypeScript: `export`. Python:
    really imported elsewhere, a module constant without `_` being importable by default."""
    sources = _sources(repo, params)
    imported = {pair for path in sources if path.suffix == ".py" for pair in _python_imports(path)}
    shared: dict[tuple[bool, str], list[Constant]] = defaultdict(list)
    for path in sources:
        is_python = path.suffix == ".py"
        module = path.parent.name if path.name == "__init__.py" else path.stem
        for found in _read(path)[1]:
            if found.is_exported and (not is_python or (module, found.name) in imported):
                shared[(is_python, found.name)].append(found)
    return _report(repo, [one for group in shared.values() if len(group) > 1 for one in group])
