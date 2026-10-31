"""What a repo is made of, read from its tracked files in milliseconds: the facts a rule's
`applies` asks for (`django`, `github-actions`…). Any repo, made by ion-repo or not."""

import codecs
import functools
import glob
import json
import re
import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from ion_repo.grid import forge

# Facts a rule may ask for, and what tells them.
KNOWN_FACTS = (
    "python",
    "uv",
    "django",
    "javascript",
    "typescript",
    "pnpm",
    "nuxt",
    "vue",
    "github-actions",
    "containers",
    "agent",
    "github",
)
# A coding agent's folder: the repo is worked with one (on disk, even when git ignores it).
AGENT_FOLDERS = (".claude", ".cursor", ".codex", ".gemini")
IGNORED_PARTS = frozenset({".git", "node_modules", ".venv", "__pycache__", "dist", ".nuxt"})
# A NUL byte in the first 8 KB: a binary file, never text (git's own test).
BINARY_PROBE = 8192
# A source with a line longer than this: minified or generated, which code rules leave aside
# (prose, Markdown or HTML, has long lines of its own).
MINIFIED_LINE = 1000
MINIFIABLE = frozenset({".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".css", ".py"})
# A text that is not UTF-8: its byte order mark first, then the legacy encodings of Windows and
# of Western Europe (latin-1 decodes anything, so it always ends the search).
BOMS = (
    (codecs.BOM_UTF8, "utf-8-sig"),
    (codecs.BOM_UTF16_LE, "utf-16"),
    (codecs.BOM_UTF16_BE, "utf-16"),
)
LEGACY_ENCODINGS = ("cp1252", "latin-1")


@dataclass(frozen=True)
class Repo:
    root: Path
    files: tuple[str, ...]  # tracked files, POSIX paths relative to the root
    facts: frozenset[str]
    # Python and JavaScript packages the repo declares, by their public names.
    dependencies: frozenset[str] = frozenset()
    # Read once per run: a later read (after `ion repo fix` writes) takes a new `read_repo`.
    texts: dict[str, str] = field(default_factory=dict, compare=False, hash=False, repr=False)
    # What reading found: binary files, and texts that are not UTF-8 with their encoding.
    binaries: set[str] = field(default_factory=set, compare=False, hash=False, repr=False)
    encodings: dict[str, str] = field(default_factory=dict, compare=False, hash=False, repr=False)

    def matching(self, *patterns: str) -> list[str]:
        """Tracked files matching any of the glob `patterns` (`**` crosses folders)."""
        compiled = [_glob(pattern) for pattern in patterns]
        return [name for name in self.files if any(regex.match(name) for regex in compiled)]

    def text(self, name: str) -> str:
        """A tracked file's text, read once for every rule; "" when it cannot be read or is
        binary. A text that is not UTF-8 is decoded all the same, never read as empty (an empty
        text passes every rule that looks for a pattern), and its encoding kept."""
        if name not in self.texts:
            self.texts[name] = self._decode(name)
        return self.texts[name]

    def is_code(self, name: str) -> bool:
        """Text a code rule reads: neither binary nor minified."""
        text = self.text(name)
        if name in self.binaries:
            return False
        if PurePosixPath(name).suffix not in MINIFIABLE:
            return True
        return all(len(line) <= MINIFIED_LINE for line in text.splitlines())

    def _decode(self, name: str) -> str:
        try:
            data = (self.root / name).read_bytes()
        except OSError:
            return ""
        for bom, encoding in BOMS:
            if data.startswith(bom):
                if encoding != "utf-8-sig":
                    self.encodings[name] = encoding
                return data.decode(encoding, errors="replace")
        if b"\0" in data[:BINARY_PROBE]:
            self.binaries.add(name)
            return ""
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            pass
        for encoding in LEGACY_ENCODINGS:
            try:
                text = data.decode(encoding)
            except UnicodeDecodeError:
                continue
            self.encodings[name] = encoding
            return text
        return ""


@functools.cache
def _glob(pattern: str) -> re.Pattern[str]:
    return re.compile(glob.translate(pattern, recursive=True, include_hidden=True))


def read_repo(root: Path) -> Repo:
    files = tuple(tracked_files(root))
    dependencies = _python_dependencies(root, files) | _node_dependencies(root, files)
    return Repo(root, files, frozenset(detect_facts(root, files)), frozenset(dependencies))


def tracked_files(root: Path) -> list[str]:
    """`git ls-files` (ignored files left out); every file outside node_modules and the like
    when the folder is not a git repo."""
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if listed.returncode == 0:
        return [name for name in listed.stdout.decode().split("\0") if name]
    return [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(root).parts)
    ]


def detect_facts(root: Path, files: tuple[str, ...]) -> set[str]:
    names = {PurePosixPath(name).name for name in files}
    facts: set[str] = set()
    python_deps = _python_dependencies(root, files)
    node_deps = _node_dependencies(root, files)
    if names & {"pyproject.toml", "setup.py", "requirements.txt"} or any(
        name.endswith(".py") for name in files
    ):
        facts.add("python")
    if "uv.lock" in names:
        facts.add("uv")
    if "django" in python_deps or "manage.py" in names:
        facts.add("django")
    if "package.json" in names:
        facts.add("javascript")
    if "tsconfig.json" in names or any(name.endswith((".ts", ".tsx")) for name in files):
        facts.add("typescript")
    if "pnpm-lock.yaml" in names:
        facts.add("pnpm")
    if "nuxt" in node_deps or any(name.startswith("nuxt.config.") for name in names):
        facts.add("nuxt")
    if "vue" in node_deps or "nuxt" in facts:
        facts.add("vue")
    if any(PurePosixPath(name).full_match(".github/workflows/*.y*ml") for name in files):
        facts.add("github-actions")
    if any(
        name in {"Dockerfile", "Containerfile"} or re.fullmatch(r"(docker-)?compose.*\.ya?ml", name)
        for name in names
    ):
        facts.add("containers")
    if any((root / folder).is_dir() for folder in AGENT_FOLDERS):
        facts.add("agent")
    if forge.github_slug(root) is not None:
        facts.add("github")
    return facts


def _python_dependencies(root: Path, files: tuple[str, ...]) -> set[str]:
    found: set[str] = set()
    for name in files:
        path = PurePosixPath(name)
        if path.name == "pyproject.toml":
            try:
                project = tomllib.loads((root / name).read_text(encoding="utf-8"))
            except OSError, tomllib.TOMLDecodeError:
                continue
            declared = project.get("project", {}).get("dependencies", [])
            found |= {_requirement_name(item) for item in declared if isinstance(item, str)}
        elif path.name.startswith("requirements") and path.suffix == ".txt":
            try:
                lines = (root / name).read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            found |= {_requirement_name(line) for line in lines if line.strip()[:1].isalpha()}
    return found


def _node_dependencies(root: Path, files: tuple[str, ...]) -> set[str]:
    found: set[str] = set()
    for name in files:
        if PurePosixPath(name).name != "package.json" or "node_modules/" in name:
            continue
        try:
            package = json.loads((root / name).read_text(encoding="utf-8"))
        except OSError, ValueError:
            continue
        for section in ("dependencies", "devDependencies"):
            declared = package.get(section, {})
            if isinstance(declared, dict):
                found |= set(declared)
    return found


def _requirement_name(requirement: str) -> str:
    """`Django>=5.2` → `django`."""
    return re.split(r"[\s<>=!~;\[(@]", requirement.strip(), maxsplit=1)[0].lower()
