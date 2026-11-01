"""`kiln`: the old name of `ion-repo`, said on every run, then the command itself."""

import sys

from ion_repo import cli

NOTICE = (
    "kiln is now ion-repo, in the Ion family: type `ion-repo …`, or `ion repo …` once "
    "`uv tool install ion-sh` has brought the `ion` command. `kiln` stays an alias for a while."
)


def main() -> None:
    # On stderr: what a script reads of stdout (`kiln frame`, `--version`) stays the same.
    print(f"kiln: {NOTICE}", file=sys.stderr)
    cli.main()
