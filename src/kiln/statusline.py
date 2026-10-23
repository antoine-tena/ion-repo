"""Claude Code's status line: the style chosen for this machine and the repo's own settings.

The style (`kiln set statusline=…`, a machine key) is read by the `kiln` plugin's script at each
render; kiln touches the `statusLine` of `~/.claude/settings.json` only to set its script or to
remove it, never with `custom`. The repo's settings live in kiln's answers (`statusline_ci`,
`prod_health_url`), so the team shares them, and are set as `git config statusline.*` at each
`kiln install`, `kiln new` and `kiln set`.
"""

import json
from dataclasses import replace
from pathlib import Path

from kiln.config import (
    CUSTOM_STATUSLINE,
    DEFAULT_STATUSLINE,
    NO_STATUSLINE,
    STATUSLINE_STYLES,
    UserConfig,
    config_path,
    save_config,
)
from kiln.shell import KilnError, run
from kiln.stack import answers_if_any

SCRIPT = Path("plugins") / "kiln" / "scripts" / "statusline.py"
# Its path before kiln 0.4 (plugin `base`), still recognized.
LEGACY_SCRIPT = Path("plugins") / "base" / "scripts" / "statusline.py"
# Claude Code reruns the script only on its own events (a new message…): without a timer, the
# values refreshed in the background (git, CI, tasks) wait for the next one. A render costs
# about 0.15 s.
REFRESH_SECONDS = 5


def apply_statusline_settings(root: Path) -> None:
    answers = answers_if_any(root)
    show_ci = answers.get("statusline_ci", True) is not False
    # A CI run on the machine is read from its git note (`kiln ci`), not from GitHub.
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
    """The `kiln` plugin's script, where Claude Code put the kiln marketplace."""
    known = known_marketplaces()
    try:
        location = json.loads(known.read_text())["kiln"]["installLocation"]
    except (OSError, ValueError, KeyError) as error:
        raise KilnError(
            "kiln plugin marketplace missing: claude plugin marketplace add antoine-tena/kiln"
        ) from error
    script = Path(location) / SCRIPT
    if not script.exists():
        raise KilnError(f"status line script not found: {script}")
    return script


def is_kiln_statusline(entry: object) -> bool:
    command = str(entry.get("command", "")) if isinstance(entry, dict) else ""
    return any(script.as_posix() in command for script in (SCRIPT, LEGACY_SCRIPT))


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
        if is_kiln_statusline(current):
            if current.get("refreshInterval"):
                return f"kiln status line, {choice} style."
            current["refreshInterval"] = REFRESH_SECONDS
            message = f"kiln status line, {choice} style, refreshed every {REFRESH_SECONDS} s."
        else:
            settings["statusLine"] = {
                "type": "command",
                "command": f'python3 "{kiln_script()}"',
                "refreshInterval": REFRESH_SECONDS,
            }
            message = f"kiln status line, {choice} style, set in {path}{previous}."
    else:
        raise KilnError(f"unknown statusline: {choice}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    return message


def ensure_statusline(config: UserConfig) -> UserConfig:
    """At the first `kiln install`: the default style, or `custom` when the user already has a
    status line of their own; the choice is kept in the machine settings. Without kiln's plugins
    (no Claude Code yet), nothing: there is no script to point at."""
    if not known_marketplaces().exists():
        return config
    path = claude_settings_path()
    settings = json.loads(path.read_text()) if path.exists() else {}
    current = settings.get("statusLine")
    if config.statusline is not None:
        # a kiln status line set before its timer gets it
        if is_kiln_statusline(current) and not current.get("refreshInterval"):
            print(apply_statusline_choice(str(config.statusline)))
        return config
    own = current is not None and not is_kiln_statusline(current)
    updated = replace(config, statusline=CUSTOM_STATUSLINE if own else DEFAULT_STATUSLINE)
    print(apply_statusline_choice(str(updated.statusline)))
    save_config(updated)
    print(f"Choice saved in {config_path()} (change: kiln set statusline=…).")
    return updated
