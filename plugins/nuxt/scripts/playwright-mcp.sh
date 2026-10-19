#!/bin/sh
# Starts the playwright MCP server on Playwright's Chromium, headless (WSL has no display) and
# with an in-memory profile: two worktrees or two sessions do not fight over the same profile.
# The default "chrome" channel required Google Chrome in /opt.
# The Chromium expected by this version of the MCP server installs on first run (a few seconds
# afterwards, when it is already there): a new worktree or a new machine has nothing to do.
VERSION=0.0.83
npx -y -p "@playwright/mcp@$VERSION" playwright-core install chromium >/dev/null 2>&1
exec npx -y "@playwright/mcp@$VERSION" --browser chromium --headless --isolated "$@"
