import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from ion_repo import adopt, update
from ion_repo.shell import KilnError
from ion_repo.stack import detect_stack

TEMPLATE_DIR = str(Path(__file__).resolve().parent.parent)
GIT_IDENTITY = ["-c", "user.name=N", "-c", "user.email=n@example.com", "-c", "commit.gpgsign=false"]


def commit(root: Path, message: str) -> None:
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(root), *GIT_IDENTITY, "commit", "-q", "-m", message], check=True
    )


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An existing repo of one's own, on a work branch; the `charter` command does not run."""
    monkeypatch.setattr(adopt, "run_status", lambda *args, **kwargs: 0)
    monkeypatch.setattr(adopt, "ci_runner_for", lambda root: "local")
    root = tmp_path / "Mon_Outil"
    subprocess.run(["git", "init", "-q", "-b", "chore/ion-repo-adopt", str(root)], check=True)
    (root / "outil.py").write_text("print('ok')\n")
    (root / "README.md").write_text("# Mon outil\n")
    (root / ".gitignore").write_text("dist/\n")
    commit(root, "a")
    return root


def answers(root: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = yaml.safe_load((root / ".copier-answers.yml").read_text())
    return loaded


def test_adoption_lays_what_kiln_new_writes_and_keeps_the_repo_s_files(repo: Path) -> None:
    adopt.adopt_project(repo, size="medium", template=TEMPLATE_DIR)

    for laid in (
        "CLAUDE.md",
        ".claude/rules/ion-repo/charter.md",
        ".claude/settings.json",
        ".pre-commit-config.yaml",
        ".github/workflows/ci.yml",
        "docs/backlog/backlog.md",
    ):
        assert (repo / laid).is_file(), laid
    assert 'size = "medium"' in (repo / "charter.toml").read_text()
    assert (repo / "README.md").read_text() == "# Mon outil\n"
    assert (repo / "outil.py").read_text() == "print('ok')\n"
    gitignore = (repo / ".gitignore").read_text()
    assert gitignore.startswith("dist/\n") and "\n# ion-repo\n" in gitignore
    assert answers(repo)["kept"] == [".gitignore", "README.md"]
    assert answers(repo)["backend"] == answers(repo)["frontend"] == "none"
    assert not (repo / "backend").exists()


def test_a_stack_in_its_folders_gets_its_rules_but_its_code_stays_its_own(repo: Path) -> None:
    (repo / "frontend").mkdir()
    (repo / "frontend/nuxt.config.ts").write_text("export default {}\n")
    commit(repo, "nuxt")

    adopt.adopt_project(repo, template=TEMPLATE_DIR)

    assert (repo / ".claude/rules/ion-repo/nuxt.md").is_file()
    assert sorted(path.name for path in (repo / "frontend").iterdir()) == ["nuxt.config.ts"]
    assert "frontend" in answers(repo)["kept"]
    assert answers(repo)["frontend"] == "nuxt"


def test_a_vite_app_at_the_root_gets_its_stack_there(tmp_path: Path, repo: Path) -> None:
    # Issue #59: a course's Vite app at the root got the common part only (ion-repo#T-166).
    (repo / "vite.config.ts").write_text("export default {}\n")
    (repo / "package.json").write_text('{"dependencies": {"react": "19"}}')
    commit(repo, "vite")
    template = tmp_path / "kiln"
    subprocess.run(["git", "clone", "-q", "--no-tags", TEMPLATE_DIR, str(template)], check=True)

    adopt.adopt_project(repo, template=str(template))

    assert (answers(repo)["frontend"], answers(repo)["frontend_dir"]) == ("vite-react", ".")
    assert "frontend" in answers(repo)["kept"]
    assert not (repo / "frontend").exists()
    assert (repo / ".claude/rules/ion-repo/vite-react.md").is_file()
    ci = yaml.safe_load((repo / ".github/workflows/ci.yml").read_text())
    assert ci["jobs"]["frontend"]["with"]["directory"] == "."
    stack = detect_stack(repo)
    assert (stack.frontend, stack.frontend_dir, stack.pnpm_dir) == ("vite-react", ".", ".")

    commit(repo, "adopt ion-repo")
    (template / "template/.editorconfig").write_text("root = true\n# newer\n")
    commit(template, "template moves on")
    update.apply_template(repo)

    assert (repo / ".editorconfig").read_text() == "root = true\n# newer\n"
    assert not (repo / "frontend").exists()
    assert answers(repo)["frontend_dir"] == "."
    assert yaml.safe_load((repo / ".github/workflows/ci.yml").read_text()) == ci


def test_kiln_update_replays_the_template_and_spares_what_the_repo_keeps(
    tmp_path: Path, repo: Path
) -> None:
    template = tmp_path / "kiln"
    subprocess.run(["git", "clone", "-q", "--no-tags", TEMPLATE_DIR, str(template)], check=True)
    adopt.adopt_project(repo, template=str(template))
    commit(repo, "adopt ion-repo")
    (template / "template/.editorconfig").write_text("root = true\n# newer\n")
    (template / "template/README.md.jinja").write_text("# {{ title }}, newer\n")
    commit(template, "template moves on")

    update.apply_template(repo)

    assert (repo / ".editorconfig").read_text() == "root = true\n# newer\n"
    assert (repo / "README.md").read_text() == "# Mon outil\n"


def test_adoption_refuses_kiln_repos_and_dirty_trees(repo: Path) -> None:
    (repo / "brouillon.txt").write_text("")
    with pytest.raises(KilnError, match="working tree not clean"):
        adopt.check_adoptable(repo)
    (repo / "charte.toml").write_text("")  # adopted before kiln 0.4.0
    with pytest.raises(KilnError, match="ion repo update first moves its names"):
        adopt.check_adoptable(repo)
    (repo / ".copier-answers.yml").write_text("")
    with pytest.raises(KilnError, match="generated by ion-repo"):
        adopt.check_adoptable(repo)


def test_on_an_integration_branch_kiln_opens_its_work_branch(repo: Path) -> None:
    def current() -> str:
        return subprocess.run(
            ["git", "-C", str(repo), "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    subprocess.run(["git", "-C", str(repo), "switch", "-q", "-c", "develop"], check=True)
    update.leave_protected_branch(repo, "chore/ion-repo-update")
    assert current() == "chore/ion-repo-update"

    subprocess.run(["git", "-C", str(repo), "switch", "-q", "develop"], check=True)
    update.leave_protected_branch(repo, "chore/ion-repo-update")
    assert current().startswith("chore/ion-repo-update-")

    subprocess.run(["git", "-C", str(repo), "switch", "-q", "develop"], check=True)
    with pytest.raises(KilnError, match="merge or delete them"):
        update.leave_protected_branch(repo, "chore/ion-repo-update")

    update.leave_protected_branch(repo, "chore/ion-repo-set")
    assert current() == "chore/ion-repo-set"
    update.leave_protected_branch(repo, "chore/ion-repo-other")  # already on a work branch
    assert current() == "chore/ion-repo-set"


def test_a_repo_adopted_before_is_completed(repo: Path) -> None:
    (repo / "charter.toml").write_text('size = "spark"\n')
    commit(repo, "adopted by kiln 0.4.5")

    adopt.adopt_project(repo, template=TEMPLATE_DIR)

    assert (repo / "charter.toml").read_text() == 'size = "spark"\n'
    assert "charter.toml" in answers(repo)["kept"]
    assert (repo / ".github/workflows/ci.yml").is_file()


def test_project_name_follows_the_template_format() -> None:
    assert adopt.project_name(Path("Mon_Outil")) == "mon-outil"
    assert adopt.project_name(Path("2048")) == "projet-2048"


def test_project_name_of_a_worktree_is_its_main_tree_s(tmp_path: Path) -> None:
    main = tmp_path / "club"
    subprocess.run(["git", "init", "-q", str(main)], check=True)
    subprocess.run(
        ["git", "-C", str(main), "-c", "user.name=t", "-c", "user.email=t@t",
         "commit", "-q", "--allow-empty", "-m", "init"],
        check=True,
    )  # fmt: skip
    worktree = main / ".claude/worktrees/chore-backlog"
    subprocess.run(["git", "-C", str(main), "worktree", "add", "-q", str(worktree)], check=True)

    assert adopt.project_name(worktree) == "club"


@pytest.mark.parametrize(("dependency", "frontend"), [("react", "vite-react"), ("vue", "none")])
def test_a_vite_app_is_taken_for_react_only_when_it_depends_on_it(
    tmp_path: Path, dependency: str, frontend: str
) -> None:
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend/vite.config.ts").write_text("export default {}\n")
    (tmp_path / "frontend/package.json").write_text(f'{{"dependencies": {{"{dependency}": "1"}}}}')

    assert detect_stack(tmp_path).frontend == frontend
