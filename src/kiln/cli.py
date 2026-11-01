"""`kiln`: the old name of `ion-repo`, said once on a machine, then the command itself."""

import sys

from ion_repo import cli, kiln_move

NOTICE = (
    "kiln is now ion-repo, in the Ion family: type `ion-repo …`, or `ion repo …` once "
    "`uv tool install ion-sh` has brought the `ion` command. `kiln` stays an alias for a while."
)
SAID_FILE = "alias-notice"


def say_notice_once() -> None:
    said = kiln_move.STATE_DIR / SAID_FILE
    if said.exists():
        return
    # On stderr: what a script reads of stdout (`kiln frame`, `--version`) stays the same.
    print(f"kiln: {NOTICE}", file=sys.stderr)
    try:
        said.parent.mkdir(parents=True, exist_ok=True)
        said.touch()
    except OSError:
        pass


def main() -> None:
    say_notice_once()
    cli.main()
