"""`kiln update` with conflicts left by the template: stopped before anything reads the files."""

from pathlib import Path

import pytest

from ion_repo import update
from ion_repo.deps import _ignored_pnpm_dependencies
from ion_repo.shell import KilnError

CONFLICTED = """saveExact: true
<<<<<<< before updating
auditConfig:
  ignoreGhsas:
    - GHSA-x
=======
peerDependencyRules:
  allowedVersions: {}
>>>>>>> after updating
"""


def test_an_unreadable_workspace_is_a_kiln_error(tmp_path: Path) -> None:
    (tmp_path / "pnpm-workspace.yaml").write_text(CONFLICTED)
    with pytest.raises(KilnError, match=r"pnpm-workspace\.yaml: not valid YAML"):
        _ignored_pnpm_dependencies(tmp_path)


def test_conflicts_stop_the_update_after_the_template(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    for name in (
        "check_working_branch",
        "check_tool_not_older",
        "show_release_notes",
        "report_frozen_drift",
        "mention_newer_release",
        "report_changes",
    ):
        monkeypatch.setattr(update, name, lambda *a, _n=name, **k: calls.append(_n))
    monkeypatch.setattr(update, "require_tools", lambda *a: None)
    monkeypatch.setattr(update, "is_adopted", lambda root: False)
    monkeypatch.setattr(update, "template_commit", lambda root: "v0")
    monkeypatch.setattr(update, "template_revision", lambda source: "v1")
    monkeypatch.setattr(update, "_template_source", lambda root: "")
    monkeypatch.setattr(update, "apply_template", lambda root: None)
    monkeypatch.setattr(update, "conflicted_files", lambda root: ["frontend/pnpm-workspace.yaml"])
    monkeypatch.setattr(update, "update_dependencies", lambda *a, **k: calls.append("deps"))
    update.update_project(
        tmp_path,
        should_update_template=True,
        should_update_deps=True,
        allow_major=False,
        should_check=False,
    )
    assert "deps" not in calls
    assert "report_changes" in calls
