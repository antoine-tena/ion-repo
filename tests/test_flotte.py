import subprocess
from pathlib import Path

import pytest

from kiln import fleet
from kiln.config import UserConfig
from kiln.fleet import (
    MAX_FILES_PER_COMMIT,
    commit_in_batches,
    find_adopted,
    find_repos,
    integration_branch,
    template_state,
)
from kiln.shell import KilnError, step
from kiln.update import conflicted_files


def make_repo(root: Path, source: str) -> Path:
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    (root / ".copier-answers.yml").write_text(f"_commit: abc1234\n_src_path: {source}\n")
    return root


def test_only_kiln_repos_are_found(tmp_path: Path) -> None:
    make_repo(tmp_path / "association" / "projet", "https://github.com/antoine-tena/kiln.git")
    make_repo(tmp_path / "ancien", "https://github.com/antoine-tena/init-repo.git")
    make_repo(tmp_path / "autre", "gh:quelquun/modele")

    found = sorted(repo.root.name for repo in find_repos(tmp_path))

    assert found == ["ancien", "projet"]


def test_adopted_repo_has_a_charter_but_no_answers(tmp_path: Path) -> None:
    generated = make_repo(tmp_path / "genere", "https://github.com/antoine-tena/kiln.git")
    (generated / "charte.toml").touch()
    adopted = tmp_path / "association" / "adopte"
    (adopted / ".git").mkdir(parents=True)
    (adopted / "charte.toml").touch()

    assert find_adopted(tmp_path) == [adopted]


def test_commits_hold_at_most_ten_files(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "projet", "https://github.com/antoine-tena/kiln.git")
    git = ["git", "-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "init"], cwd=repo, check=True)
    for index in range(MAX_FILES_PER_COMMIT + 3):
        (repo / f"fichier_{index}.txt").write_text("contenu\n")

    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    commit_in_batches(repo)

    sizes = [
        len(
            subprocess.run(
                ["git", "show", "--name-only", "--format=", revision],
                cwd=repo,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.split()
        )
        for revision in ("HEAD", "HEAD~1")
    ]
    # Les treize fichiers et le fichier de réponses : dix, puis quatre.
    assert sorted(sizes) == [4, 10]


def test_conflicts_left_by_copier_are_found(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "projet", "https://github.com/antoine-tena/kiln.git")
    (repo / "README.md").write_text(
        "<<<<<<< before updating\nancien\n=======\nnouveau\n>>>>>>> after\n"
    )

    assert conflicted_files(repo) == ["README.md"]
    (repo / "README.md").write_text("nouveau\n")
    assert conflicted_files(repo) == []


def test_develop_wins_without_origin_head(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "projet", "https://github.com/antoine-tena/kiln.git")
    git = ["git", "-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "init"], cwd=repo, check=True)
    subprocess.run(
        ["git", "update-ref", "refs/remotes/origin/develop", "HEAD"], cwd=repo, check=True
    )

    assert integration_branch(repo) == "develop"


def test_local_develop_wins_without_origin(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "projet", "https://github.com/antoine-tena/kiln.git")
    git = ["git", "-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "init"], cwd=repo, check=True)
    subprocess.run(["git", "switch", "-q", "-c", "develop"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "-q", "-D", "main"], cwd=repo, check=True)

    assert integration_branch(repo) == "develop"


def test_template_state_compares_releases() -> None:
    assert template_state("v0.4.0", "v0.4.0") == "v0.4.0 up to date"
    assert template_state("v0.3.2", "v0.4.0") == "v0.3.2 → v0.4.0"
    assert template_state("v0.4.0-rc.1", "v0.4.0") == "v0.4.0-rc.1 → v0.4.0"
    assert template_state("f611f82", "v0.3.0") == "f611f82 → v0.3.0"
    assert template_state("v0.4.0", None) == "v0.4.0"


def test_missing_code_dir_is_explained(tmp_path: Path) -> None:
    with pytest.raises(KilnError, match="code_dir"):
        fleet.require_code_dir(tmp_path / "code")


def test_update_branch_is_merged_straight_into_integration(tmp_path: Path) -> None:
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "develop", str(origin)], check=True)
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)
    git = ["git", "-C", str(clone), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "init"], check=True)
    subprocess.run([*git, "push", "-q", "origin", "HEAD:develop"], check=True)
    subprocess.run([*git, "switch", "-q", "-c", "chore/kiln-update"], check=True)
    (clone / "f.txt").write_text("x\n")
    subprocess.run([*git, "add", "f.txt"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "chore: maj"], check=True)

    subprocess.run([*git, "config", "user.name", "t"], check=True)
    subprocess.run([*git, "config", "user.email", "t@t"], check=True)
    fleet._merge_into_integration(clone, "chore/kiln-update", "develop")

    log = subprocess.run(
        ["git", "-C", str(origin), "log", "--format=%s", "develop"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert log[0] == "Merge branch 'chore/kiln-update' into develop"
    assert "chore: maj" in log


def test_status_counts_waivers_across_the_fleet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(fleet, "latest_release", lambda **_: None)
    waiver = (
        '[[waiver]]\nrule = "TAILLE-FICHIER"\nreason = "r"\nby = "a"\n'
        'since = 2026-10-16\nuntil = "never"\n'
    )
    for name in ("un", "deux"):
        repo = make_repo(tmp_path / name, "https://github.com/antoine-tena/kiln.git")
        (repo / "kiln-waivers.toml").write_text(waiver)

    fleet.show_status(tmp_path)

    # A waiver written with a rule name of before kiln 0.4.0 counts under the current one.
    assert "FILE-SIZE (2)" in capsys.readouterr().out


def _clone_with_develop(tmp_path: Path) -> Path:
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "develop", str(origin)], check=True)
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)
    git = ["git", "-C", str(clone), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "init"], check=True)
    subprocess.run([*git, "push", "-q", "origin", "HEAD:develop"], check=True)
    return clone


def test_worktree_left_empty_by_a_failed_run_is_reused(tmp_path: Path) -> None:
    clone = _clone_with_develop(tmp_path)
    worktree = clone / fleet.WORKTREES_DIR / "chore-kiln-update"
    fleet._create_worktree(clone, worktree, "chore/kiln-update", "develop")

    fleet._create_worktree(clone, worktree, "chore/kiln-update", "develop")

    assert worktree.is_dir()


def test_worktree_with_changes_is_never_touched(tmp_path: Path) -> None:
    clone = _clone_with_develop(tmp_path)
    worktree = clone / fleet.WORKTREES_DIR / "chore-kiln-update"
    fleet._create_worktree(clone, worktree, "chore/kiln-update", "develop")
    (worktree / "travail.txt").write_text("à garder\n")

    with pytest.raises(KilnError, match="left work in"):
        fleet._create_worktree(clone, worktree, "chore/kiln-update", "develop")
    assert (worktree / "travail.txt").read_text() == "à garder\n"


def test_update_all_shows_one_line_per_repo_and_logs_the_rest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    code_dir = tmp_path / "code"
    for name in ("ok", "stuck"):
        make_repo(code_dir / name, "https://github.com/antoine-tena/kiln.git")
    monkeypatch.setattr(fleet, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(fleet, "require_tools", lambda *_: None)

    def noisy_update(root: Path, *, allow_major: bool) -> str:
        step("Check: charter")
        # A command's output, written straight to the descriptors (pre-commit's hooks).
        subprocess.run(["sh", "-c", "echo hook passed; echo hook warning >&2"], check=True)
        return "merged into develop" if root.name == "ok" else "failed: tree not clean\n  a.lock"

    monkeypatch.setattr(fleet, "update_one", noisy_update)

    fleet.update_all(code_dir, allow_major=False)

    shown = capfd.readouterr().out
    assert "hook" not in shown
    assert "Check: charter" not in shown
    assert "✓ ok" in shown and "merged into develop" in shown
    assert "✗ stuck" in shown and "a.lock" in shown
    assert "1 of 2 repos to finish by hand" in shown
    (log,) = (tmp_path / "logs").glob("*/stuck.log")
    assert f"log: {log}" in shown
    assert "hook passed" in log.read_text() and "hook warning" in log.read_text()


def test_an_update_with_nothing_to_take_runs_no_check_and_leaves_no_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    clone = _clone_with_develop(tmp_path)
    monkeypatch.setattr(fleet, "_update_worktree", lambda worktree, **_: None)
    monkeypatch.setattr(fleet, "run_checks", lambda root: pytest.fail("checks run"))

    assert fleet.update_one(clone, allow_major=False) == "already up to date"
    branches = subprocess.run(
        ["git", "branch"], cwd=clone, capture_output=True, text=True, check=True
    ).stdout
    assert "chore/kiln-update" not in branches


def test_conflicts_of_the_template_are_reported_before_any_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    clone = _clone_with_develop(tmp_path)

    def conflicted_update(worktree: Path, **_: object) -> None:
        (worktree / "pnpm-workspace.yaml").write_text("<<<<<<< before updating\n")

    monkeypatch.setattr(fleet, "_update_worktree", conflicted_update)
    monkeypatch.setattr(fleet, "conflicted_files", lambda root: ["pnpm-workspace.yaml"])
    # The checks would install from the conflicted pnpm-workspace.yaml, and fail on it.
    monkeypatch.setattr(fleet, "run_checks", lambda root: pytest.fail("checks run"))

    outcome = fleet.update_one(clone, allow_major=False)

    assert outcome.startswith("conflicts to resolve (pnpm-workspace.yaml)")


def test_a_frozen_repo_is_left_alone_by_update_all(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    code_dir = tmp_path / "code"
    for name in ("live", "witness"):
        make_repo(code_dir / name, "https://github.com/antoine-tena/kiln.git")
    monkeypatch.setattr(fleet, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(fleet, "require_tools", lambda *_: None)
    monkeypatch.setattr(fleet, "load_config", lambda: UserConfig(frozen_repos=("witness",)))
    updated: list[str] = []

    def update_one(root: Path, **_: object) -> str:
        updated.append(root.name)
        return "merged into develop"

    monkeypatch.setattr(fleet, "update_one", update_one)

    fleet.update_all(code_dir, allow_major=False)

    assert updated == ["live"]
    assert "✓ witness" in capfd.readouterr().out
