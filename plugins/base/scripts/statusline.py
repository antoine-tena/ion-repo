#!/usr/bin/env python3
"""Former path of kiln's status line (plugin `base`, before kiln 0.4), still named by existing
`statusLine` settings: runs plugins/kiln/scripts/statusline.py. `kiln set statusline=…` writes
the new path."""

import runpy
import sys
from pathlib import Path

script = Path(__file__).resolve().parents[2] / "kiln" / "scripts" / "statusline.py"
sys.argv[0] = str(script)
runpy.run_path(str(script), run_name="__main__")
