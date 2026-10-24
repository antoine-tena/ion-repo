# shellcheck shell=bash
# The shell of the README's recorded demos (`docs/assets/*.tape`), sourced by each tape before
# it shows anything. Replay a demo from kiln's root: `vhs docs/assets/kiln-new.tape` (needs vhs,
# ttyd and ffmpeg). kiln runs from this checkout, its template rendered as a release would, in a
# fresh folder that the banner calls `~/code`, without a version number that would date the
# recording, as `scripts/screenshots.py` does for the still images. The folder is on disk, not
# in `/tmp` (often held in memory), as a generated app weighs about 500 MB: the tape deletes it
# at the end.

KILN_CHECKOUT="$PWD"
mkdir -p "${XDG_CACHE_HOME:-$HOME/.cache}"
KILN_DEMO_HOME="$(mktemp -d "${XDG_CACHE_HOME:-$HOME/.cache}/kiln-demo.XXXXXX")"
export KILN_DEMO_HOME
# Also gone if the recording stops halfway.
trap 'rm -rf "$KILN_DEMO_HOME"' EXIT
export COLORTERM=truecolor
mkdir -p "$KILN_DEMO_HOME/code"

# The template is rendered as a release renders it: a clone of the checkout's last commit, tagged
# with the version of `pyproject.toml`. Taken outside a release, it would cite kiln's workflows
# at `develop` rather than at a commit, and the new repo would miss PINNED-ACTIONS (97/100).
git clone --quiet "$KILN_CHECKOUT" "$KILN_DEMO_HOME/kiln"
git -C "$KILN_DEMO_HOME/kiln" tag --force \
    "v$(sed -n 's/^version = "\(.*\)"$/\1/p' "$KILN_CHECKOUT/pyproject.toml")" >/dev/null
export KILN_TEMPLATE="$KILN_DEMO_HOME/kiln"
cd "$KILN_DEMO_HOME/code" || return

# The environment's own Python, as an installed kiln runs: `uv run` would hand the projects
# kiln creates its `VIRTUAL_ENV`, and their `uv` would warn about it on screen. A command on the
# `PATH` rather than a shell function, so that Claude Code finds it too.
mkdir -p "$KILN_DEMO_HOME/bin"
cat >"$KILN_DEMO_HOME/bin/kiln" <<EOF
#!$KILN_CHECKOUT/.venv/bin/python
import os, sys
from pathlib import Path
from unittest import mock
from kiln import banner, cli

home = Path(os.environ["KILN_DEMO_HOME"])
mock.patch.object(banner, "installed_version", lambda: "").start()
mock.patch.object(banner, "_home_relative", lambda path: f"~/{path.relative_to(home)}").start()
sys.argv[0] = "kiln"
cli.main()
EOF
chmod +x "$KILN_DEMO_HOME/bin/kiln"
export PATH="$KILN_DEMO_HOME/bin:$PATH"

# Claude Code as a visitor has it: none of this machine's settings, instructions or status line
# (the repo's own settings only), kiln's plugin from this checkout. Recorded from a Claude Code
# session, the shell would also hand it that session's variables.
unset "${!CLAUDE@}"
claude() {
    command claude --setting-sources project,local --plugin-dir "$KILN_CHECKOUT/plugins/kiln" "$@"
}

# Synced once here, so the recording never shows uv preparing the environment.
uv sync --quiet --project "$KILN_CHECKOUT"
PS1='\[\e[38;2;140;140;135m\]$\[\e[0m\] '
clear
