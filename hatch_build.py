"""Build hook: what the tool is built from, written into the package (`ion_repo/_build.json`).

A tool installed from a folder (`uv tool install ~/code/kiln`) is a copy of that folder taken at
install time: what it is must be read from the copy, not from the folder, which keeps moving.
Without git (a build from the sdist), nothing is written.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

BUILD_INFO = "ion_repo/_build.json"


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        # An editable install runs the folder itself: kiln reads it live.
        if version == "editable":
            return
        described = _git(
            self.root, "describe", "--tags", "--always", "--dirty", "--match", "v[0-9]*"
        )
        commit = _git(self.root, "rev-parse", "HEAD")
        if not described or not commit:
            return
        info = Path(tempfile.mkdtemp()) / "_build.json"
        info.write_text(json.dumps({"describe": described, "commit": commit}) + "\n")
        build_data["force_include"][str(info)] = BUILD_INFO


def _git(root: str, *args: str) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", root, *args], capture_output=True, text=True, timeout=10, check=False
        )
    except subprocess.TimeoutExpired, OSError:
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""
