"""kiln update and a project of kiln 0.3: the conversions Copier cannot make."""

import os
import subprocess
from pathlib import Path

import pytest

from kiln import migrations

LEGACY_CHARTER = """\
# Notre commentaire.
envergure = "flame"
exclus = ["/migrations/"]
regles_non_verifiees = "scripts/ci/charte-non-verifiee.txt"

[cliquets.taille-fichier]
id = "TAILLE-FICHIER"
fichiers = ["backend/**/*.py"]
budget = 7  # dette de l'import X

[cliquets.horloge-tests]
regle = "occurrences"
id = "HORLOGE"
motif = "timezone.now()"
budget = 3
"""


def test_a_legacy_charter_keeps_its_budgets_and_comments() -> None:
    translated = migrations.translate_charter(LEGACY_CHARTER)

    assert 'size = "flame"' in translated
    assert 'exclude = ["/migrations/"]' in translated
    assert 'unverified_rules = "scripts/ci/unverified-rules.txt"' in translated
    assert '[ratchets.file-size]\nid = "FILE-SIZE"\nfiles = ["backend/**/*.py"]' in translated
    assert "budget = 7  # dette de l'import X" in translated
    assert '[ratchets.horloge-tests]\nrule = "occurrences"\nid = "CLOCK"\npattern = ' in translated
    assert translated.startswith("# Notre commentaire.\n")


def test_the_project_additions_to_a_generated_file_are_found() -> None:
    rendered = "# Title\n\n- rule a\n- rule b\n"
    project = "# Title\n\n- rule a\n- our own rule\n- rule b\n\n## Our section\nmore\n"

    added = migrations.additions(rendered, project)

    assert "- our own rule" in added and "#### Our section" in added and "- rule a" not in added


def test_the_carried_over_additions_keep_the_outline_of_the_file() -> None:
    rendered = "# Title\n\n## Map\n\n- `src/`: code\n\n## Language\n\n- English\n"
    project = (
        "# Title\n\n## Map\n\n- `src/`: code\n- `docs/`: our docs\n\n## Language\n\n- English\n\n"
        "## Ours\n\n- rule\n\n### Detail\n\n```sh\n# not a heading\n```\n- `team.md`: who\n"
    )

    added = migrations.additions(rendered, project)

    # Under `### From`: the section a line was added to is named, headings go one level below.
    assert added == [
        "#### Map", "", "- `docs/`: our docs", "",
        "#### Ours", "", "- rule", "", "##### Detail", "", "```sh", "# not a heading", "```",
        "- `team.md`: who", "",
    ]  # fmt: skip


def test_legacy_answers_get_their_new_names_and_the_team_of_that_time(tmp_path: Path) -> None:
    (tmp_path / ".copier-answers.yml").write_text(
        "_commit: v0.3.3\nnom: myapp\nenvergure: flame\nbackend: java\nfrontend: aucun\n"
    )

    data = migrations.answers_for_update(tmp_path, {"podman": True})

    assert data["name"] == "myapp" and data["size"] == "flame" and data["frontend"] == "none"
    assert data["language"] == "fr" and data["java_package"] == "fr.myapp" and data["podman"]
    assert "nom" not in data


def test_rules_are_cited_by_their_new_identifiers(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "service.py").write_text(
        "# [TEMPS-CONSTANT]: compare_digest\nvalue = rows[INDEX]\n# see [INDEX]\n"
    )

    migrations.convert_rule_references(tmp_path)

    text = (tmp_path / "service.py").read_text()
    assert "# [CONSTANT-TIME]: compare_digest" in text
    assert "rows[INDEX]" in text and "# see [INDEXES]" in text


@pytest.mark.parametrize(("visibility", "runner"), [("PUBLIC", "github"), ("PRIVATE", "local")])
def test_the_ci_runs_where_it_costs_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, visibility: str, runner: str
) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh = bin_dir / "gh"
    gh.write_text(f"#!/bin/sh\necho {visibility}\n")
    gh.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")
    (tmp_path / ".copier-answers.yml").write_text("_commit: v0.4.0\nname: myapp\n")

    assert migrations.answers_for_update(tmp_path, {})["ci_runner"] == runner
    # Said once, kept: the answer wins over the visibility.
    (tmp_path / ".copier-answers.yml").write_text("_commit: v0.4.0\nci_runner: local\n")
    assert "ci_runner" not in migrations.answers_for_update(tmp_path, {})


def test_without_gh_the_ci_stays_on_the_machine(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))  # no gh at all

    assert migrations.ci_runner_for(tmp_path) == "local"
