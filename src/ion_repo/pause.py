"""`ion repo pause`: a Claude Code session named and its place kept, listed at the next start
(ion-repo#T-344).

Claude Code already names a session (`/rename`) and resumes it (`claude --resume`); what it lacks
is the list, at the next start in any repo, of the sessions left halfway with where each stopped
and its next step. One file per session in `~/.local/state/kiln/sessions/<id>.json`, which the
plugin's `session_start.py` reads; it drops a session once resumed or its branch deleted.
"""

import datetime
import json
import os
import re
import subprocess
from pathlib import Path

from ion_repo import ui
from ion_repo.shell import KilnError

STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
SESSIONS_DIR = STATE_DIR / "kiln" / "sessions"
# What Claude Code gives the commands a session runs: the id `claude --resume` takes.
SESSION_VARIABLE = "CLAUDE_CODE_SESSION_ID"


# Branches whose name says nothing of the work.
SHARED_BRANCHES = {"main", "master", "develop", "trunk"}
BACKLOG_FILE = Path("docs") / "backlog" / "backlog.md"
TICKET_HEADING = re.compile(r"^### ((?:[a-z][a-z0-9-]*#)?T-\d+) · (.+?)(?:\.\.\.)?$")


def pause(cwd: Path, name: str, next_step: str) -> Path | None:
    session = os.environ.get(SESSION_VARIABLE, "")
    if not name:
        propose_names(cwd, inside=bool(session))
        return None
    if not session or "/" in session:
        raise KilnError(
            'no Claude Code session here: /repo:pause, or `! ion repo pause "<name>"`, from inside '
            "one"
        )
    root = Path(_git(cwd, "rev-parse", "--show-toplevel") or cwd)
    # The project's name, not a worktree's folder: the parent of the shared git folder.
    common = _git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
    record = {
        "id": session,
        "name": name,
        "project": Path(common).parent.name if common else root.name,
        "repo": str(root),
        "branch": _git(cwd, "branch", "--show-current"),
        "next": next_step,
        "paused": datetime.datetime.now().astimezone().isoformat(timespec="minutes"),
    }
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = SESSIONS_DIR / f"{session}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.success(f"Paused: {name}")
    ui.note(f"Listed at the next session start; resume with: claude --resume {session}")
    return path


def propose_names(cwd: Path, *, inside: bool) -> None:
    """Names drawn from the work at hand, each with the command that pauses under it."""
    names = suggested_names(cwd)
    ui.step("A name for this session")
    prefix = "ion repo pause" if inside else "! ion repo pause"
    for suggestion in names or ["<what this session works on>"]:
        ui.note(f'{prefix} "{suggestion}" --next "<the next step>"')
    if not inside:
        ui.note("From inside a Claude Code session: /repo:pause, or one of these after `!`.")


def suggested_names(cwd: Path) -> list[str]:
    """The current branch made readable, the backlog's tickets in progress, the last commit."""
    names: list[str] = []
    branch = _git(cwd, "branch", "--show-current")
    if branch and branch not in SHARED_BRANCHES:
        names.append(re.sub(r"[-_/]+", " ", branch.split("/", 1)[-1]).strip())
    root = Path(_git(cwd, "rev-parse", "--show-toplevel") or cwd)
    names += _tickets_in_progress(root / BACKLOG_FILE)
    subject = _git(cwd, "log", "-1", "--no-merges", "--format=%s")
    if subject:
        names.append(subject)
    return list(dict.fromkeys(name for name in names if name))[:5]


def _tickets_in_progress(backlog: Path) -> list[str]:
    if not backlog.is_file():
        return []
    found, ticket = [], ""
    for line in backlog.read_text(encoding="utf-8").splitlines():
        if heading := TICKET_HEADING.match(line):
            ticket = f"{heading[1]}: {heading[2]}"
        elif ticket and line.startswith("- **Status**: in progress"):
            found.append(ticket)
            ticket = ""
    return found


def _git(cwd: Path, *arguments: str) -> str:
    done = subprocess.run(["git", *arguments], cwd=cwd, capture_output=True, text=True, check=False)
    return done.stdout.strip() if done.returncode == 0 else ""
