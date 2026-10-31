"""kiln's names in a project, moved to ion-repo's by `ion repo update` (the Ion family)."""

import subprocess
from pathlib import Path

from ion_repo.ion_names import convert_ion_names, rewrite


def test_kiln_s_names_become_ion_repo_s() -> None:
    text = (
        '/kiln:merge, kiln:update, [REPORT-TO-KILN], $KILN_PROJECT, "kiln@kiln", '
        '"django@kiln", .claude/rules/kiln/cli.md, antoine-tena/kiln/.github/workflows/x.yml'
    )

    assert rewrite(text) == (
        '/repo:merge, repo:update, [REPORT-TO-ION-REPO], $ION_REPO_PROJECT, "repo@ion-repo", '
        '"django@ion-repo", .claude/rules/ion-repo/cli.md, '
        "antoine-tena/ion-repo/.github/workflows/x.yml"
    )


def test_what_is_not_one_of_kiln_s_names_stays() -> None:
    text = "kiln-bot uses KILN_BOT_TOKEN; antoine-tena/kiln-measures; kiln:other; a kiln of clay"

    assert rewrite(text) == text


def test_the_project_s_own_rules_move_and_history_stays(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".claude/rules/kiln").mkdir(parents=True)
    (tmp_path / ".claude/rules/kiln/ours.md").write_text("See /kiln:merge.\n")
    (tmp_path / ".claude/rules/kiln/charter.md").write_text("an edited copy\n")
    (tmp_path / ".claude/rules/ion-repo").mkdir(parents=True)
    (tmp_path / ".claude/rules/ion-repo/charter.md").write_text("the template's\n")
    (tmp_path / "CHANGELOG.md").write_text("- /kiln:merge learned to push\n")

    done = convert_ion_names(tmp_path)

    assert (tmp_path / ".claude/rules/ion-repo/ours.md").read_text() == "See /repo:merge.\n"
    assert (tmp_path / ".claude/rules/kiln/charter.md").is_file()  # a clash: left, named
    assert any("charter.md" in line and "by hand" in line for line in done)
    assert (tmp_path / "CHANGELOG.md").read_text() == "- /kiln:merge learned to push\n"


def test_a_project_without_kiln_s_names_is_left_alone(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("Run /repo:merge.\n")

    assert convert_ion_names(tmp_path) == []
