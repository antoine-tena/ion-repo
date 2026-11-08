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


def test_the_vps_plugin_s_names_become_ion_host_s() -> None:
    text = 'Run /vps:deploy, then /vps-podman:prod-logs; "vps@ion-repo", "vps@kiln"'

    assert rewrite(text) == (
        'Run /host:deploy, then /host:prod-logs; "host@ion-host", "host@ion-host"'
    )


def test_what_is_not_one_of_kiln_s_names_stays() -> None:
    text = "kiln-bot uses KILN_BOT_TOKEN; antoine-tena/kiln-measures; kiln:other; a kiln of clay"
    text += "; config/vps:deploy-remote.sh; vps:backup"

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


def test_kiln_waivers_toml_becomes_waivers_toml_in_git(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    waivers = '[[waiver]]\nrule = "FILE-SIZE"\nreason = "taken as is"\n'
    (tmp_path / "kiln-waivers.toml").write_text(waivers)
    (tmp_path / "README.md").write_text("Waivers: `kiln-waivers.toml`.\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "waivers"], cwd=tmp_path, check=True)

    done = convert_ion_names(tmp_path)

    assert not (tmp_path / "kiln-waivers.toml").exists()
    assert (tmp_path / "waivers.toml").read_text() == waivers
    assert (tmp_path / "README.md").read_text() == "Waivers: `waivers.toml`.\n"
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout
    assert "R  kiln-waivers.toml -> waivers.toml" in status
    assert "kiln-waivers.toml → waivers.toml" in done


def test_kiln_waivers_toml_next_to_waivers_toml_is_left_for_charter(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "kiln-waivers.toml").write_text("# old\n")
    (tmp_path / "waivers.toml").write_text("# new\n")

    convert_ion_names(tmp_path)

    assert (tmp_path / "kiln-waivers.toml").read_text() == "# old\n"
    assert (tmp_path / "waivers.toml").read_text() == "# new\n"
