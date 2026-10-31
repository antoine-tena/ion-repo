#!/usr/bin/env bash
# Former path (plugin `base`, before kiln 0.4), still named by sessions started before the
# update: runs plugins/repo/scripts/prepare-worktree.sh.
exec bash "$(dirname "$0")/../../repo/scripts/prepare-worktree.sh" "$@"
