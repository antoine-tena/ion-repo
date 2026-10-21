"""Converters of `kiln fix`: Python (T-128)."""

import re
import shutil
import subprocess
import tomllib
from pathlib import PurePosixPath

from kiln.grid.facts import Repo
from kiln.grid.fixers import Fixer, register
from kiln.shell import KilnError

BACKPORT = re.compile(
    r"(?i)^\s*[\"']?(typing|enum34|futures|pathlib|dataclasses)\s*([<>=~!;\"',]|$)"
)
RUFF_SELECT = ("E4", "E7", "E9", "F", "I", "UP")
SAFE_FIXES = "I,UP,RUF100"


def _write(repo: Repo, name: str, text: str) -> None:
    (repo.root / name).write_text(text, encoding="utf-8")


def remove_backports(repo: Repo) -> list[str]:
    """Lines naming `typing`, `enum34`, `futures`, `pathlib` or `dataclasses` from PyPI removed."""
    changed = []
    for name in repo.matching("**/requirements*.txt", "**/pyproject.toml"):
        lines = repo.text(name).splitlines(keepends=True)
        kept = [line for line in lines if not BACKPORT.match(line)]
        if kept != lines:
            _write(repo, name, "".join(kept))
            changed.append(name)
    return changed


def _pinned(text: str) -> bool:
    wanted = [line.split("#")[0].strip() for line in text.splitlines()]
    return all("==" in line for line in wanted if line and not line.startswith("-"))


def lock_requirements(repo: Repo) -> list[str]:
    """Each loose `requirements*.txt` becomes its `.in` source, compiled by uv into a pinned
    `.txt`: images and scripts that install it keep working, now on exact versions."""
    loose = [name for name in repo.matching("**/requirements*.txt") if not _pinned(repo.text(name))]
    if not loose:
        return []
    if shutil.which("uv") is None:
        raise KilnError("uv is needed to compile the requirements: https://docs.astral.sh/uv/")
    changed: list[str] = []
    failed: list[str] = []
    for name in loose:
        source = str(PurePosixPath(name).with_suffix(".in"))
        (repo.root / name).rename(repo.root / source)
        done = subprocess.run(
            ["uv", "pip", "compile", "--quiet", "--no-header", source, "-o", name],
            cwd=repo.root,
            capture_output=True,
            text=True,
            check=False,
        )
        if done.returncode != 0:
            (repo.root / source).rename(repo.root / name)
            failed.append(f"{name}: {done.stderr.strip().splitlines()[-1][:160]}")
            continue
        changed += [source, name]
    if failed and not changed:
        raise KilnError("uv could not compile " + "; ".join(failed))
    return changed


def _line_length(repo: Repo) -> int | None:
    """The line length the repo already uses, from black or flake8."""
    try:
        black = tomllib.loads(repo.text("pyproject.toml") or "").get("tool", {}).get("black", {})
    except tomllib.TOMLDecodeError:
        black = {}
    if isinstance(black.get("line-length"), int):
        return int(black["line-length"])
    for name in (".flake8", "setup.cfg", "tox.ini"):
        found = re.search(r"(?m)^max-line-length\s*=\s*(\d+)", repo.text(name))
        if found:
            return int(found.group(1))
    return None


def add_ruff(repo: Repo) -> list[str]:
    """ruff set up in `pyproject.toml` (the line length of black or flake8 carried over), then
    its safe fixes applied: imports sorted, syntax of the supported Pythons, unused noqa."""
    name = "pyproject.toml"
    text = repo.text(name)
    length = _line_length(repo)
    section = "\n[tool.ruff]\n" + (f"line-length = {length}\n" if length else "")
    section += "\n[tool.ruff.lint]\nselect = [" + ", ".join(f'"{code}"' for code in RUFF_SELECT)
    section += "]\n"
    _write(repo, name, (text.rstrip("\n") + "\n" if text else "") + section)
    if shutil.which("uvx") is not None:
        subprocess.run(
            ["uvx", "ruff", "check", "--fix", "--select", SAFE_FIXES, "--quiet", "."],
            cwd=repo.root,
            capture_output=True,
            check=False,
        )
    return [name]


def ts_expect_error(repo: Repo) -> list[str]:
    """`@ts-ignore` → `@ts-expect-error`: the type checker then says when it is no longer needed."""
    changed = []
    for name in repo.matching("**/*.ts", "**/*.tsx", "**/*.vue"):
        text = repo.text(name)
        if "@ts-ignore" in text:
            _write(repo, name, re.sub(r"@ts-ignore\b", "@ts-expect-error", text))
            changed.append(name)
    return changed


register(Fixer("remove_backports", remove_backports, "obsolete backports removed"))
register(
    Fixer(
        "lock_requirements",
        lock_requirements,
        "requirements compiled to exact versions",
        network=True,
    )
)
register(Fixer("add_ruff", add_ruff, "ruff set up, its safe fixes applied", network=True))
register(Fixer("ts_expect_error", ts_expect_error, "@ts-expect-error rather than @ts-ignore"))
