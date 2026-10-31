"""What the compressor may remove: dead code and unused dependencies, found by the tools that
find them best, then filtered by guards that keep what a static tool cannot see.

vulture (Python code), deptry (Python dependencies) and knip (JavaScript and TypeScript files
and dependencies) propose; nothing they propose is removed here. A candidate the guards keep
is only a candidate: `proof` decides.
"""

import ast
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ion_repo.grid.compressor import proof
from ion_repo.grid.facts import Repo

CODE, DEPENDENCY, FILE = "code", "dependency", "file"
VULTURE_LINE = re.compile(
    r"^(?P<path>.+?):(?P<line>\d+): unused (?P<kind>[a-z]+) '(?P<name>[^']+)'"
)
# What vulture finds that can go whole: variables and attributes may be fields read by an ORM, a
# serializer or a template, imports are ruff's.
REMOVABLE_KINDS = frozenset({"function", "method", "class", "property"})
# Decorators that change nothing about who calls the function; any other one registers it
# somewhere (a signal, a task, a route, a fixture) and keeps it.
NEUTRAL_DECORATORS = frozenset(
    {"property", "staticmethod", "classmethod", "cached_property", "functools.cached_property"}
)
# Files the framework or the tooling calls by convention: nothing in them is dead for vulture.
CONVENTIONAL = re.compile(
    r"(^|/)(tests?|migrations|management/commands|conftest\.py|settings[^/]*|urls\.py|"
    r"apps\.py|admin\.py|signals\.py|wsgi\.py|asgi\.py|manage\.py|setup\.py|__main__\.py|"
    r"test_[^/]*|[^/]*_test\.py)($|/)"
)
# Never touched, even proven (T-139): code where a missing branch is a silent security or
# correctness bug that tests rarely cover.
SENSITIVE_PATH = re.compile(
    r"(?i)(crypt|cipher|hash|hmac|sign|token|auth|password|secret|"
    r"pars(e|er|ing)|lexer|tokeni[sz]|timezone|(^|[/_])tz|unicode|encod)"
)
SENSITIVE_IMPORT = re.compile(
    r"(?m)^\s*(from|import)\s+(cryptography|hashlib|hmac|secrets|ssl|jwt|nacl|bcrypt|"
    r"argon2|zoneinfo|pytz|dateutil|unicodedata|codecs|ast|tokenize|lark|pyparsing)\b"
)
# Dependencies loaded by name, never by an import a tool can see: database drivers, servers,
# time zone data, a framework's plugins. Removing one passes the tests and breaks production.
LOADED_BY_NAME = frozenset(
    {
        "psycopg",
        "psycopg2",
        "psycopg2-binary",
        "psycopg-binary",
        "psycopg-c",
        "mysqlclient",
        "pymysql",
        "oracledb",
        "cx-oracle",
        "gunicorn",
        "uvicorn",
        "daphne",
        "hypercorn",
        "granian",
        "waitress",
        "whitenoise",
        "tzdata",
        "certifi",
        "cryptography",
        "pyjwt",
        "pytz",
        "idna",
        "charset-normalizer",
        "hiredis",
        "redis",
        "django-redis",
        "celery",
        "channels-redis",
        "brotli",
        "uvloop",
        "httptools",
        "pillow",
        "boto3",
        "django-storages",
        "sentry-sdk",
        "typescript",
        "vue-tsc",
        "@nuxt/kit",
        "nuxt",
        "vite",
        "sass",
        "postcss",
        "tailwindcss",
        "autoprefixer",
        "@types/node",
    }
)
MANIFESTS = ("pyproject.toml", "package.json", "uv.lock", "pnpm-lock.yaml", "package-lock.json")
# Prose: a name an audit or a README mentions is not called by it.
PROSE = re.compile(r"(?i)\.(md|rst|txt|adoc)$|(^|/)(docs?|CHANGELOG[^/]*)/")
# Files knip cannot know are used without the framework's plugins: tests and configs.
TEST_OR_CONFIG = re.compile(
    r"(^|/)(tests?|e2e|__tests__|fixtures?|scripts)/|\.(spec|test|stories)\.[cm]?[jt]sx?$|"
    r"(^|/)[^/]*(\.config|rc)\.[cm]?[jt]s$|(^|/)\.[^/]*rc(\.[a-z]+)?$"
)
# Entry point groups that load a package by name: a plugin, never imported by the code.
PLUGIN_GROUPS = re.compile(r"(?m)^\[(?!console_scripts\]|gui_scripts\])[^\]]+\]")


@dataclass(frozen=True)
class Candidate:
    kind: str  # code, dependency, file
    path: str  # the file holding the code, the manifest naming the dependency, the file
    name: str  # dotted path inside the module (`Box.unused`), package name, file path
    tool: str
    lines: int = 0  # lines it weighs

    @property
    def label(self) -> str:
        if self.kind == CODE:
            return f"{self.path}: {self.name}"
        return self.name if self.kind == FILE else f"{self.name} ({self.path})"


@dataclass(frozen=True)
class Skipped:
    candidate: Candidate
    reason: str


def _run(command: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)


def dead_code(
    repo: Repo, executed: dict[str, set[int]] | None = None
) -> tuple[list[Candidate], list[Skipped]]:
    """Functions, methods, classes and properties vulture finds unused, each located in the
    syntax tree, then kept only if no guard speaks against it. `executed`, the lines the tests
    ran (coverage), sends back what runs while nothing names it: used by reflection."""
    sources = [name for name in repo.matching("**/*.py") if (repo.root / name).is_file()]
    if not sources or shutil.which("uvx") is None:
        return [], []
    # Every file is read, tests included: code only the tests call is not proven dead.
    done = _run(["uvx", "vulture", "--min-confidence", "60", *sources], repo.root)
    found: list[Candidate] = []
    skipped: list[Skipped] = []
    words = _word_index(repo)
    library = _is_library(repo)
    for line in done.stdout.splitlines():
        match = VULTURE_LINE.match(line)
        if not match or match["kind"] not in REMOVABLE_KINDS:
            continue
        path = PurePosixPath(match["path"]).as_posix()
        located = locate(repo.root / path, match["name"], int(match["line"]))
        if located is None:
            continue
        qualname, node, parents = located
        size = (node.end_lineno or node.lineno) - _start(node) + 1
        candidate = Candidate(CODE, path, qualname, "vulture", size)
        reason = _guard_code(repo, candidate, node, parents, words, library, executed)
        if reason:
            skipped.append(Skipped(candidate, reason))
        else:
            found.append(candidate)
    return found, skipped


def locate(
    path: Path, name: str, line: int
) -> tuple[str, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, list[ast.AST]] | None:
    """The definition vulture names at `line` (decorators count: vulture gives a property's
    first decorator), its dotted name in the module and the nodes around it."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except OSError, SyntaxError, UnicodeDecodeError:
        return None
    for node, parents in _definitions(tree, []):
        if node.name == name and _start(node) <= line <= node.lineno:
            qualname = ".".join([*(p.name for p in parents if isinstance(p, ast.ClassDef)), name])
            return qualname, node, parents
    return None


def find(
    tree: ast.Module, qualname: str
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, list[ast.AST]] | None:
    """The definition at `qualname`, wherever earlier removals moved it."""
    for node, parents in _definitions(tree, []):
        names = [p.name for p in parents if isinstance(p, ast.ClassDef)]
        if ".".join([*names, node.name]) == qualname:
            return node, parents
    return None


def _definitions(
    node: ast.AST, parents: list[ast.AST]
) -> Iterator[tuple[ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, list[ast.AST]]]:
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield child, parents
            yield from _definitions(child, [*parents, child])


def _start(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> int:
    return min([node.lineno, *(item.lineno for item in node.decorator_list)])


def _guard_code(
    repo: Repo,
    candidate: Candidate,
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    parents: list[ast.AST],
    words: dict[str, set[str]],
    library: bool,
    executed: dict[str, set[int]] | None,
) -> str:
    """Why the definition stays, or "" when only the proof is left to decide."""
    name, path = node.name, candidate.path
    if CONVENTIONAL.search(path):
        return "a file the framework or the tooling calls by convention"
    if SENSITIVE_PATH.search(path) or SENSITIVE_IMPORT.search(repo.text(path)):
        return "security, parsing, time zones or text encoding: never touched"
    if any(PurePosixPath(path).match(pattern) for pattern in ("**/__init__.py",)):
        return "a package's interface"
    if name.startswith("__") and name.endswith("__"):
        return "a special method, called by Python itself"
    decorators = {ast.unparse(item).split("(")[0] for item in node.decorator_list}
    if decorators - NEUTRAL_DECORATORS:
        return f"decorated by {', '.join(sorted(decorators - NEUTRAL_DECORATORS))}: registered"
    if any(isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)) for parent in parents):
        return "nested in a function"
    owner = next((p for p in reversed(parents) if isinstance(p, ast.ClassDef)), None)
    if owner is not None and owner.bases:
        return f"a method of {owner.name}, which inherits: maybe an override the parent calls"
    if library and not name.startswith("_"):
        return "a public name of a library: its users may call it"
    if name in _exported(repo.text(path)):
        return "listed in __all__"
    # Its own file counts too: there, beyond its definition, only a string or a comment names it.
    elsewhere = words.get(name, set())
    if elsewhere:
        return f"named in {sorted(elsewhere)[0]}: a template, a string or a config may call it"
    if executed is not None and _ran(node, executed.get(path, set())):
        return "ran during the tests: something calls it by reflection"
    return ""


def _ran(node: ast.AST, lines: set[int]) -> bool:
    """A line of the body ran (the `def` line runs at import, whatever calls it)."""
    body = getattr(node, "body", [])
    return any(statement.lineno in lines for statement in body)


def _exported(text: str) -> set[str]:
    found = re.search(r"(?s)__all__\s*[:=][^=].*?[\]\)]", text)
    return set(re.findall(r"[\"'](\w+)[\"']", found.group(0))) if found else set()


def _word_index(repo: Repo) -> dict[str, set[str]]:
    """Where each word appears, in every tracked text file but the lines that define it: the
    names a template, a string, a setting or a script uses without an import vulture sees."""
    index: dict[str, set[str]] = {}
    definition = re.compile(r"^\s*(async\s+def|def|class)\s+(\w+)")
    for name in repo.files:
        if PurePosixPath(name).name in MANIFESTS or PROSE.search(name):
            continue
        text = repo.text(name)
        for line in text.splitlines():
            defined = definition.match(line)
            words = set(re.findall(r"[A-Za-z_]\w{2,}", line))
            if defined and name.endswith(".py"):
                words.discard(defined.group(2))
            for word in words:
                index.setdefault(word, set()).add(name)
    return index


def _is_library(repo: Repo) -> bool:
    """A package others install: built, with no command and no web framework."""
    text = repo.text("pyproject.toml")
    return (
        "[build-system]" in text
        and "[project.scripts]" not in text
        and "django" not in (repo.facts)
    )


def python_dependencies(repo: Repo) -> tuple[list[Candidate], list[Skipped]]:
    """The dependencies of each `[project]` deptry finds no import of (DEP002)."""
    found: list[Candidate] = []
    skipped: list[Skipped] = []
    if shutil.which("uvx") is None:
        return found, skipped
    for folder in proof.projects(repo.root, repo.files, "pyproject.toml"):
        with tempfile.TemporaryDirectory(prefix="kiln-deptry-") as scratch:
            report = Path(scratch) / "deptry.json"
            _run(["uvx", "deptry", ".", "--json-output", str(report)], repo.root / folder)
            try:
                issues = json.loads(report.read_text(encoding="utf-8"))
            except OSError, ValueError:
                continue
        names = [item["module"] for item in issues if item["error"]["code"] == "DEP002"]
        manifest = str(PurePosixPath(folder) / "pyproject.toml")
        kept, dropped = _guard_dependencies(repo, manifest, names, "deptry")
        found += kept
        skipped += dropped
    return found, skipped


def node_unused(repo: Repo) -> tuple[list[Candidate], list[Skipped]]:
    """The files and dependencies knip finds unused, in each package of the repo."""
    runner = ["pnpm", "dlx"] if shutil.which("pnpm") else ["npx", "--yes"]
    found: list[Candidate] = []
    skipped: list[Skipped] = []
    if shutil.which(runner[0]) is None:
        return found, skipped
    for folder in proof.projects(repo.root, repo.files, "package.json"):
        # Without the packages installed, knip's plugins see no test runner, no framework:
        # every test and config would look unused.
        if not (repo.root / folder / "node_modules").is_dir():
            continue
        done = _run([*runner, "knip", "--reporter", "json", "--no-progress"], repo.root / folder)
        try:
            issues = json.loads(done.stdout).get("issues", [])
        except ValueError:
            continue
        for issue in issues:
            for item in issue.get("files", []):
                path = str(PurePosixPath(folder) / item["name"])
                candidate = Candidate(FILE, path, path, "knip", _count(repo, path))
                reason = _guard_file(repo, path, folder)
                if reason:
                    skipped.append(Skipped(candidate, reason))
                else:
                    found.append(candidate)
            names = [
                item["name"]
                for key in ("dependencies", "devDependencies")
                for item in issue.get(key, [])
            ]
            manifest = str(PurePosixPath(folder) / issue["file"])
            kept, dropped = _guard_dependencies(repo, manifest, names, "knip")
            found += kept
            skipped += dropped
    return found, skipped


def _count(repo: Repo, name: str) -> int:
    return len(repo.text(name).splitlines())


def _guard_file(repo: Repo, name: str, folder: str = "") -> str:
    if SENSITIVE_PATH.search(name):
        return "security, parsing, time zones or text encoding: never touched"
    if TEST_OR_CONFIG.search(name):
        return "a test, a script or a config: run by a tool, never imported"
    stem = PurePosixPath(name).stem
    inside = PurePosixPath(name).relative_to(folder or ".").parts
    if inside[0] in {"app", "src"} and len(inside) > 1:
        inside = inside[1:]
    if inside[0] in {
        "pages",
        "layouts",
        "middleware",
        "plugins",
        "server",
        "public",
        "app",
    }:
        return "a folder the framework loads by its path"
    elsewhere = [other for other in repo.files if other != name and stem in repo.text(other)]
    if elsewhere:
        return f"named in {elsewhere[0]}: loaded by a dynamic import or a config"
    return ""


def _guard_dependencies(
    repo: Repo, manifest: str, names: list[str], tool: str
) -> tuple[list[Candidate], list[Skipped]]:
    found: list[Candidate] = []
    skipped: list[Skipped] = []
    plugins = _plugins(repo.root / PurePosixPath(manifest).parent)
    for name in names:
        candidate = Candidate(DEPENDENCY, manifest, name, tool)
        normal = name.lower().replace("_", "-")
        module = normal.replace("-", "_").removeprefix("python_")
        users = [
            other
            for other in repo.files
            if PurePosixPath(other).name not in MANIFESTS
            and not PROSE.search(other)
            and re.search(
                rf"(?i)(?<![\w-])({re.escape(normal)}|{re.escape(module)})(?![\w-])",
                repo.text(other),
            )
        ]
        if normal in LOADED_BY_NAME or normal.startswith(("@types/", "types-", "django-stubs")):
            skipped.append(Skipped(candidate, "loaded by name (a driver, a server, data, types)"))
        elif normal in plugins:
            skipped.append(Skipped(candidate, "a plugin: its entry points load it by name"))
        elif users:
            skipped.append(
                Skipped(candidate, f"named in {users[0]}: loaded by a config or a script")
            )
        else:
            found.append(candidate)
    return found, skipped


def _plugins(project: Path) -> set[str]:
    """The installed distributions of the project's `.venv` that declare entry points other than
    commands: plugins (an instrumentor, a pytest plugin, a backend) found by name at run time."""
    found: set[str] = set()
    for entry_points in project.glob(
        ".venv/lib/python*/site-packages/*.dist-info/entry_points.txt"
    ):
        try:
            text = entry_points.read_text(encoding="utf-8")
        except OSError:
            continue
        if PLUGIN_GROUPS.search(text):
            distribution = entry_points.parent.name.removesuffix(".dist-info").rsplit("-", 1)[0]
            found.add(distribution.lower().replace("_", "-"))
    return found
