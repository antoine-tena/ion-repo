"""`charter.toml`: where it is, and its content under today's names.

A repo adopted before kiln 0.4.0 still has a `charte.toml` with French names (`[cliquets.*]`,
`fichiers`, `taille-fichier`…): it is read as is, its names translated on the fly, so that such a
repo keeps working without being converted.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from kiln.renames import CHARTER_KEYS, CHARTER_RULES, CHARTER_SECTIONS

CHARTER_FILE = "charter.toml"
LEGACY_CHARTER_FILE = "charte.toml"
RULE_SECTIONS = ("bans", "ratchets", "floors")


def charter_path(root: Path) -> Path | None:
    """The repo's `charter.toml`, or its `charte.toml` of before 0.4.0; None if it has neither."""
    for name in (CHARTER_FILE, LEGACY_CHARTER_FILE):
        if (root / name).is_file():
            return root / name
    return None


def load(root: Path) -> dict[str, Any]:
    """The charter of the repo, under today's names; empty if it has none."""
    path = charter_path(root)
    if path is None:
        return {}
    return normalize(tomllib.loads(path.read_text("utf-8")))


def normalize(config: dict[str, Any]) -> dict[str, Any]:
    """A charter written with the names of kiln 0.3, under the names of today."""
    normalized: dict[str, Any] = {}
    for key, value in config.items():
        name = CHARTER_SECTIONS.get(key, CHARTER_KEYS.get(key, key))
        if name in RULE_SECTIONS and isinstance(value, dict):
            normalized[name] = {
                CHARTER_RULES.get(rule, rule): _rule_params(params)
                for rule, params in value.items()
            }
        elif isinstance(value, dict):
            normalized[name] = _keys(value)
        else:
            normalized[name] = value
    return normalized


def _rule_params(params: dict[str, Any]) -> dict[str, Any]:
    renamed = _keys(params)
    if "rule" in renamed:
        renamed["rule"] = CHARTER_RULES.get(renamed["rule"], renamed["rule"])
    return renamed


def _keys(values: dict[str, Any]) -> dict[str, Any]:
    return {CHARTER_KEYS.get(key, key): value for key, value in values.items()}
