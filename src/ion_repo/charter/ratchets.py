"""Counters of ratchets (`[ratchets.<name>]`, a `budget` ceiling that only goes down) and floors
(`[floors.<name>]`, a `floor` value that only goes up).

Each counter receives the repo and its parameters and returns (value, detail).
"""

from __future__ import annotations

import ast
import re
from collections.abc import Callable

from ion_repo.charter.repo import Params, Repo, outside_tests

Counter = Callable[[Repo, Params], tuple[int, list[str]]]
DEFAULT_SUFFIXES = [".py", ".ts", ".vue", ".css", ".mjs"]
NINJA_ROUTE = r"\s*@(api|router)\.(get|post|put|patch|delete)"
BLOCKING_LOCK = re.compile(r"#\s*(?:Blocking lock|Verrou bloquant)\s*:", re.IGNORECASE)
LOCK_LOOKBACK = 9


def file_size(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """At most `max_lines` (300) lines per file; generated files do not count."""
    suffixes = set(params.get("suffixes", DEFAULT_SUFFIXES))
    ceiling = params.get("max_lines", 300)
    culprits = []
    for path in repo.tracked(params["files"]):
        if path.suffix not in suffixes or repo.is_generated(path):
            continue
        lines = len(path.read_text("utf-8").splitlines())
        if lines > ceiling:
            culprits.append(f"{lines:5d}  {repo.rel(path)}")
    return len(culprits), sorted(culprits, reverse=True)


def long_routes(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """Views longer than `max_lines` (15) lines, found by their decorator (`decorator`, a regex;
    django-ninja's by default)."""
    decorator = re.compile(params.get("decorator", NINJA_ROUTE))
    ceiling = params.get("max_lines", 15)
    culprits = []
    for path in repo.tracked(params.get("files", ["backend/*/api/*.py", "backend/*/api.py"])):
        lines = path.read_text("utf-8").splitlines()
        for index, line in enumerate(lines):
            if not decorator.match(line):
                continue
            start = index
            while start < len(lines) and not re.match(r"\s*def ", lines[start]):
                start += 1
            if start >= len(lines):
                continue
            indent = len(lines[start]) - len(lines[start].lstrip())
            end = start + 1
            while end < len(lines) and not (
                lines[end].strip() and len(lines[end]) - len(lines[end].lstrip()) <= indent
            ):
                end += 1
            if end - start > ceiling:
                where = f"{repo.rel(path)}:{start + 1}"
                culprits.append(f"{end - start:5d}  {where}  {lines[start].strip()[:60]}")
    return len(culprits), sorted(culprits, reverse=True)


def _method(call: ast.Call) -> str:
    return getattr(call.func, "attr", "")


def django_locks(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """`select_for_update` without `nowait`/`skip_locked` nor a `# Blocking lock: <reason>`
    comment in the 8 lines above. Parsed, so a docstring is not a lock."""
    culprits = []
    files = params.get("files", ["backend/*.py", "backend/**/*.py"])
    for path in outside_tests(repo.tracked(files)):
        text = path.read_text("utf-8")
        lines = text.splitlines()
        for node in ast.walk(ast.parse(text)):
            if not (isinstance(node, ast.Call) and _method(node) == "select_for_update"):
                continue
            guarded = any(keyword.arg in {"nowait", "skip_locked"} for keyword in node.keywords)
            above = "\n".join(lines[max(0, node.lineno - LOCK_LOOKBACK) : node.lineno])
            if not guarded and not BLOCKING_LOCK.search(above):
                culprits.append(f"{repo.rel(path)}:{node.lineno}")
    return len(culprits), culprits


def occurrences(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """How many times a text (`pattern`, literal) appears in files: for example
    `timezone.now()` in tests, where the clock must be frozen."""
    culprits = []
    for path in repo.tracked(params["files"]):
        found = path.read_text("utf-8").count(params["pattern"])
        if found:
            culprits.append(f"{found:4d}  {repo.rel(path)}")
    return sum(int(line.split()[0]) for line in culprits), sorted(culprits, reverse=True)


def test_density(repo: Repo, params: Params) -> tuple[int, list[str]]:
    """Lines of tests per thousand lines of code (generated files left out). Test files end with
    one of `test_suffixes`."""
    suffixes = set(params.get("suffixes", [".ts", ".vue", ".mjs"]))
    test_suffixes = tuple(params.get("test_suffixes", [".spec.ts", ".nuxt.spec.ts"]))
    code = tests = 0
    for path in repo.tracked(params["files"]):
        if path.suffix not in suffixes or repo.is_generated(path):
            continue
        lines = len(path.read_text("utf-8").splitlines())
        if path.name.endswith(test_suffixes):
            tests += lines
        else:
            code += lines
    ratio = round(1000 * tests / code) if code else 0
    return ratio, [f"{tests} lines of tests for {code} lines of code ({ratio}/1000)"]


COUNTERS: dict[str, Counter] = {
    "file-size": file_size,
    "long-routes": long_routes,
    "django-locks": django_locks,
    "occurrences": occurrences,
    "test-density": test_density,
}
