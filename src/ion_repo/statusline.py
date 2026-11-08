"""Claude Code's status line: the style chosen for this machine and the repo's own settings.

The style (`ion repo set statusline=…`, a machine key) is read by the `ion-repo` plugin's script at
each render; ion-repo touches the `statusLine` of `~/.claude/settings.json` only to set its script
or to remove it, never with `custom`. The repo's settings live in ion-repo's answers
(`statusline_ci`, `prod_health_url`), so the team shares them, and are set as `git config
statusline.*` at each `ion repo install`, `ion repo new` and `ion repo set`.
"""

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, TypeGuard

from ion_repo.config import (
    CUSTOM_STATUSLINE,
    DEFAULT_PALETTE,
    DEFAULT_STATUSLINE,
    NO_STATUSLINE,
    STATUSLINE_PALETTES,
    STATUSLINE_STYLES,
    UserConfig,
    config_path,
    save_config,
)
from ion_repo.shell import KilnError, run
from ion_repo.stack import answers_if_any

SCRIPT = Path("plugins") / "repo" / "scripts" / "statusline.py"
# Its paths before: plugin `kiln` until ion-repo, `base` before kiln 0.4; still recognized.
LEGACY_SCRIPTS = (
    Path("plugins") / "kiln" / "scripts" / "statusline.py",
    Path("plugins") / "base" / "scripts" / "statusline.py",
)
# The catalogue's names in `known_marketplaces.json`: today's, then kiln's.
MARKETPLACES = ("ion-repo", "kiln")
# Claude Code reruns the script only on its own events (a new message…): without a timer, the
# values refreshed in the background (git, CI, tasks) wait for the next one. A render costs
# about 0.15 s.
REFRESH_SECONDS = 5
# The script needs ion-repo's Python (3.14): a bare `python3` is 3.9 or 3.13 on macOS, where it
# stops on a syntax error and the status line stays empty.
INTERPRETER = f'"{sys.executable}"'
BARE_PYTHON = "python3 "


def with_interpreter(command: str) -> str:
    """The command run by ion-repo's Python, not by whatever `python3` the PATH holds."""
    return (
        f"{INTERPRETER} {command.removeprefix(BARE_PYTHON)}"
        if command.startswith(BARE_PYTHON)
        else command
    )


def apply_statusline_settings(root: Path) -> None:
    answers = answers_if_any(root)
    show_ci = answers.get("statusline_ci", True) is not False
    # A CI run on the machine is read from its git note (`ion repo ci`), not from GitHub.
    local_ci = answers.get("ci_runner") == "local"
    value = ("locale" if local_ci else "true") if show_ci else "false"
    run(["git", "config", "statusline.ci", value], root)
    prod_url = str(answers.get("prod_health_url") or "")
    if prod_url:
        run(["git", "config", "statusline.prod-url", prod_url], root)


def claude_settings_path() -> Path:
    return Path.home() / ".claude" / "settings.json"


def known_marketplaces() -> Path:
    return Path.home() / ".claude" / "plugins" / "known_marketplaces.json"


def kiln_script() -> Path:
    """The `ion-repo` plugin's script, where Claude Code put the ion-repo marketplace."""
    known = known_marketplaces()
    try:
        catalogues = json.loads(known.read_text())
        name = next(name for name in MARKETPLACES if name in catalogues)
        location = catalogues[name]["installLocation"]
    except (OSError, ValueError, KeyError, StopIteration, TypeError) as error:
        raise KilnError(
            "ion-repo plugin marketplace missing: ion repo install --machine"
        ) from error
    script = Path(location) / SCRIPT
    if not script.exists():
        raise KilnError(f"status line script not found: {script}")
    return script


def is_kiln_statusline(entry: object) -> TypeGuard[dict[str, Any]]:
    command = str(entry.get("command", "")) if isinstance(entry, dict) else ""
    return any(script.as_posix() in command for script in (SCRIPT, *LEGACY_SCRIPTS))


def moved_command(command: str) -> str:
    """Its path before ion-repo (plugins/kiln/, plugins/base/) made today's, its interpreter
    ion-repo's; the rest kept."""
    for legacy in LEGACY_SCRIPTS:
        command = command.replace(legacy.as_posix(), SCRIPT.as_posix())
    return with_interpreter(command)


def is_stale_statusline(entry: object) -> bool:
    """An ion-repo status line whose command is no longer the one `moved_command` would write."""
    return is_kiln_statusline(entry) and entry.get("command") != moved_command(
        str(entry.get("command"))
    )


def apply_statusline_choice(choice: str, settings_path: Path | None = None) -> str:
    """Aligns Claude Code's `statusLine` with the choice; returns what was done."""
    path = settings_path or claude_settings_path()
    if choice == CUSTOM_STATUSLINE:
        return f"Claude Code's statusLine left as is ({CUSTOM_STATUSLINE})."
    settings = json.loads(path.read_text()) if path.exists() else {}
    current = settings.get("statusLine")
    previous = "" if current is None or is_kiln_statusline(current) else f" (replaces: {current})"
    if choice == NO_STATUSLINE:
        if current is None:
            return "No status line."
        del settings["statusLine"]
        message = f"statusLine removed from {path}{previous}."
    elif choice in STATUSLINE_STYLES:
        if is_kiln_statusline(current) and current.get("command") != (
            command := moved_command(str(current.get("command")))
        ):
            current["command"] = command
            current.setdefault("refreshInterval", REFRESH_SECONDS)
            message = f"ion-repo status line, {choice} style, moved to {command}."
        elif is_kiln_statusline(current):
            if current.get("refreshInterval"):
                return f"ion-repo status line, {choice} style."
            current["refreshInterval"] = REFRESH_SECONDS
            message = f"ion-repo status line, {choice} style, refreshed every {REFRESH_SECONDS} s."
        else:
            settings["statusLine"] = {
                "type": "command",
                "command": f'{INTERPRETER} "{kiln_script()}"',
                "refreshInterval": REFRESH_SECONDS,
            }
            message = f"ion-repo status line, {choice} style, set in {path}{previous}."
    else:
        raise KilnError(f"unknown statusline: {choice}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    return message


def ensure_statusline(config: UserConfig) -> UserConfig:
    """At the first `ion repo install`: the default style, or `custom` when the user already has a
    status line of their own; the choice is kept in the machine settings. Without ion-repo's plugins
    (no Claude Code yet), nothing: there is no script to point at."""
    if not known_marketplaces().exists():
        return config
    path = claude_settings_path()
    settings = json.loads(path.read_text()) if path.exists() else {}
    current = settings.get("statusLine")
    if config.statusline is not None:
        # an ion-repo status line set before its timer gets it
        if is_kiln_statusline(current) and (
            is_stale_statusline(current) or not current.get("refreshInterval")
        ):
            print(apply_statusline_choice(str(config.statusline)))
        return config
    own = current is not None and not is_kiln_statusline(current)
    updated = replace(config, statusline=CUSTOM_STATUSLINE if own else DEFAULT_STATUSLINE)
    print(apply_statusline_choice(str(updated.statusline)))
    save_config(updated)
    print(f"Choice saved in {config_path()} (change: ion repo set statusline=…).")
    return updated


def palette_levels() -> dict[str, dict[str, str]]:
    """Each palette's four levels (`--levels` of the script); empty when the script is out of
    reach."""
    try:
        done = subprocess.run(
            [sys.executable, str(kiln_script()), "--levels"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        levels = json.loads(done.stdout)
    except KilnError, OSError, ValueError, subprocess.SubprocessError:
        return {}
    return levels if isinstance(levels, dict) else {}


def swatch(color: str, text: str) -> str:
    """`text` after a square in `#rrggbb`, in the terminal's true colors."""
    red, green, blue = (int(color[i : i + 2], 16) for i in (1, 3, 5))
    return f"\033[38;2;{red};{green};{blue}m■\033[0m {text}"


def show_palettes(levels: dict[str, dict[str, str]]) -> None:
    """A palette by its colors, not its name: what each level of the status line looks like."""
    width = max(map(len, STATUSLINE_PALETTES))
    for name in STATUSLINE_PALETTES:
        colors = levels.get(name) or {}
        shown = "  ".join(swatch(color, level) for level, color in colors.items())
        print(f"  {name:<{width}}  {shown}")


def ask_palette() -> str:
    """Outside a terminal, the default: stone and fire."""
    if not sys.stdin.isatty():
        return DEFAULT_PALETTE
    levels = palette_levels()
    if levels:
        print("Status line colors, from all well to urgent:")
        show_palettes(levels)
    prompt = (
        f"Status line colors? {' / '.join(STATUSLINE_PALETTES)} "
        f"[Enter: {DEFAULT_PALETTE}, ion-repo's own]: "
    )
    answer = input(prompt).strip().lower()
    return answer if answer in STATUSLINE_PALETTES else DEFAULT_PALETTE


def ensure_palette(config: UserConfig) -> UserConfig:
    """Asked once, at the first `ion repo install` that sets an ion-repo status line, then kept in
    the machine settings; the script reads it at each render."""
    if config.statusline_palette or config.statusline not in STATUSLINE_STYLES:
        return config
    updated = replace(config, statusline_palette=ask_palette())
    save_config(updated)
    print(
        f"Palette {updated.statusline_palette} saved in {config_path()} "
        "(change: ion repo set statusline_palette=…)."
    )
    return updated
