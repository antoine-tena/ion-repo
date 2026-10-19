#!/usr/bin/env bash
# Former path (plugin `base`, before kiln 0.4), still named by sessions started before the
# update: runs plugins/kiln/scripts/prepare-worktree.sh.
exec bash "$(dirname "$0")/../../kiln/scripts/prepare-worktree.sh" "$@"
