"""`ion-repo frame`: the two rules that frame an Ion tool's skill answer, at the terminal's width.

The tool is named by its word (`learn`), whatever its plugin is called: `ion-learn`, or its name
before the Ion family (`grog`). Claude's Bash has no terminal (COLUMNS empty, `tput cols` says 80),
but the terminal is still there, held by an ancestor: the shell's parents are walked up to the
first whose standard input is a terminal, whose size is then read. Without one (a cloud session),
80 columns.
"""

import os
import subprocess
from collections.abc import Iterator
from pathlib import Path

FALLBACK_COLUMNS = 80
# What Claude Code takes from the line: the answer's bullet and the code block's padding.
MARGIN = 6
RULE = "═"
MIN_FILL = 3
PROC = Path("/proc")
FAMILY = "ion"
# A tool's repo, package and command are `ion-<word>`; its plugin is the word alone.
TOOL_PREFIX = "ion-"
# The tools' names before the Ion family (Keramos, until 31 October 2026), and the family's.
FORMER_NAMES = {
    "kiln": "repo",
    "slake": "render",
    "cone": "score",
    "grog": "learn",
    "seal": "deal",
    "hearth": "host",
    "saggar": "secure",
    "glaze": "design",
    "wedge": "media",
    "stylus": "words",
    "raku": "launch",
    "keramos": "ion",
}


def frame(tool: str, skill: str, width: int | None = None) -> None:
    for line in rules(tool, skill, width or terminal_columns() - MARGIN):
        print(line)


def tool_word(plugin: str) -> str:
    """The word of a tool, from its plugin's name: `ion-learn`, `grog` and `learn` give `learn`."""
    word = plugin.removeprefix(TOOL_PREFIX)
    return FORMER_NAMES.get(word, word)


def rules(tool: str, skill: str, width: int) -> tuple[str, str]:
    word = tool_word(tool)
    head = f"{RULE * 2} ◆ {FAMILY} · {word} "
    foot = f" /{word}:{skill} {RULE * 2}"
    return (
        head + RULE * max(MIN_FILL, width - len(head)),
        RULE * max(MIN_FILL, width - len(foot)) + foot,
    )


def terminal_columns() -> int:
    for device in _ancestor_terminals():
        try:
            descriptor = os.open(device, os.O_RDONLY | os.O_NOCTTY)
        except OSError:
            continue
        try:
            return os.get_terminal_size(descriptor).columns
        except OSError:
            continue
        finally:
            os.close(descriptor)
    return FALLBACK_COLUMNS


def _ancestor_terminals() -> Iterator[str]:
    """The terminal of this process or its nearest ancestor that has one, first."""
    walk = _proc_ancestors if PROC.is_dir() else _ps_ancestors
    yield from walk(os.getpid())


def _proc_ancestors(pid: int) -> Iterator[str]:
    seen: set[int] = set()
    while pid > 1 and pid not in seen:
        seen.add(pid)
        try:
            standard_input = os.readlink(PROC / str(pid) / "fd" / "0")
            # The command name, in parentheses, may hold spaces: the fields follow the last one.
            fields = (PROC / str(pid) / "stat").read_text().rpartition(")")[2].split()
        except OSError:
            return
        if standard_input.startswith(("/dev/pts/", "/dev/tty")):
            yield standard_input
        pid = int(fields[1])


def _ps_ancestors(pid: int) -> Iterator[str]:
    """macOS and the BSDs, without /proc: `ps` gives each process's parent and terminal."""
    seen: set[int] = set()
    while pid > 1 and pid not in seen:
        seen.add(pid)
        try:
            shown = subprocess.run(
                ["ps", "-o", "ppid=,tty=", "-p", str(pid)],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.split()
        except OSError:
            return
        if len(shown) != 2:  # its parent and its terminal
            return
        parent, terminal = shown
        if terminal not in ("?", "??", "-"):
            yield terminal if terminal.startswith("/") else f"/dev/{terminal}"
        pid = int(parent)
