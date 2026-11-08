"""What `ion repo check` looks at: the branch's changes, the whole repo on a release branch."""

import subprocess
from pathlib import Path

import pytest

from ion_repo import check


def _repo(root: Path, branch: str) -> Path:
    subprocess.run(["git", "init", "-q", "-b", branch, str(root)], check=True)
    return root


@pytest.mark.parametrize("branch", ["release/v1.2.3", "hotfix/v1.2.4"])
def test_a_release_branch_checks_the_whole_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, branch: str
) -> None:
    scopes: list[list[str] | None] = []

    def record(_root: Path, _with_tests: bool, changed: list[str] | None) -> list[str]:
        scopes.append(changed)
        return []

    monkeypatch.setattr(check, "changed_files", lambda _root: [])
    monkeypatch.setattr(check, "run_checks", record)
    check.check_project(_repo(tmp_path, branch))
    assert scopes == [None]


def test_a_branch_without_changes_does_not_claim_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check, "changed_files", lambda _root: [])
    check.check_project(_repo(tmp_path, "feat/nothing"))
    printed = capsys.readouterr()
    output = printed.out + printed.err
    assert "nothing was checked" in output
    assert "--all --tests" in output
    assert "✓" not in output
