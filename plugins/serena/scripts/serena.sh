#!/usr/bin/env bash
# Starts Serena on the current worktree (each worktree is its own project, indexed in its
# .serena/ directory, ignored by git), in kiln's read-only context, without dashboard. Pinned
# version: bump it here after trying it.
set -euo pipefail
VERSION=2.0.0
here="$(cd "$(dirname "$0")" && pwd)"
project="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
exec uvx --from "serena-agent==$VERSION" serena start-mcp-server \
  --project "$project" --context "$here/read-only.yml" --mode no-memories --agent-interface tools \
  --enable-web-dashboard false --open-web-dashboard false --enable-gui-log-window false
