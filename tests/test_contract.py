"""`ion repo contract`: the export chosen from the backend, the front types only when scripted."""

import subprocess
from pathlib import Path

import pytest

from ion_repo.contract import EXPORT_COMMAND, SPECTACULAR_COMMAND, _scripts, export_command
from ion_repo.shell import KilnError, require_clean_tree


def test_kilns_own_export_comes_first(tmp_path: Path) -> None:
    commands = tmp_path / "config" / "management" / "commands"
    commands.mkdir(parents=True)
    (commands / "export_openapi.py").write_text("", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text('dependencies = ["drf-spectacular"]\n')
    assert export_command(tmp_path) == EXPORT_COMMAND


def test_a_drf_backend_exports_through_drf_spectacular(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('dependencies = ["drf-spectacular>=0.30.0"]\n')
    assert export_command(tmp_path) == SPECTACULAR_COMMAND


def test_no_export_is_said(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('dependencies = ["django"]\n')
    with pytest.raises(KilnError, match="no OpenAPI export"):
        export_command(tmp_path)


def test_front_scripts_read_from_package_json(tmp_path: Path) -> None:
    assert _scripts(tmp_path) == {}
    (tmp_path / "package.json").write_text('{"scripts": {"generate:api": "x"}}')
    assert "generate:api" in _scripts(tmp_path)


def test_a_dirty_tree_names_its_files(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    require_clean_tree(tmp_path)
    (tmp_path / "pnpm-lock.yaml").write_text("")
    with pytest.raises(KilnError, match=r"not clean.*\n  pnpm-lock\.yaml"):
        require_clean_tree(tmp_path)
