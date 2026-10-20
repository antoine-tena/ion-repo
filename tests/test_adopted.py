"""An adopted repo's references to kiln's workflows, moved to the last public release (T-146)."""

import subprocess
from pathlib import Path

import pytest

from kiln import adopted, fleet, update
from kiln.shell import KilnError

CI = """\
name: CI
on: push
jobs:
  charter:
    uses: antoine-tena/kiln/.github/workflows/charter.yml@v0.3.4  # kiln's charter
  backend:
    uses: antoine-tena/kiln/.github/workflows/python.yml@develop
    with:
      directory: backend
  own:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
"""
CHARTER_WORKFLOW = "on:\n  workflow_call:\n    inputs: {}\n"
PYTHON_WORKFLOW = "on:\n  workflow_call:\n    inputs:\n      directory: {type: string}\n"


def fetch(ref: str, file: str) -> str:
    return {"charter.yml": CHARTER_WORKFLOW, "python.yml": PYTHON_WORKFLOW}[Path(file).name]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / ".github/workflows/ci.yml").write_text(CI)
    (tmp_path / "charter.toml").write_text('size = "ember"\n')
    return tmp_path


def test_only_kiln_references_move_to_the_release(repo: Path) -> None:
    assert adopted.quoted_refs(repo) == {"v0.3.4", "develop"}

    changed = adopted.move_to_release(repo, "v0.4.0", fetch)

    text = (repo / ".github/workflows/ci.yml").read_text()
    assert changed == [".github/workflows/ci.yml"]
    assert adopted.quoted_refs(repo) == {"v0.4.0"}
    assert "charter.yml@v0.4.0  # kiln's charter" in text
    assert "actions/checkout@v5" in text  # not kiln's: untouched
    assert adopted.move_to_release(repo, "v0.4.0", fetch) == []


def test_an_input_the_release_no_longer_takes_stops_everything(repo: Path) -> None:
    def without_inputs(ref: str, file: str) -> str:
        return CHARTER_WORKFLOW

    with pytest.raises(KilnError, match=r"input `directory` unknown to .*python\.yml@v0\.4\.0"):
        adopted.move_to_release(repo, "v0.4.0", without_inputs)
    assert (repo / ".github/workflows/ci.yml").read_text() == CI


def test_kiln_update_in_an_adopted_repo_moves_the_tag_only(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    git = ["git", "-C", str(repo)]
    subprocess.run([*git, "init", "-q", "-b", "chore/kiln-update"], check=True)
    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "adopted"], check=True)
    monkeypatch.setattr(adopted, "latest_release", lambda candidates: "v0.4.0")
    monkeypatch.setattr(adopted, "_fetch", fetch)

    assert update.is_adopted(repo)
    update.update_project(
        repo, should_update_template=True, should_update_deps=True, allow_major=False,
        should_check=False,
    )  # fmt: skip

    assert adopted.quoted_refs(repo) == {"v0.4.0"}


def test_status_says_when_an_adopted_repo_quotes_an_older_release(repo: Path) -> None:
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted develop, v0.3.4 → v0.4.0"
    adopted.move_to_release(repo, "v0.4.0", fetch)
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted v0.4.0"
    (repo / ".github/workflows/ci.yml").unlink()
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted"
