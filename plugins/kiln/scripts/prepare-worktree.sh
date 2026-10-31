#!/usr/bin/env bash
# Former path of the kiln plugin (before ion-repo), still named by sessions started before the
# rename: runs plugins/repo/scripts/prepare-worktree.sh.
exec bash "$(dirname "$0")/../../repo/scripts/prepare-worktree.sh" "$@"
