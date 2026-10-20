# The shell of the README's recorded demos (`docs/assets/*.tape`), sourced by each tape before
# it shows anything. Replay a demo from kiln's root: `vhs docs/assets/kiln-new.tape` (needs vhs,
# ttyd and ffmpeg). kiln runs from this checkout (`KILN_TEMPLATE`), in a fresh folder that the
# banner calls `~/code`, without a version number that would date the recording, as
# `scripts/screenshots.py` does for the still images. The folder is on disk, not in `/tmp`
# (often held in memory), as a generated app weighs about 500 MB: the tape deletes it at the end.

export KILN_TEMPLATE="$PWD"
mkdir -p "${XDG_CACHE_HOME:-$HOME/.cache}"
KILN_DEMO_HOME="$(mktemp -d "${XDG_CACHE_HOME:-$HOME/.cache}/kiln-demo.XXXXXX")"
export KILN_DEMO_HOME
# Also gone if the recording stops halfway.
trap 'rm -rf "$KILN_DEMO_HOME"' EXIT
export COLORTERM=truecolor
mkdir -p "$KILN_DEMO_HOME/code"
cd "$KILN_DEMO_HOME/code" || return

KILN_DEMO_MAIN='
import os, sys
from pathlib import Path
from unittest import mock
from kiln import banner, cli

home = Path(os.environ["KILN_DEMO_HOME"])
mock.patch.object(banner, "installed_version", lambda: "").start()
mock.patch.object(banner, "_home_relative", lambda path: f"~/{path.relative_to(home)}").start()
sys.argv[0] = "kiln"
cli.main()
'

# The environment's own Python, as an installed kiln runs: `uv run` would hand the projects
# kiln creates its `VIRTUAL_ENV`, and their `uv` would warn about it on screen.
kiln() {
    "$KILN_TEMPLATE/.venv/bin/python" -c "$KILN_DEMO_MAIN" "$@"
}

# Synced once here, so the recording never shows uv preparing the environment.
uv sync --quiet --project "$KILN_TEMPLATE"
PS1='\[\e[38;2;140;140;135m\]$\[\e[0m\] '
clear
