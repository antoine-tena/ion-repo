#!/usr/bin/env python3
"""PostToolUse (Edit/Write): checks the edited file, to see the violation right away.

ruff for a .py (the nearest `.venv/bin/ruff` going up), ESLint with cache for a .ts/.vue/.js
(the nearest `node_modules/.bin/eslint`), then the repo's charter: `charter file`, the bans on
the edited file alone (ratchets and floors run at commit and in CI), if it has a `charter.toml`
(`charte.toml` before kiln 0.4), otherwise the script named by
`ION_REPO_CHARTER_SCRIPT` (`PROJET_CHARTE` before 0.4; path relative to the root of the repo) in its
`.claude/settings.json`. A charter violation is reported once, then again when it changes:
ongoing debt does not repeat its report at every edit. Works in a worktree too. Exit 2 = the
report is sent back to the agent; without the tool installed, stay quiet.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ESLINT_SUFFIXES = (".ts", ".vue", ".js", ".mjs")
CHARTER_SUFFIXES = (".py", ".ts", ".vue", ".js", ".mjs", ".css")
# End of the useful report: the rest lists unverified rules, noise at every edit (the engine
# before kiln 0.4.0 listed them all; today's counts them in one line).
LEGACY_REPORT_END = "\nRègles de CLAUDE.md non vérifiées"
CHARTER_FILES = ("charter.toml", "charte.toml")


def find_upward(start: Path, relative: str) -> Path | None:
    for folder in [start, *start.parents]:
        if (folder / relative).exists():
            return folder / relative
    return None


def lint_command(path: Path) -> tuple[list[str], Path] | None:
    if path.suffix == ".py":
        ruff = find_upward(path.parent, ".venv/bin/ruff")
        if ruff:
            return (
                [str(ruff), "check", "--quiet", "--output-format", "concise", str(path)],
                ruff.parents[2],
            )
    if path.suffix in ESLINT_SUFFIXES:
        eslint = find_upward(path.parent, "node_modules/.bin/eslint")
        if eslint:
            project = eslint.parents[2]
            cache = str(project / "node_modules/.cache/eslint-hook")
            return ([str(eslint), "--cache", "--cache-location", cache, str(path)], project)
    return None


def charter_command(path: Path) -> tuple[list[str], Path] | None:
    if path.suffix not in CHARTER_SUFFIXES:
        return None
    top = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    if not top:
        return None
    if any((Path(top) / name).exists() for name in CHARTER_FILES):
        # `charter` comes with ion-repo (uv tool install kiln-cli) and checks the edited file only;
        # `charte`, its name before 0.4.0, only knows the whole repo.
        if engine := shutil.which("charter"):
            return ([engine, "file", str(path)], Path(top))
        engine = shutil.which("charte")
        return ([engine], Path(top)) if engine else None
    script = (
        os.environ.get("ION_REPO_CHARTER_SCRIPT")
        or os.environ.get("KILN_CHARTER_SCRIPT")
        or os.environ.get("PROJET_CHARTE")
    )
    if not script or not (Path(top) / script).exists():
        return None
    return ([sys.executable, str(Path(top) / script)], Path(top))


def failure_report(command: tuple[list[str], Path] | None) -> str:
    if not command:
        return ""
    argv, cwd = command
    completed = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=60)
    if completed.returncode == 0:
        return ""
    report = completed.stdout + completed.stderr
    if argv[1:2] == ["file"] and report.startswith("charter: checks a repo"):
        # A `charter` older than `charter file` prints its usage: the whole repo, then.
        return failure_report((argv[:1], cwd))
    if LEGACY_REPORT_END in report:
        report = report.split(LEGACY_REPORT_END)[0]
    return report.strip()


def is_new_charter_report(report: str, edited: Path) -> bool:
    """A violation already reported (ongoing debt) is not repeated at every edit.

    The signature ignores digits, which move with every line written; a new offending file or a
    new broken rule changes it, and the report comes back.
    """
    signature = "\n".join(
        sorted({"".join(c for c in line if not c.isdigit()) for line in report.splitlines()})
    )
    memo = (
        Path(tempfile.gettempdir())
        / f"charte-hook-{hashlib.sha1(str(edited).encode()).hexdigest()[:12]}"
    )
    previous = memo.read_text(encoding="utf-8") if memo.exists() else ""
    memo.write_text(signature, encoding="utf-8")
    return signature != previous


file_path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
if not file_path or "node_modules" in file_path or not os.path.isfile(file_path):
    sys.exit(0)
path = Path(file_path)
charter = charter_command(path)
charter_report = failure_report(charter)
if charter and not is_new_charter_report(charter_report, path.resolve()):
    charter_report = ""
reports = [report for report in (failure_report(lint_command(path)), charter_report) if report]
if reports:
    print(
        f"Check failed after editing {file_path}:\n\n" + "\n\n".join(reports),
        file=sys.stderr,
    )
    sys.exit(2)
