"""What every rule works on: the checked repo, its files and its configuration, plus the way a
failure is written and an exception justified."""

from __future__ import annotations

import re
import subprocess
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

# Parameters of one rule, or the whole configuration, as read in `charter.toml`.
Params = dict[str, Any]
MAX_LISTED = 15


class Repo:
    """The checked repo: its root, its configuration (`charter.toml`) and its files."""

    def __init__(self, root: Path, config: Params) -> None:
        self.root = root
        self.config = config
        # Path fragments that every rule ignores (e.g. "/migrations/").
        self.excluded: list[str] = list(config.get("exclude", []))
        # Generated files: their list lives in `.gitattributes` (attribute linguist-generated).
        self.generated = self.generated_files()
        # Patterns waived for the rule being checked (`kiln-waivers.toml`).
        self.waived: list[str] = []
        # The one file checked after an edit (`charter file`), None for the whole repo.
        self.only: str | None = None

    def generated_files(self) -> set[str]:
        """Files `.gitattributes` marks linguist-generated, new ones included: `kiln contract`
        writes openapi.json before anyone adds it. A pathspec `:(attr:…)` would miss a new
        file in a new folder (git does not walk into an untracked folder for it)."""
        files = self.git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
        attributes = subprocess.run(
            ["git", "check-attr", "-z", "--stdin", "linguist-generated"],
            cwd=self.root,
            input=files,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.split("\0")
        # check-attr -z answers path, attribute, value for each path.
        triples = zip(attributes[::3], attributes[2::3], strict=False)
        return {path for path, value in triples if value == "true"}

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True, check=False
        ).stdout

    def tracked(self, patterns: str | list[str], *, excluded: bool = True) -> list[Path]:
        """Tracked files AND new files that are not ignored: `git ls-files` alone missed a module
        created but not yet added, and the local check passed on code CI would have refused.
        A file deleted but still in the index is left out."""
        patterns = [patterns] if isinstance(patterns, str) else patterns
        if self.only is not None:
            return self._only_if_matched(patterns, excluded=excluded)
        waived = [f":(exclude){pattern}" for pattern in self.waived]
        # A pathspec of excludes alone is read against the current directory, not the root.
        patterns = patterns or ([":/"] if waived else [])
        listed = self.git(
            "ls-files", "--cached", "--others", "--exclude-standard", "--", *patterns, *waived
        ).split()
        kept = dict.fromkeys(
            path
            for path in listed
            if (self.root / path).exists()
            and not (excluded and any(fragment in path for fragment in self.excluded))
        )
        return [self.root / path for path in kept]

    def _only_if_matched(self, patterns: list[str], *, excluded: bool) -> list[Path]:
        """`tracked` for a single file, without listing the repo: git's pathspecs, where `*`
        crosses `/` and a folder covers what it holds, are matched in Python."""
        path = self.only or ""

        def matches(pattern: str) -> bool:
            folder = pattern.rstrip("/") + "/"
            return fnmatchcase(path, pattern) or path.startswith(folder)

        kept = (
            (not patterns or any(map(matches, patterns)))
            and not any(map(matches, self.waived))
            and not (excluded and any(fragment in path for fragment in self.excluded))
        )
        return [self.root / path] if kept else []

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.root))

    def is_generated(self, path: Path) -> bool:
        return self.rel(path) in self.generated

    # Names of kiln 0.3, still used by a project's own rules (`local_rules`).
    @property
    def racine(self) -> Path:
        return self.root

    def suivis(self, patterns: str | list[str], *, exclus: bool = True) -> list[Path]:
        return self.tracked(patterns, excluded=exclus)

    def engendre(self, path: Path) -> bool:
        return self.is_generated(path)


def failure(rule: str, message: str, culprits: list[str]) -> str:
    listed = "\n".join(f"      {culprit}" for culprit in culprits[:MAX_LISTED])
    more = len(culprits) - MAX_LISTED
    rest = f"\n      … and {more} more" if more > 0 else ""
    return f"  [{rule}] {message}\n{listed}{rest}"


def justified(lines: list[str], number: int, *markers: str, above: int = 8) -> bool:
    """An exception is justified by a comment (`# <marker>: reason`) in the lines above line
    `number` (1-based), that line included. Each marker is matched case-insensitively, with or
    without a space before the colon (`# Constant time: …`, `# Temps constant : …`)."""
    block = "\n".join(lines[max(0, number - above - 1) : number])
    return any(re.search(rf"#\s*{marker}\s*:", block, re.IGNORECASE) for marker in markers)


def outside_tests(files: list[Path]) -> list[Path]:
    return [path for path in files if "tests" not in path.parts]
