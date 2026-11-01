"""An adopted repo's references to ion-repo's workflows, moved to the last public release
(T-146)."""

import subprocess
from pathlib import Path

import pytest

from ion_repo import adopted, adopted_names, fleet, update
from ion_repo.shell import KilnError

CI = """\
name: CI
on: push
jobs:
  charter:
    uses: antoine-tena/ion-repo/.github/workflows/charter.yml@v0.3.4  # ion-repo's charter
  backend:
    uses: antoine-tena/ion-repo/.github/workflows/python.yml@develop
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
    assert "charter.yml@v0.4.0  # ion-repo's charter" in text
    assert "actions/checkout@v5" in text  # not ion-repo's: untouched
    assert adopted.move_to_release(repo, "v0.4.0", fetch) == []


def test_a_reference_pinned_by_sha_stays_pinned_at_the_release(repo: Path) -> None:
    """`ion repo fix` pins ion-repo's workflows too ([PINNED-ACTIONS]): the release's SHA, its tag
    in the comment, read back as the release quoted."""
    old, new = "a" * 40, "b" * 40
    ci = repo / ".github/workflows/ci.yml"
    ci.write_text(
        CI.replace("charter.yml@v0.3.4  # ion-repo's charter", f"charter.yml@{old} # v0.3.4")
    )
    assert adopted.quoted_refs(repo) == {"v0.3.4", "develop"}

    adopted.move_to_release(repo, "v0.4.0", fetch, resolve={"v0.4.0": new}.__getitem__)

    text = ci.read_text()
    assert f"charter.yml@{new} # v0.4.0\n" in text
    assert "python.yml@v0.4.0\n" in text  # quoted by tag: stays a tag
    assert adopted.quoted_refs(repo) == {"v0.4.0"}


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
    subprocess.run([*git, "init", "-q", "-b", "chore/ion-repo-update"], check=True)
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


def test_on_the_beta_channel_an_adopted_repo_follows_kilns_develop(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(adopted, "is_beta", lambda: True)
    monkeypatch.setattr(adopted, "_fetch", fetch)

    adopted.update_adopted(repo)

    assert adopted.quoted_refs(repo) == {"develop"}


def test_status_says_when_an_adopted_repo_quotes_an_older_release(repo: Path) -> None:
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted develop, v0.3.4 → v0.4.0"
    adopted.move_to_release(repo, "v0.4.0", fetch)
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted v0.4.0"
    (repo / ".github/workflows/ci.yml").unlink()
    assert fleet.adopted_state(repo, "v0.4.0") == "adopted"


LEGACY_CHARTER = """\
envergure = "flame"

[interdictions.signaux-django]
id = "SIGNAUX"

[interdictions.renvois-audit]
id = "RENVOIS-AUDIT"
exclus = '(^docs/|^charte\\.toml$)'

[cliquets.taille]
regle = "taille-fichier"
id = "TAILLE-FICHIER"
"""
LEGACY_HOOKS = """\
      - id: charte
        entry: charte
      - id: typage
        entry: charte types
      - id: couverture
        entry: "charte couverture"
"""
LEGACY_CI = """\
jobs:
  schema:
    uses: antoine-tena/ion-repo/.github/workflows/contrat-api.yml@v0.3.4
    with:
      back: backend
      front: frontend
  own:
    runs-on: ubuntu-latest
    with:
      back: kept
"""


def test_an_adopted_repo_moves_to_todays_names_keeping_its_rule_ids(tmp_path: Path) -> None:
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / ".github/workflows/ci.yml").write_text(LEGACY_CI)
    (tmp_path / ".pre-commit-config.yaml").write_text(LEGACY_HOOKS)
    (tmp_path / "charte.toml").write_text(LEGACY_CHARTER)

    done = adopted_names.convert_legacy_names(tmp_path)

    assert len(done) == 3 and not (tmp_path / "charte.toml").exists()
    charter = (tmp_path / "charter.toml").read_text()
    assert 'size = "flame"' in charter and "[bans.django-signals]" in charter
    assert 'rule = "file-size"' in charter and 'id = "TAILLE-FICHIER"' in charter
    assert "^charter\\.toml$" in charter
    hooks = (tmp_path / ".pre-commit-config.yaml").read_text()
    assert "entry: charter\n" in hooks and "entry: charter types" in hooks
    assert 'entry: "charter coverage"' in hooks and "id: charte\n" in hooks
    ci = (tmp_path / ".github/workflows/ci.yml").read_text()
    assert "workflows/api-contract.yml@v0.3.4" in ci
    assert "      backend: backend\n      frontend: frontend\n" in ci
    assert "      back: kept\n" in ci
    assert adopted_names.convert_legacy_names(tmp_path) == []


def test_an_adopted_repo_moves_its_a_faire_to_the_backlog(tmp_path: Path) -> None:
    (tmp_path / "docs/a-faire").mkdir(parents=True)
    (tmp_path / "docs/a-faire/a-faire.md").write_text(
        "# À faire\n\nIntro.\n\n---\n\n## 🔴 Critique\n\n### AF-07 · Payer\n- **État** : à faire\n"
    )
    (tmp_path / "docs/backlog").mkdir(parents=True)
    (tmp_path / "docs/backlog/backlog.md").write_text("# Backlog\n\n---\n\n## 🔴 Critical\n")
    (tmp_path / "notes.py").write_text("# see AF-07\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)

    adopted._move_legacy_backlog(tmp_path)

    assert "### T-07 · Payer" in (tmp_path / "docs/backlog/backlog.md").read_text()
    assert not (tmp_path / "docs/a-faire").exists()
    assert adopted_names.ticket_mentions(tmp_path) == ["notes.py"]
