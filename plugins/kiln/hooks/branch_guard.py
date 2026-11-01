#!/usr/bin/env python3
"""Former path of the kiln plugin (before ion-repo, 31 October 2026), still called by sessions
started before the rename: runs plugins/repo/hooks/branch_guard.py."""

import runpy
import sys
from pathlib import Path

script = Path(__file__).resolve().parents[2] / "repo" / "hooks" / "branch_guard.py"
sys.path.insert(0, str(script.parent))
sys.argv[0] = str(script)
runpy.run_path(str(script), run_name="__main__")
