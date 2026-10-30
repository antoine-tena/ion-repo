"""`kiln update --rehearse`: the update on a throwaway clone, the repo untouched (T-150)."""

import subprocess
import tempfile
from pathlib import Path

import pytest

from kiln import rehearsal
from kiln.shell import KilnError


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    # The clones go under the test's folder, not the machine's /tmp.
    (tmp_path / "tmp").mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "tmp"))
    root = tmp_path / "demo"
    root.mkdir()
    git(root, "init", "-q", "-b", "develop")
    (root / ".gitignore").write_text(".env\nbackend/.env\n")
    (root / "README.md").write_text("demo\n")
    (root / ".copier-answers.yml").write_text("stack: python\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "start")
    (root / ".env").write_text("SECRET=local\n")
    (root / "backend").mkdir()
    (root / "backend/.env").write_text("DB=local\n")
    return root


def test_the_update_runs_on_a_clone_and_the_repo_is_untouched(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[Path] = []

    def update(clone: Path, **_: object) -> None:
        seen.append(clone)
        assert (clone / ".env").read_text() == "SECRET=local\n"
        assert (clone / "backend/.env").read_text() == "DB=local\n"
        assert git(clone, "branch", "--show-current") == rehearsal.REHEARSAL_BRANCH
        (clone / "README.md").write_text("updated\n")
        (clone / "new.txt").write_text("x\n")

    monkeypatch.setattr(rehearsal, "update_project", update)

    outcome = rehearsal.rehearse(repo, should_update_deps=False, allow_major=False)

    assert outcome.succeeded
    assert outcome.summary == "updates cleanly: 2 files changed, checks green"
    assert (repo / "README.md").read_text() == "demo\n"
    assert git(repo, "status", "--porcelain") == ""
    assert not seen[0].exists()  # a clean rehearsal leaves nothing behind


def test_a_failed_rehearsal_keeps_its_clone_and_says_why(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def update(clone: Path, **_: object) -> None:
        raise KilnError("Invalid choice for 'frontend'")

    monkeypatch.setattr(rehearsal, "update_project", update)

    outcome = rehearsal.rehearse(repo, should_update_deps=False, allow_major=False)
    assert not outcome.succeeded
    assert "Invalid choice for 'frontend'" in outcome.summary
    kept = Path(outcome.summary.rsplit("clone kept in ", 1)[1].rstrip(")"))
    assert kept.is_dir()
    with pytest.raises(KilnError, match="rehearsal: the update fails"):
        rehearsal.rehearse_project(repo, should_update_deps=False, allow_major=False)


def test_a_repo_not_under_kiln_is_refused_before_any_clone(tmp_path: Path, repo: Path) -> None:
    (repo / ".copier-answers.yml").unlink()
    with pytest.raises(KilnError, match="not under kiln"):
        rehearsal.rehearse(repo, should_update_deps=False, allow_major=False)
    assert list((tmp_path / "tmp").iterdir()) == []
