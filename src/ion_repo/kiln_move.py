"""The last `kiln-cli` moves its tester to the Ion family, at its first run on the machine.

Only a uv tool named `kiln-cli` moves: `uvx`, Homebrew and a checkout are left alone, and so is
`charter`, which git hooks call. Standard library only, and every report on stderr: the code under
it is uninstalled while it runs, and a script keeps reading the command's stdout.

The order is what uv's behaviour imposes (uv 0.12, reproduced from a real 0.4.10):
- `uv tool install ion-repo` refuses while `kiln-cli` owns the same commands, hence `--force`;
- `uv tool uninstall kiln-cli` then removes those commands, though they now point to `ion-repo`,
  hence a second `--force`, which brings them back;
- a package's dependency brings no command to a uv tool, hence `ion-sh` as a tool of its own.

A failure before the uninstall leaves the tool working: the command runs, the way to finish is
said, and the next run tries again a day later at the earliest.
"""

import fcntl
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path

LEGACY_TOOL = "kiln-cli"
TOOL = "ion-repo"
FAMILY = "ion-sh"
# Left by `uv tool install` in the tool's environment; `uvx` leaves none.
RECEIPT = "uv-receipt.toml"
OPT_OUT_VARIABLE = "ION_REPO_NO_UPDATE_CHECK"
RETRY_DELAY = 24 * 3600
STEP_TIMEOUT = 600
STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / "kiln"
ATTEMPT_FILE = STATE_DIR / "move-to-ion"
LOCK_FILE = STATE_DIR / "move-to-ion.lock"
MANUAL = (
    f"uv tool install {FAMILY} && uv tool install --force {TOOL} && "
    f"uv tool uninstall {LEGACY_TOOL} && uv tool install --force {TOOL} && "
    f"{TOOL} install --machine"
)


def say(message: str) -> None:
    print(f"kiln: {message}", file=sys.stderr)


def in_legacy_tool() -> bool:
    prefix = Path(sys.prefix)
    return prefix.name == LEGACY_TOOL and (prefix / RECEIPT).is_file()


def is_due(now: float) -> bool:
    if os.environ.get(OPT_OUT_VARIABLE):
        return False
    try:
        return now - ATTEMPT_FILE.stat().st_mtime >= RETRY_DELAY
    except OSError:
        return True


def step(command: Sequence[str]) -> bool:
    """Runs a step quietly, its output kept for a failure; True when it worked."""
    try:
        done = subprocess.run(
            command,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=STEP_TIMEOUT,
            check=False,
        )
    except OSError, subprocess.TimeoutExpired:
        say(f"`{' '.join(command)}` did not finish.")
        return False
    if done.returncode != 0:
        say(f"`{' '.join(command)}` failed: {done.stderr.strip()[-400:]}")
    return done.returncode == 0


def move_tools() -> bool:
    """`ion-sh` and `ion-repo` in place of `kiln-cli`. The interpreter's version is given because
    it is known to work here; uv would otherwise try the machine's default Python first."""
    python = ["--python", f"{sys.version_info.major}.{sys.version_info.minor}"]
    install = ["uv", "tool", "install", *python]
    return (
        step([*install, FAMILY])
        and step([*install, "--force", TOOL])
        and step(["uv", "tool", "uninstall", LEGACY_TOOL])
        and step([*install, "--force", TOOL])
    )


def hand_over() -> None:
    """The new tool replaces this process, whose own files are gone by now."""
    try:
        os.execvp(TOOL, [TOOL, *sys.argv[1:]])
    except OSError:
        say(f"`{TOOL}` is not on the PATH: open a new terminal, or run `uv tool update-shell`.")
        sys.exit(1)


def run() -> None:
    """Moves this machine if it is due; returns only when the old tool is to carry on."""
    if not in_legacy_tool():
        return
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        lock = LOCK_FILE.open("w")
        # Two sessions opening at once: the second waits, then finds the first one's work.
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not Path(sys.prefix, RECEIPT).is_file():
            hand_over()
        now = time.time()
        if not is_due(now):
            say(f"kiln-cli is no longer updated, move to Ion: {MANUAL}")
            return
        ATTEMPT_FILE.touch()
    except OSError as error:
        say(f"cannot move to Ion ({error}): {MANUAL}")
        return
    say("kiln is now ion-repo, in the Ion family: moving this machine, once.")
    if not move_tools():
        if Path(sys.prefix, RECEIPT).is_file():
            say(f"staying on kiln-cli for now. To finish by hand: {MANUAL}")
            return
        say(f"kiln-cli is gone but ion-repo is incomplete. To finish: {MANUAL}")
        sys.exit(1)
    # The plugin moves with the new tool's code, and its failure costs no command.
    if shutil.which("claude") is not None and not step([TOOL, "install", "--machine"]):
        say(f"the Claude Code plugin did not move: {TOOL} install --machine")
    say("done: type `ion repo …`. In Claude Code: /reload-plugins, then the skills are /repo:… .")
    hand_over()
