"""What `kiln dev` asks in a terminal: what to run, then whether to follow the logs.

A small project (one or two processes) runs everything without a question. From three on (a
backend, a front, a worker…), a menu offers everything, the last choice, or a choice process by
process, remembered for the next time. Outside a terminal (a script, a Claude session), nothing
is asked: everything runs, or what `--only` names.
"""

import json
import sys
from collections.abc import Callable
from pathlib import Path

from kiln import ui
from kiln.shell import KilnError
from kiln.stack import Command

# From this many processes on, kiln asks what to run.
MENU_THRESHOLD = 3
# Not a `.json`: the background takes those for the records of its processes.
SELECTION_FILE = "last-selection"

type Ask = Callable[[str], str]


def is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def select(
    commands: list[Command],
    state: Path,
    only: list[str] | None = None,
    ask: Ask | None = None,
) -> list[Command]:
    """The processes to run: `--only`, else the menu in a terminal, else all of them."""
    labels = [command.label for command in commands]
    if only is not None:
        unknown = [label for label in only if label not in labels]
        if unknown:
            raise KilnError(f"no {', '.join(unknown)} here (known: {', '.join(labels)})")
        chosen = only
    elif ask is None or len(commands) < MENU_THRESHOLD:
        return commands
    else:
        chosen = _ask_selection(labels, _last_selection(state, labels), ask)
    state.mkdir(parents=True, exist_ok=True)
    (state / SELECTION_FILE).write_text(json.dumps(chosen), encoding="utf-8")
    return [command for command in commands if command.label in chosen]


def _last_selection(state: Path, labels: list[str]) -> list[str] | None:
    try:
        last = json.loads((state / SELECTION_FILE).read_text(encoding="utf-8"))
    except OSError, ValueError:
        return None
    kept = [label for label in last if label in labels] if isinstance(last, list) else []
    return kept if kept and kept != labels else None


def _ask_selection(labels: list[str], last: list[str] | None, ask: Ask) -> list[str]:
    options = [("everything", labels)]
    if last:
        options.insert(0, ("as last time", last))
    print(f"\n{ui.paint('What should run?', bold=True)}")
    for number, (name, chosen) in enumerate(options, start=1):
        print(f"  {ui.paint(str(number), ui.FIRE)}  {name}: {', '.join(chosen)}")
    print(f"  {ui.paint(str(len(options) + 1), ui.FIRE)}  choose")
    while True:
        reply = ask("Choice [1]: ").strip()
        if not reply:
            return options[0][1]
        if reply.isdigit() and 1 <= int(reply) <= len(options):
            return options[int(reply) - 1][1]
        if reply == str(len(options) + 1):
            return _ask_each(labels, last or labels, ask)
        print(f"A number from 1 to {len(options) + 1}.")


def _ask_each(labels: list[str], default: list[str], ask: Ask) -> list[str]:
    for number, label in enumerate(labels, start=1):
        print(f"  {ui.paint(str(number), ui.FIRE)}  {label}")
    numbers = " ".join(str(labels.index(label) + 1) for label in default)
    while True:
        reply = ask(f"Numbers, separated by spaces [{numbers}]: ").strip()
        if not reply:
            return default
        picked = reply.replace(",", " ").split()
        if picked and all(part.isdigit() and 1 <= int(part) <= len(labels) for part in picked):
            return [label for number, label in enumerate(labels, start=1) if str(number) in picked]
        print(f"Numbers from 1 to {len(labels)}, such as: {numbers}.")


def wants_logs(ask: Ask) -> bool:
    reply = ask("Follow the logs? (Ctrl+C leaves them, the servers keep running) [Y/n] ")
    return reply.strip().lower() in ("", "y", "yes", "o", "oui")
