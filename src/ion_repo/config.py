"""kiln's settings for this machine: `~/.config/kiln/config.toml`.

The system (Linux, WSL, macOS) is asked once, at the first install; the GitHub owner, the team
and the code directory give their defaults to `ion repo new` and `ion repo update --all`. Keys and
values written before kiln 0.4.0 (`canal = "interne"`, `statusline = "sobre"`) are still read.
"""

import os
import platform
import sys
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from ion_repo import renames

CONFIG_DIR_VARIABLE = "XDG_CONFIG_HOME"
CONFIG_RELATIVE_PATH = Path("kiln") / "config.toml"
DEFAULT_CODE_DIR = Path.home() / "code"

SYSTEMS = ("linux", "wsl", "macos")
# Release channel: `public` (promoted releases), `internal` (candidates included) or `beta`
# (the tool runs ion-repo's `develop`, read live from the checkout of the code directory).
PUBLIC_CHANNEL, INTERNAL_CHANNEL, BETA_CHANNEL = "public", "internal", "beta"
CHANNELS = (PUBLIC_CHANNEL, INTERNAL_CHANNEL, BETA_CHANNEL)
# Claude Code's status line: an ion-repo style, none, or the user's own (`custom`).
STATUSLINE_STYLES = ("plain", "band", "classic", "classic-band")
NO_STATUSLINE, CUSTOM_STATUSLINE = "none", "custom"
STATUSLINE_CHOICES = (*STATUSLINE_STYLES, NO_STATUSLINE, CUSTOM_STATUSLINE)
DEFAULT_STATUSLINE = "plain"
# Whether Claude's commits and pull requests say Claude helped (`Co-Authored-By: Claude`):
# disclosed by default, as the AI policies of several large open-source projects ask.
DISCLOSE_TRAILERS, NO_TRAILERS = "disclose", "never"
TRAILER_CHOICES = (DISCLOSE_TRAILERS, NO_TRAILERS)
SYSTEM_LABELS = {"linux": "Linux", "wsl": "Windows (WSL)", "macos": "macOS"}


@dataclass(frozen=True)
class UserConfig:
    system: str | None = None
    owner: str | None = None
    team: tuple[str, ...] = ()
    code_dir: Path = DEFAULT_CODE_DIR
    channel: str = PUBLIC_CHANNEL
    statusline: str | None = None  # None: not chosen yet (ion repo install sets it)
    ai_trailers: str | None = None  # None: not chosen yet (ion repo install asks)
    # Repos of the code folder `ion repo update --all` leaves as they are (a witness repo kept at an
    # old release on purpose), by their path in it.
    frozen_repos: tuple[str, ...] = ()


def config_path() -> Path:
    base_dir = os.environ.get(CONFIG_DIR_VARIABLE)
    return (Path(base_dir) if base_dir else Path.home() / ".config") / CONFIG_RELATIVE_PATH


def load_config() -> UserConfig:
    path = config_path()
    if not path.exists():
        return UserConfig()
    values = machine_settings(tomllib.loads(path.read_text()))
    team = values.get("team", [])
    statusline = values.get("statusline")
    frozen = values.get("frozen_repos", [])
    return UserConfig(
        system=values.get("system"),
        owner=values.get("owner"),
        team=tuple(str(login) for login in team) if isinstance(team, list) else (),
        code_dir=Path(values.get("code_dir", str(DEFAULT_CODE_DIR))).expanduser(),
        channel=renames.machine_value("channel", str(values.get("channel", PUBLIC_CHANNEL))),
        statusline=renames.machine_value("statusline", str(statusline)) if statusline else None,
        ai_trailers=values.get("ai_trailers"),
        frozen_repos=tuple(str(repo) for repo in frozen) if isinstance(frozen, list) else (),
    )


def machine_settings(values: dict[str, Any]) -> dict[str, Any]:
    """Settings under today's keys; a current key wins over its old name."""
    renamed = {renames.MACHINE_KEYS.get(key, key): value for key, value in values.items()}
    renamed.update({key: value for key, value in values.items() if key not in renames.MACHINE_KEYS})
    return renamed


def save_config(config: UserConfig) -> None:
    lines = ["# ion-repo's settings for this machine (created by ion repo install)."]
    if config.system:
        lines.append(f'system = "{config.system}"')
    if config.owner:
        lines.append(f'owner = "{config.owner}"')
    if config.team:
        lines.append("team = [" + ", ".join(f'"{login}"' for login in config.team) + "]")
    lines.append(f'code_dir = "{config.code_dir}"')
    if config.channel != PUBLIC_CHANNEL:
        lines.append(f'channel = "{config.channel}"')
    if config.statusline:
        lines.append(f'statusline = "{config.statusline}"')
    if config.ai_trailers:
        lines.append(f'ai_trailers = "{config.ai_trailers}"')
    if config.frozen_repos:
        lines.append("frozen_repos = [" + ", ".join(f'"{r}"' for r in config.frozen_repos) + "]")
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def detect_system() -> str:
    if platform.system() == "Darwin":
        return "macos"
    proc_version = Path("/proc/version")
    if proc_version.exists() and "microsoft" in proc_version.read_text().lower():
        return "wsl"
    return "linux"


def ask_system(detected: str) -> str:
    """Asks for the system, the detected one by default; outside a terminal, keeps it."""
    if not sys.stdin.isatty():
        return detected
    choices = " / ".join(f"{key} ({SYSTEM_LABELS[key]})" for key in SYSTEMS)
    answer = input(f"System of this machine? {choices} [{detected}]: ").strip().lower()
    return answer if answer in SYSTEMS else detected


def ensure_system(config: UserConfig) -> UserConfig:
    """The machine's system, asked once then kept in the settings."""
    if config.system in SYSTEMS:
        return config
    updated = replace(config, system=ask_system(detect_system()))
    save_config(updated)
    print(f"System saved in {config_path()}: {updated.system}.")
    return updated
