#!/usr/bin/env python3
"""PreToolUse (Edit/Write/NotebookEdit): protects secrets, tokens, lockfiles and archives.

These files are not edited by hand.
"""

import json
import os
import re
import sys

path = json.load(sys.stdin).get("tool_input", {}).get("file_path") or ""
name = os.path.basename(path)
LOCKFILES = {
    "uv.lock",
    "poetry.lock",
    "pnpm-lock.yaml",
    "package-lock.json",
    "yarn.lock",
    "bun.lockb",
    "Cargo.lock",
}

if "/docs/_archive/" in path:
    reason = "docs/_archive/ is closed"
elif re.fullmatch(r"\.env(\..*)?", name) and not name.endswith((".example", ".sample")):
    reason = "secrets file"
elif re.search(r"/\.[\w-]+/token$", path):
    reason = "service token: the user pastes it themselves"
elif name in LOCKFILES:
    reason = "lockfile: go through the package manager"
else:
    sys.exit(0)
print(f"Edit refused ({reason}): {path}", file=sys.stderr)
sys.exit(2)
