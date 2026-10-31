"""Whether Claude's commits and pull requests say Claude helped: a choice of each machine.

`kiln set ai_trailers=disclose|never` (asked at the first `kiln install`, "choose for me"
meaning disclose). `never` empties the `attribution` of `~/.claude/settings.json`, so Claude Code
writes no `Co-Authored-By: Claude`, and kiln's branch guard refuses one; `disclose` leaves
Claude Code's default. `Claude-Session:` is refused either way: a link nobody else can open.
"""

import json
import sys
from dataclasses import replace
from pathlib import Path

from ion_repo.config import (
    DISCLOSE_TRAILERS,
    NO_TRAILERS,
    TRAILER_CHOICES,
    UserConfig,
    config_path,
    save_config,
)
from ion_repo.shell import KilnError
from ion_repo.statusline import claude_settings_path

NO_ATTRIBUTION = {"commit": "", "pr": ""}


def apply_trailers_choice(choice: str, settings_path: Path | None = None) -> str:
    """Aligns Claude Code's `attribution` with the choice; returns what was done."""
    if choice not in TRAILER_CHOICES:
        raise KilnError(f"unknown ai_trailers: {choice}")
    path = settings_path or claude_settings_path()
    settings = json.loads(path.read_text()) if path.exists() else {}
    if choice == NO_TRAILERS:
        if settings.get("attribution") == NO_ATTRIBUTION:
            return "Claude's commits and pull requests don't say Claude helped."
        settings["attribution"] = dict(NO_ATTRIBUTION)
        message = f"attribution emptied in {path}: no Co-Authored-By: Claude."
    else:
        # Only kiln's own value goes: an attribution the user wrote stays.
        if settings.get("attribution") != NO_ATTRIBUTION:
            return "Claude's commits and pull requests say Claude helped."
        del settings["attribution"]
        message = f"attribution back to Claude Code's default in {path}: Co-Authored-By: Claude."
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    return message


def ask_trailers() -> str:
    """Outside a terminal, the default: disclose."""
    if not sys.stdin.isatty():
        return DISCLOSE_TRAILERS
    prompt = (
        "Should Claude's commits and pull requests say Claude helped (Co-Authored-By: Claude)? "
        "disclose / never [Enter: choose for me, disclose]: "
    )
    answer = input(prompt).strip().lower()
    return answer if answer in TRAILER_CHOICES else DISCLOSE_TRAILERS


def ensure_trailers(config: UserConfig) -> UserConfig:
    """Asked once, at the first `kiln install`, then kept in the machine settings."""
    if config.ai_trailers in TRAILER_CHOICES:
        return config
    updated = replace(config, ai_trailers=ask_trailers())
    print(apply_trailers_choice(str(updated.ai_trailers)))
    save_config(updated)
    print(f"Choice saved in {config_path()} (change: kiln set ai_trailers=…).")
    return updated
