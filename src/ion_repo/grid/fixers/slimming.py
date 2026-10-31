"""Converters of `kiln fix`: the slimming pillar (T-139), the compressor's two phases."""

from ion_repo.grid.compressor import remove_dead_code, remove_unused_dependencies
from ion_repo.grid.fixers import Fixer, register

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
