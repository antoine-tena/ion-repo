#!/usr/bin/env python3
"""Former path of a hook of the `base` plugin (before kiln 0.4), still called by sessions started
before the plugin became `kiln`: runs plugins/repo/hooks/check_file.py."""

import runpy
import sys
from pathlib import Path

script = Path(__file__).resolve().parents[2] / "repo" / "hooks" / "check_file.py"
sys.path.insert(0, str(script.parent))
sys.argv[0] = str(script)
runpy.run_path(str(script), run_name="__main__")
