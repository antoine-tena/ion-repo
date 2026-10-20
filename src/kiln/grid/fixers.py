"""The converters of `kiln fix`, by name: what a script can close, closed by script.

A rule names its fixer (`fixer = "…"`); an empty name means only judgment closes the gap
(Claude, through the roadmap). Filled by `kiln fix` (T-126 and the converters that follow)."""

from collections.abc import Callable
from pathlib import Path

FIXERS: dict[str, Callable[[Path], list[str]]] = {}
