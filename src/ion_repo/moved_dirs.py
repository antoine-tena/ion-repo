"""A project renamed: the package's and the plugin's folders moved with what it made of them.

Copier knows files by their path. Under a new `name` or `plugin_name`, it sees the old folder as
removed and a new one as added: the starter files come back beside a package the project
reshaped (`greeting.py`, a `cli.py` next to a `cli/`), the project's own files stay behind in the
old folder, and each file citing the old package conflicts when the rename is all that changed.
So, after Copier, each file of the old folder is merged at its new path (the old render, the
project, the new render), and what cites the old names follows.
"""

import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from ion_repo import migrations, renames
from ion_repo.ion_names import TEXT_SUFFIXES, UNTOUCHED
from ion_repo.shell import capture

BACKEND_DIR = "backend"
PLUGINS_DIR = "plugins"
CONFLICT_LABELS = ("before updating", "base", "after updating")
ION_PREFIX = "ion-"
# Where the project's name is the PyPI distribution's, which a new `name` does not move.
DISTRIBUTION_CITED = (
    r"DISTRIBUTION\s*=\s*[\"']|(?:uv tool install|uv pip install|pip install|pipx install|uvx)\s+"
)


def default_plugin_name(name: str) -> str:
    """As in `copier.yml`: the project's name, without the Ion family's prefix."""
    return name.removeprefix(ION_PREFIX)


def package_of(name: str) -> str:
    return name.replace("-", "_")


@dataclass(frozen=True)
class Renaming:
    """The names of a project before and after Copier; only a name that changed is acted on."""

    old_name: str
    new_name: str
    old_plugin: str | None
    new_plugin: str | None
    python_package: bool
    # The PyPI name when it stayed through the rename.
    distribution: str | None = None

    @property
    def old_package(self) -> str:
        return package_of(self.old_name)

    @property
    def new_package(self) -> str:
        return package_of(self.new_name)

    @property
    def folders(self) -> list[tuple[str, str]]:
        moved = []
        if self.python_package and self.old_package != self.new_package:
            moved.append((f"{BACKEND_DIR}/{self.old_package}", f"{BACKEND_DIR}/{self.new_package}"))
        if self.old_plugin and self.new_plugin and self.old_plugin != self.new_plugin:
            moved.append((f"{PLUGINS_DIR}/{self.old_plugin}", f"{PLUGINS_DIR}/{self.new_plugin}"))
        return moved

    @property
    def renamed(self) -> bool:
        return self.old_name != self.new_name

    def references(self, text: str) -> str:
        """What cites the package or the plugin, safe in any of the project's files."""
        if self.python_package and self.old_package != self.new_package:
            old, new = re.escape(self.old_package), self.new_package
            text = re.sub(rf"\b((?:from|import)\s+){old}\b(?=[.\s])", rf"\g<1>{new}", text)
            text = re.sub(rf"(\"|'){old}\.", rf"\g<1>{new}.", text)
            text = re.sub(rf"\b{BACKEND_DIR}/{old}(?![\w-])", f"{BACKEND_DIR}/{new}", text)
        if self.old_plugin and self.new_plugin and self.old_plugin != self.new_plugin:
            old, new = re.escape(self.old_plugin), self.new_plugin
            text = re.sub(rf"\b{PLUGINS_DIR}/{old}(?![\w-])", f"{PLUGINS_DIR}/{new}", text)
            # A bare `word:` is too common (`host:port`), but `ion-host:domain` can only be a skill.
            before = "/|`|" if self.old_plugin.startswith(ION_PREFIX) else "/|`"
            text = re.sub(rf"(?<![\w/.-])({before}){old}:(?=[a-z])", rf"\g<1>{new}:", text)
            old_id = re.escape(f"{self.old_plugin}@{self.old_name}")
            text = re.sub(
                rf"(?<![\w-]){old_id}(?![\w-])", f"{self.new_plugin}@{self.new_name}", text
            )
        return text

    def words(self, text: str) -> str:
        """Every mention of the project's name, for a file about to be merged with a render under
        the new name; a plugin's new name is no reason to touch the command's."""
        return self._names(self.references(text), r"(?<![\w-])", r"(?![\w-])", r"(?<![\w-])")

    def mentions(self, text: str) -> str:
        """What cites the project in its own files. A path or a URL stays: neither the folder
        nor the GitHub repo moved. A name of one plain word is a common word too (`sweep`):
        only when quoted, or in a code span."""
        return self._names(
            self.references(text),
            r"(?<![\w/.-])",
            r"(?![\w/-])",
            r"(?<=[`\"'])",
        )

    def _names(self, text: str, before: str, after: str, before_plain: str) -> str:
        if not self.renamed:
            return text
        for old, new in ((self.old_name, self.new_name), (self.old_package, self.new_package)):
            start = before if "-" in old or "_" in old else before_plain
            pinned = rf"({DISTRIBUTION_CITED})?" if old == self.distribution else "()"
            text = re.sub(
                rf"{pinned}{start}{re.escape(old)}{after}",
                lambda match, new=new: match.group(0) if match.group(1) else new,
                text,
            )
        if self.old_name.startswith(ION_PREFIX):
            typed = self.old_name.replace(ION_PREFIX, "ion ", 1)
            new_typed = self.new_name.replace(ION_PREFIX, "ion ", 1)
            text = re.sub(rf"(?<![\w-]){typed}(?![\w-])", new_typed, text)
        return text

    def words_beside(self, text: str, render: str) -> str:
        """`words`, sparing a line the new render still holds as it is: it cites a name that did
        not move with the project's (`pypi_name`), and renaming it would invent a change."""
        held = set(render.splitlines())
        return "".join(
            line if line.rstrip("\r\n") in held else self.words(line)
            for line in text.splitlines(keepends=True)
        )

    def mentions_beside(self, text: str, render: str) -> str:
        """`mentions`, sparing a line the new render still holds, as `words_beside`."""
        held = set(render.splitlines())
        return "".join(
            line if line.rstrip("\r\n") in held else self.mentions(line)
            for line in text.splitlines(keepends=True)
        )


def renaming_of(previous: Mapping[str, object], current: Mapping[str, object]) -> Renaming | None:
    """None when the answers say nothing of a name that moved (a template without `name`)."""
    previous, current = renames.answers(dict(previous)), renames.answers(dict(current))
    old_name, new_name = previous.get("name"), current.get("name")
    if not isinstance(old_name, str) or not isinstance(new_name, str):
        return None
    distribution = (
        current.get("pypi_name") if current.get("pypi_name") == previous.get("pypi_name") else None
    )
    had_plugin = bool(previous.get("claude_plugin"))
    has_plugin = bool(current.get("claude_plugin"))
    renaming = Renaming(
        old_name=old_name,
        new_name=new_name,
        # Before `plugin_name`, the plugin bore the project's name.
        old_plugin=str(previous.get("plugin_name") or old_name) if had_plugin else None,
        new_plugin=str(current.get("plugin_name") or new_name) if has_plugin else None,
        python_package=previous.get("backend") == "cli" and current.get("backend") == "cli",
        distribution=distribution if isinstance(distribution, str) else None,
    )
    return renaming if renaming.renamed or renaming.folders else None


def move_renamed_dirs(
    root: Path,
    renaming: Renaming,
    previous_answers: Mapping[str, object],
    source: str,
    ref: str | None,
    *,
    spared: Iterable[str] = (),
) -> list[str]:
    """After Copier; returns what was done. `spared`: the files `ion repo update` never writes
    (frozen, kept), whose folder stays where the project has it."""
    spared = set(spared)
    done = []
    folders = [
        (old, new)
        for old, new in renaming.folders
        if (files := _committed_files(root, old)) and not spared.intersection(files)
    ]
    with tempfile.TemporaryDirectory() as tmp:
        new_render = None
        if folders or renaming.renamed:
            new_render = migrations.render(
                source, ref, migrations.raw_answers(root), Path(tmp) / "new"
            )
        if folders and new_render is not None:
            previous_commit = str(previous_answers.get("_commit", "")) or None
            old_render = migrations.render(
                source, previous_commit, previous_answers, Path(tmp) / "old"
            )
            for old, new in folders:
                _move_folder(root, old, new, old_render, new_render, renaming)
                done.append(f"{old}/ moved to {new}/")
        if _rewrite_project(root, renaming, spared, new_render):
            done.append("what cites the old names follows the new ones")
    return done


def _committed_files(root: Path, folder: str) -> list[str]:
    listed = capture(["git", "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", folder], root)
    return [name for name in listed.split("\0") if name]


def _committed_bytes(root: Path, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"HEAD:{path}"], cwd=root, capture_output=True, check=True
    ).stdout


def _read(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


def _move_folder(
    root: Path, old: str, new: str, old_render: Path, new_render: Path, renaming: Renaming
) -> None:
    committed = _committed_files(root, old)
    for path in committed:
        relative = path.removeprefix(f"{old}/")
        target = root / new / relative
        merged = _merged_file(
            ours=_committed_bytes(root, path),
            base=_read(old_render / path),
            theirs=_read(new_render / new / relative),
            renaming=renaming,
        )
        if merged is None:
            target.unlink(missing_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(merged)
    # What the project removed from the template's folder stays removed under the new name.
    kept = {path.removeprefix(f"{old}/") for path in committed}
    old_folder = old_render / old
    for rendered in old_folder.rglob("*") if old_folder.is_dir() else ():
        relative = rendered.relative_to(old_folder).as_posix()
        if rendered.is_file() and relative not in kept:
            (root / new / relative).unlink(missing_ok=True)
    _prune_empty(root / new)
    _remove_old_folder(root, old, new)


def _merged_file(
    *, ours: bytes, base: bytes | None, theirs: bytes | None, renaming: Renaming
) -> bytes | None:
    """The file at its new path; None when the template dropped it and the project hadn't
    touched it."""
    if base is None and theirs is None:
        return ours  # the project's own
    if theirs is None:
        return None if ours == base else ours
    if ours == base:
        return theirs
    try:
        render = theirs.decode()
        merged = _merge_text(
            base=renaming.words_beside(base.decode(), render) if base is not None else "",
            ours=renaming.words_beside(ours.decode(), render),
            theirs=render,
        )
    except UnicodeDecodeError:
        return ours
    return merged.encode()


def _merge_text(*, base: str, ours: str, theirs: str) -> str:
    """A conflict stays marked in the file, as Copier leaves them."""
    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / name for name in ("ours", "base", "theirs")]
        for path, text in zip(paths, (ours, base, theirs), strict=True):
            path.write_text(text)
        labels = [flag for label in CONFLICT_LABELS for flag in ("-L", label)]
        merged = subprocess.run(
            ["git", "merge-file", "-p", *labels, *map(str, paths)],
            capture_output=True,
            text=True,
            check=False,
        )
    return merged.stdout


def _prune_empty(folder: Path) -> None:
    for path in sorted(folder.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def _remove_old_folder(root: Path, old: str, new: str) -> None:
    """Only ignored files are left beside the committed ones (Copier needs a clean tree): moved,
    build caches apart, then the folder goes."""
    folder = root / old
    if not folder.is_dir():
        return
    committed = set(_committed_files(root, old))
    for path in folder.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or relative in committed or "__pycache__" in path.parts:
            continue
        target = root / new / path.relative_to(folder)
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            path.replace(target)
    shutil.rmtree(folder)


def _rewrite_project(
    root: Path, renaming: Renaming, spared: set[str], new_render: Path | None
) -> bool:
    listed = capture(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], root)
    changed = False
    for name in sorted(set(listed.split("\0"))):
        path = root / name
        if (
            not name
            or name in UNTOUCHED
            or name in spared
            or path.suffix not in TEXT_SUFFIXES
            or not path.is_file()
        ):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        rendered = new_render / name if new_render is not None else None
        rewritten = (
            renaming.mentions_beside(text, rendered.read_text())
            if rendered is not None and rendered.is_file()
            else renaming.mentions(text)
        )
        if rewritten != text:
            path.write_text(rewritten)
            changed = True
    return changed
