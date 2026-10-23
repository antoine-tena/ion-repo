"""Converters of `kiln fix`: the slimming pillar (T-139), the compressor's two phases."""

from kiln.grid.compressor import remove_dead_code, remove_unused_dependencies
from kiln.grid.fixers import Fixer, register

register(
    Fixer(
        "remove_dead_code",
        remove_dead_code,
        "dead code removed, each removal proven by the types and the tests",
        network=True,
    )
)
register(
    Fixer(
        "remove_unused_dependencies",
        remove_unused_dependencies,
        "unused dependencies removed, each removal proven by the types and the tests",
        network=True,
    )
)
