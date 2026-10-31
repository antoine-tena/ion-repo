"""`kiln set` outside a repo (or `kiln set --machine`): the settings of this machine.

They live in `~/.config/kiln/config.toml`: system, default GitHub owner and team of `kiln new`,
code directory of `kiln status` and `kiln update --all`, release channel, Claude Code's status
line, whether Claude's commits say Claude helped, the repos `kiln update --all` leaves alone.
Keys and values of before kiln 0.4.0 (`canal=interne`) are still accepted.
"""

from dataclasses import replace
from pathlib import Path

from ion_repo import renames, ui
from ion_repo.config import (
    BETA_CHANNEL,
    CHANNELS,
    DEFAULT_STATUSLINE,
    DISCLOSE_TRAILERS,
    STATUSLINE_CHOICES,
    SYSTEMS,
    TRAILER_CHOICES,
    UserConfig,
    config_path,
    load_config,
    save_config,
)
from ion_repo.shell import KilnError
from ion_repo.statusline import apply_statusline_choice
from ion_repo.trailers import apply_trailers_choice
from ion_repo.versions import beta_install_command

MACHINE_KEYS = (
    "system",
    "owner",
    "team",
    "code_dir",
    "channel",
    "statusline",
    "ai_trailers",
    "frozen_repos",
)


def show_machine(config: UserConfig) -> None:
    statusline = config.statusline or DEFAULT_STATUSLINE
    values = {
        "system": config.system or "(asked at the first kiln install)",
        "owner": config.owner or "(none)",
        "team": ", ".join(config.team) or "(none)",
        "code_dir": str(config.code_dir),
        "channel": (
            f"{config.channel} (public: promoted releases; internal: candidates too; "
            "beta: kiln's develop, live)"
        ),
        "statusline": f"{statusline} ({' / '.join(STATUSLINE_CHOICES)})",
        "ai_trailers": (
            f"{config.ai_trailers or DISCLOSE_TRAILERS} (disclose: Claude's commits and pull "
            "requests say Claude helped; never: they don't)"
        ),
        "frozen_repos": (
            f"{', '.join(config.frozen_repos) or '(none)'} (left alone by kiln update --all)"
        ),
    }
    width = max(len(key) for key in MACHINE_KEYS)
    print(ui.paint(f"Machine settings ({config_path()})", bold=True))
    for key in MACHINE_KEYS:
        print(f"{ui.paint(f'{key:<{width}}', ui.STONE)}  {values[key]}")
    print()
    ui.note("Change: kiln set key=value [key=value…] (e.g. kiln set team=alice,bob).")
    ui.note("A repo's settings: go into the repo, then kiln set.")


def only_machine_keys(assignments: list[str]) -> bool:
    """Keys that only exist for the machine (`statusline=…`, `channel=…`): `kiln set` in a repo
    applies them to the machine rather than refusing them."""
    from ion_repo.settings import SETTABLE_KEYS

    keys = [renames.MACHINE_KEYS.get(k, k) for k, _, _ in (a.partition("=") for a in assignments)]
    return bool(keys) and all(k in MACHINE_KEYS and k not in SETTABLE_KEYS for k in keys)


def apply_machine(config: UserConfig, assignments: list[str]) -> UserConfig:
    """The new machine settings, once each `key=value` is checked."""
    updated = config
    for assignment in assignments:
        old_key, separator, value = assignment.partition("=")
        key = renames.MACHINE_KEYS.get(old_key, old_key)
        value = renames.machine_value(key, value.strip())
        if not separator or key not in MACHINE_KEYS:
            raise KilnError(
                f'"{assignment}": expected key=value, machine keys: {", ".join(MACHINE_KEYS)}'
            )
        if key == "system":
            if value not in SYSTEMS:
                raise KilnError(f"system: {', '.join(SYSTEMS)}")
            updated = replace(updated, system=value)
        elif key == "owner":
            updated = replace(updated, owner=value or None)
        elif key == "team":
            updated = replace(updated, team=_listed(value))
        elif key == "frozen_repos":
            updated = replace(updated, frozen_repos=_listed(value))
        elif key == "channel":
            if value not in CHANNELS:
                raise KilnError(f"channel: {', '.join(CHANNELS)}")
            updated = replace(updated, channel=value)
        elif key == "statusline":
            if value not in STATUSLINE_CHOICES:
                raise KilnError(f"statusline: {', '.join(STATUSLINE_CHOICES)}")
            updated = replace(updated, statusline=value)
        elif key == "ai_trailers":
            if value not in TRAILER_CHOICES:
                raise KilnError(f"ai_trailers: {', '.join(TRAILER_CHOICES)}")
            updated = replace(updated, ai_trailers=value)
        else:
            updated = replace(updated, code_dir=Path(value).expanduser())
    return updated


def _listed(value: str) -> tuple[str, ...]:
    """`alice,bob` or `[alice, bob]` as a list; empty clears it."""
    return tuple(item.strip() for item in value.strip("[]").split(",") if item.strip())


def run_machine(assignments: list[str]) -> None:
    config = load_config()
    if assignments:
        previous = config
        config = apply_machine(config, assignments)
        save_config(config)
        if config.statusline and config.statusline != previous.statusline:
            ui.note(apply_statusline_choice(config.statusline))
        if config.ai_trailers and config.ai_trailers != previous.ai_trailers:
            ui.note(apply_trailers_choice(config.ai_trailers))
        if config.channel == BETA_CHANNEL != previous.channel:
            command = beta_install_command(config.code_dir)
            ui.note(f"Beta channel: make the tool kiln's develop now: {command}")
    show_machine(config)
