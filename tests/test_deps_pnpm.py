"""pnpm updates from a fresh worktree, without `node_modules`."""

import os
from pathlib import Path

import pytest

from ion_repo.deps import update_pnpm

FAKE_PNPM = """#!/bin/sh
case "$1" in
  install) mkdir -p node_modules ;;
  outdated)
    if [ -d node_modules ]; then
      echo '{"nuxt": {"current": "4.6.2", "latest": "4.7.0", "dependencyType": "dependencies"}}'
    else
      echo '{"nuxt": {"wanted": "4.6.2", "latest": "4.7.0", "dependencyType": "dependencies"}}'
    fi ;;
  add) echo "$@" > added.txt ;;
esac
"""


def test_pnpm_update_installs_before_reading_outdated(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pnpm = bin_dir / "pnpm"
    pnpm.write_text(FAKE_PNPM)
    pnpm.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    project_dir = tmp_path / "frontend"
    project_dir.mkdir()

    update_pnpm(project_dir, allow_major=False)

    assert (project_dir / "added.txt").read_text().split() == ["add", "nuxt@4.7.0"]
