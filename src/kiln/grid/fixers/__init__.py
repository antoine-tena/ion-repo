"""The converters of `kiln fix`, by name: what a script can close, closed by script.

A rule names its fixer (`fixer = "…"`); an empty name means only judgment closes the gap
(Claude, through the roadmap). A converter edits the files of the repo in place and returns the
paths it changed; it never commits, `kiln fix` does, one commit per rule. `network` says it
reaches the internet (a commit SHA or an image digest to resolve), told before it starts.
"""

from collections.abc import Callable
from dataclasses import dataclass

from kiln.grid.facts import Repo


@dataclass(frozen=True)
class Fixer:
    name: str
    convert: Callable[[Repo], list[str]]
    summary: str  # the commit subject, after `fix(<RULE>): `
    network: bool = False


FIXERS: dict[str, Fixer] = {}


def register(fixer: Fixer) -> None:
    FIXERS[fixer.name] = fixer


# Each module registers its converters on import.
from kiln.grid.fixers import ci, containers, python  # noqa: E402, F401
