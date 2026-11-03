"""The pieces other Ion tools bring to a project (ion-repo#T-394, docs/reference.md, "Pieces of
other Ion tools"). A tool ships its piece as a Copier template in its own repo (`copier.yml`,
`piece/`, answers in `.copier-answers.<tool>.yml`); `ion repo new` lays each piece after the
template, `ion repo update` updates each one after it. The table is `pieces` in `copier.yml`,
which the generated `.claude/settings.json` reads too."""

import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from subprocess import CalledProcessError

import copier
import yaml
from copier.errors import CopierError
from ion_score import ui
from plumbum import ProcessExecutionError

from ion_repo import migrations
from ion_repo.shell import quiet_git
from ion_repo.versions import follows_candidates

TEMPLATE_CONFIG = "copier.yml"
# A piece's repo that asks for a password (private, no access) fails at once instead of waiting
# for a terminal nobody watches.
NO_PROMPT = {"GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "", "SSH_ASKPASS": ""}
REACH_TIMEOUT = 30


@dataclass(frozen=True)
class Piece:
    tool: str  # `ion-host`: its catalogue's name too
    repo: str  # `antoine-tena/ion-host`: the catalogue on GitHub
    plugin: str  # `host`: enabled as `host@ion-host`
    when: Mapping[str, object]  # the answers that bring it
    template: str  # the tool's repo holding `copier.yml` and `piece/`; empty: skills only

    @property
    def answers_file(self) -> str:
        return f".copier-answers.{self.tool}.yml"


def table(source: str) -> list[Piece]:
    """The pieces of the template at `source`: a local template (ion-repo development, a copy)
    is read as it is; the published one is the tool's own release, whose `copier.yml` ships with
    it."""
    local = Path(source) / TEMPLATE_CONFIG
    if local.is_file():
        text = local.read_text(encoding="utf-8")
    else:
        packaged = resources.files("ion_repo") / TEMPLATE_CONFIG
        in_repo = Path(__file__).resolve().parents[2] / TEMPLATE_CONFIG
        text = (packaged if packaged.is_file() else in_repo).read_text(encoding="utf-8")
    loaded = yaml.safe_load(text) or {}
    rows = loaded.get("pieces", {}).get("default", [])
    return [
        Piece(
            tool=row["tool"],
            repo=row["repo"],
            plugin=row["plugin"],
            when=row.get("when") or {},
            template=row.get("template") or "",
        )
        for row in rows
    ]


def brought(piece: Piece, answers: Mapping[str, object]) -> bool:
    """The answers bring the piece; a tool's own repo never takes its piece."""
    return answers.get("name") != piece.tool and all(
        answers.get(key) == value for key, value in piece.when.items()
    )


def apply_pieces(root: Path, source: str, spared: list[str]) -> None:
    """Each piece the answers bring, after the template: laid the first time, updated after.
    All of ion-repo's answers are passed to it (a piece reads `title` without asking it), never
    recorded in its answers file. A piece that cannot be fetched gets a note, its files left as
    they are, and the rest goes on."""
    answers = {
        key: value for key, value in migrations.raw_answers(root).items() if not key.startswith("_")
    }
    for piece in table(source):
        if not piece.template or not brought(piece, answers):
            continue
        recorded = _recorded_source(root / piece.answers_file)
        src = recorded or piece.template
        if not reachable(src):
            ui.note(
                f"{piece.tool}'s piece left as it is: {src} cannot be reached from this machine "
                "(a private repo this account cannot read, or offline). With an account that "
                "can read it: gh auth login, gh auth setup-git, then ion repo update."
            )
            continue
        try:
            with _no_prompt(), quiet_git():
                if recorded:
                    _update_piece(root, piece, answers, spared)
                else:
                    _lay_piece(root, piece, src, answers, spared)
        except (CopierError, ProcessExecutionError, CalledProcessError, OSError) as error:
            ui.note(f"{piece.tool}'s piece left as it is: {error}")


def reachable(src: str) -> bool:
    if Path(src).is_dir():
        return True
    try:
        with _no_prompt():
            found = subprocess.run(
                ["git", "ls-remote", "-q", "--exit-code", src, "HEAD"],
                capture_output=True,
                check=False,
                timeout=REACH_TIMEOUT,
            )
    except subprocess.TimeoutExpired:
        return False
    return found.returncode == 0


def _lay_piece(
    root: Path, piece: Piece, src: str, answers: Mapping[str, object], spared: list[str]
) -> None:
    """The first time: rendered aside, then laid without overwriting a file. A file the
    template has just dropped for this piece (the handover) comes back as the project had it, so
    a change made by hand survives the move; the tool's next release then merges in three
    ways."""
    with tempfile.TemporaryDirectory() as scratch:
        rendered = Path(scratch) / "piece"
        copier.run_copy(
            src,
            rendered,
            data=dict(answers),
            vcs_ref=_revision(src),
            use_prereleases=follows_candidates(),
            defaults=True,
            quiet=True,
            unsafe=False,
        )
        laid, kept = 0, 0
        for path in sorted(rendered.rglob("*")):
            name = path.relative_to(rendered).as_posix()
            target = root / name
            if path.is_dir() or name in spared or name.startswith(".git/"):
                continue
            if name != piece.answers_file and (target.exists() or _restore(root, name)):
                kept += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            laid += 1
    ui.note(f"{piece.tool}'s piece laid: {laid} files written, {kept} kept as the repo had them.")


def _update_piece(
    root: Path, piece: Piece, answers: Mapping[str, object], spared: list[str]
) -> None:
    """The next times: Copier's update, three-way, conflicts inline like the template's. Copier
    wants a clean tree and the template has just changed this one: it runs on a clone of the
    last commit, and only what it changed comes back. Copier renders the old revision with the
    piece's recorded answers alone: ion-repo's are added to them in the clone (committed there,
    never in the repo), or a line reading `title` would conflict at each release of the tool."""
    with tempfile.TemporaryDirectory() as scratch:
        # Resolved: macOS's /var is a link to /private/var, and Copier compares the two.
        clone = Path(scratch).resolve() / "repo"
        subprocess.run(
            ["git", "clone", "-q", "--no-hardlinks", str(root), str(clone)],
            check=True,
            capture_output=True,
        )
        answers_path = clone / piece.answers_file
        recorded = yaml.safe_load(answers_path.read_text(encoding="utf-8")) or {}
        answers_path.write_text(yaml.safe_dump({**answers, **recorded}), encoding="utf-8")
        _clone_commit(clone)
        src = _recorded_source(answers_path) or piece.template
        copier.run_update(
            clone,
            answers_file=piece.answers_file,
            data=dict(answers),
            vcs_ref=_revision(src),
            use_prereleases=follows_candidates(),
            exclude=spared,
            defaults=True,
            skip_answered=True,
            overwrite=True,
            conflict="inline",
            quiet=True,
            unsafe=False,
        )
        changed = _changed_files(clone)
        for name in changed:
            source, target = clone / name, root / name
            if source.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            elif target.exists():
                target.unlink()
    if changed:
        ui.note(f"{piece.tool}'s piece updated: {', '.join(changed)}.")


def _clone_commit(clone: Path) -> None:
    """A commit of the throwaway clone, under an identity of its own: Copier wants it clean."""
    for args in (["add", "-A"], ["commit", "-q", "--no-verify", "-m", "ion-repo's answers"]):
        subprocess.run(
            ["git", "-c", "user.name=ion-repo", "-c", "user.email=ion-repo@localhost", *args],
            cwd=clone,
            check=True,
            capture_output=True,
        )


def _changed_files(clone: Path) -> list[str]:
    listed = subprocess.run(
        ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
        cwd=clone,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    # `XY name`, NUL-separated; a rename adds its old name as the next entry.
    names, entries = [], iter(listed.split("\0"))
    for entry in entries:
        if not entry:
            continue
        names.append(entry[3:])
        if entry[0] == "R":
            names.append(next(entries))
    return sorted(names)


def _restore(root: Path, name: str) -> bool:
    """A file of the last commit the working tree no longer has, put back."""
    shown = subprocess.run(
        ["git", "show", f"HEAD:{name}"], cwd=root, capture_output=True, check=False
    )
    if shown.returncode != 0:
        return False
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(shown.stdout)
    mode = subprocess.run(
        ["git", "ls-tree", "--format=%(objectmode)", "HEAD", "--", name],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    if mode == "100755":
        target.chmod(target.stat().st_mode | 0o111)
    return True


def _recorded_source(answers_file: Path) -> str:
    if not answers_file.is_file():
        return ""
    loaded = yaml.safe_load(answers_file.read_text(encoding="utf-8")) or {}
    return str(loaded.get("_src_path") or "") if isinstance(loaded, dict) else ""


def _revision(src: str) -> str | None:
    """A local template at its last commit; a tool's repo at its latest release (candidates on
    the channels that follow them, through `use_prereleases`)."""
    return "HEAD" if Path(src).is_dir() else None


@contextmanager
def _no_prompt() -> Iterator[None]:
    saved = {key: os.environ.get(key) for key in NO_PROMPT}
    os.environ.update(NO_PROMPT)
    try:
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
