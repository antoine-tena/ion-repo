"""`ion repo update` with conflicts left by the template: stopped before anything reads the
files."""

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
    monkeypatch.setattr(update, "apply_pieces", lambda *a: None)
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


def test_the_follow_up_of_a_conflict_runs_the_converters(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ion-repo#T-400: stopped at a conflict, then resumed with `--no-template` once it is
    committed, the update still closes what the template leaves (pinned SHAs)."""
    converted: list[str] = []
    for name in (
        "check_working_branch",
        "check_tool_not_older",
        "show_release_notes",
        "report_frozen_drift",
        "mention_newer_release",
        "report_changes",
        "apply_template",
        "apply_pieces",
        "generate_api_contract",
        "write_unverified_rules",
        "update_dependencies",
        "lock_dependencies",
        "sync_dependencies",
        "load_stack",
    ):
        monkeypatch.setattr(update, name, lambda *a, **k: None)
    monkeypatch.setattr(update, "require_tools", lambda *a: None)
    monkeypatch.setattr(update, "is_adopted", lambda root: False)
    monkeypatch.setattr(update, "template_commit", lambda root: "v0")
    monkeypatch.setattr(update, "template_revision", lambda source: "v1")
    monkeypatch.setattr(update, "_template_source", lambda root: "")
    monkeypatch.setattr(update, "convert_in_place", lambda root, spared: converted.append("pin"))
    conflicts = [["ci.yml"]]  # the first run only
    monkeypatch.setattr(update, "conflicted_files", lambda root: conflicts and conflicts.pop())
    for template in (True, False):
        update.update_project(
            tmp_path,
            should_update_template=template,
            should_update_deps=False,
            allow_major=False,
            should_check=False,
        )
    assert converted == ["pin"]
