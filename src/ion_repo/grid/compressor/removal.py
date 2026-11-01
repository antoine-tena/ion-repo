"""How a candidate leaves the repo: a definition cut from its file, a file deleted, a dependency
removed through the package manager so that the lockfile and the environment follow.

Every removal works on the tree as it is now, earlier removals included: a definition is found
again by its dotted name, never by a line number that has moved.
"""

import ast
import json
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath

from ion_repo.grid.compressor.candidates import CODE, DEPENDENCY, FILE, Candidate, find

PYTHON_REQUIREMENT = r"(?im)^\s*[\"']?{name}\s*([<>=~!;\[\"',@\s]|$).*\n?"


def remove(root: Path, candidate: Candidate) -> bool:
    """The candidate removed; False when it is no longer there to remove."""
    if candidate.kind == CODE:
        return _cut_definition(root / candidate.path, candidate.name)
    if candidate.kind == FILE:
        target = root / candidate.path
        if not target.is_file():
            return False
        target.unlink()
        return True
    if candidate.kind == DEPENDENCY:
        return _drop_dependency(root, candidate)
    return False


def _cut_definition(path: Path, qualname: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except OSError, SyntaxError, UnicodeDecodeError:
        return False
    found = find(tree, qualname)
    if found is None:
        return False
    node, parents = found
    lines = text.splitlines(keepends=True)
    start = min([node.lineno, *(item.lineno for item in node.decorator_list)]) - 1
    end = node.end_lineno or node.lineno
    # The comment block just above belongs to it.
    while start > 0 and lines[start - 1].lstrip().startswith("#"):
        start -= 1
    owner = parents[-1] if parents else tree
    body = getattr(owner, "body", [])
    kept = lines[:start]
    if len(body) == 1:
        # The last statement of a class: `pass` keeps it valid.
        line = lines[node.lineno - 1]
        indent = line[: len(line) - len(line.lstrip())]
        kept.append(f"{indent}pass\n")
    kept += lines[end:]
    path.write_text(_tidy_blank_lines("".join(kept)), encoding="utf-8")
    return True


def _tidy_blank_lines(text: str) -> str:
    """No more blank lines in a row than PEP 8 allows (two), none at the end of the file."""
    return re.sub(r"\n{4,}", "\n\n\n", text).rstrip("\n") + "\n"


def _drop_dependency(root: Path, candidate: Candidate) -> bool:
    manifest = root / candidate.path
    if not manifest.is_file():
        return False
    if PurePosixPath(candidate.path).name == "package.json":
        return _drop_node_dependency(manifest, candidate.name)
    project = manifest.parent
    if (project / "uv.lock").is_file() and shutil.which("uv") is not None:
        done = subprocess.run(
            ["uv", "remove", "--quiet", candidate.name],
            cwd=project,
            capture_output=True,
            check=False,
        )
        return done.returncode == 0
    pattern = re.compile(PYTHON_REQUIREMENT.format(name=re.escape(candidate.name)))
    changed = False
    for target in [manifest, *project.glob("requirements*.txt")]:
        text = target.read_text(encoding="utf-8")
        kept = pattern.sub("", text)
        if kept != text:
            target.write_text(kept, encoding="utf-8")
            changed = True
    return changed


def _drop_node_dependency(manifest: Path, name: str) -> bool:
    text = manifest.read_text(encoding="utf-8")
    package = json.loads(text)
    changed = False
    for section in ("dependencies", "devDependencies"):
        if name in package.get(section, {}):
            del package[section][name]
            changed = True
    if changed:
        indent = re.search(r"\n(\s+)\"", text)
        manifest.write_text(
            json.dumps(package, indent=len(indent.group(1)) if indent else 2, ensure_ascii=False)
            + "\n",
            encoding="utf-8",
        )
    return changed


def sync_environment(root: Path, folders: set[str]) -> None:
    """The installed packages of each project in `folders` brought back to its manifest, after
    a removal or an undo: a test run on a package still installed proves nothing."""
    for folder in sorted(folders):
        project = root / folder
        if (project / "package.json").is_file():
            manager = "pnpm" if (project / "pnpm-lock.yaml").is_file() else "npm"
            if shutil.which(manager):
                subprocess.run([manager, "install"], cwd=project, capture_output=True, check=False)
        if (project / "uv.lock").is_file() and shutil.which("uv"):
            subprocess.run(
                ["uv", "sync", "--quiet", "--exact"], cwd=project, capture_output=True, check=False
            )


def tidy_imports(root: Path, paths: list[str]) -> None:
    """Imports a removal left unused, removed by ruff (its safe fix only)."""
    python = [name for name in paths if name.endswith(".py") and (root / name).is_file()]
    if python and shutil.which("uvx"):
        subprocess.run(
            ["uvx", "ruff", "check", "--fix", "--select", "F401", "--quiet", *python],
            cwd=root,
            capture_output=True,
            check=False,
        )
    for name in python:
        path = root / name
        text = path.read_text(encoding="utf-8")
        # ruff leaves the lines around a removed import: none before the first statement.
        if text.startswith("\n"):
            path.write_text(text.lstrip("\n"), encoding="utf-8")
