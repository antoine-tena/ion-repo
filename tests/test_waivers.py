"""Waivers of `kiln-waivers.toml`: tiers, expiry, targets, effect on the charter, frozen files
left alone by `kiln update`; and the charter of an adopted repo of before kiln 0.4.0, still read
under its French names."""

import datetime
import json
import subprocess
from pathlib import Path
from typing import Any

import copier
import pytest

from ion_repo.charter.cli import check
from ion_repo.charter.config import load as load_charter
from ion_repo.charter.repo import Repo
from ion_repo.charter.waivers import load
from ion_repo.frozen import report_frozen_drift
from ion_repo.update import apply_template, template_commit

TODAY = datetime.date(2026, 10, 16)
CHARTER = """
[ratchets.file-size]
id = "FILE-SIZE"
files = ["src/*.py"]
suffixes = [".py"]
max_lines = 3
budget = 0
"""
# The same, as a repo adopted before kiln 0.4.0 still writes it.
LEGACY_CHARTER = """
[cliquets.taille-fichier]
id = "TAILLE-FICHIER"
fichiers = ["src/*.py"]
suffixes = [".py"]
max_lignes = 3
budget = 0
"""


def waiver(**fields: object) -> str:
    """One `[[waiver]]` entry; a field set to None is left out."""
    entry = {
        "rule": "FILE-SIZE",
        "reason": "repris tel quel",
        "by": "antoine",
        "since": datetime.date(2026, 10, 14),
        "until": datetime.date(2026, 10, 20),
    } | fields
    lines = [f"{k} = {_toml(v)}" for k, v in entry.items() if v is not None]
    return "[[waiver]]\n" + "\n".join(lines) + "\n"


def _toml(value: object) -> str:
    return value.isoformat() if isinstance(value, datetime.date) else json.dumps(value)


def write(root: Path, *waivers: str) -> None:
    (root / "kiln-waivers.toml").write_text("\n".join(waivers))


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "charter.toml").write_text(CHARTER)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "long.py").write_text("a = 1\n" * 5)
    (tmp_path / "src" / "court.py").write_text("a = 1\n")
    return tmp_path


def test_first_period_is_one_week(tmp_path: Path) -> None:
    write(tmp_path, waiver(until=datetime.date(2026, 10, 30)))

    waivers = load(tmp_path, TODAY)

    assert not waivers.actives and "at most 7" in waivers.errors[0]


def test_each_renewal_lengthens_the_period(tmp_path: Path) -> None:
    write(
        tmp_path,
        waiver(since=datetime.date(2026, 10, 16), until=datetime.date(2026, 11, 15), renewals=1),
        waiver(since=datetime.date(2026, 10, 16), until=datetime.date(2027, 1, 14), renewals=2),
        waiver(since=datetime.date(2026, 10, 16), until=datetime.date(2027, 4, 16), renewals=7),
    )

    assert len(load(tmp_path, TODAY).actives) == 3


def test_expired_waiver_no_longer_applies(tmp_path: Path) -> None:
    write(tmp_path, waiver(since=datetime.date(2026, 10, 1), until=datetime.date(2026, 10, 8)))

    waivers = load(tmp_path, TODAY)

    assert not waivers.actives and "expired" in waivers.errors[0]


def test_warns_in_the_second_half_of_the_period(tmp_path: Path) -> None:
    write(tmp_path, waiver(since=datetime.date(2026, 10, 12), until=datetime.date(2026, 10, 18)))

    waivers = load(tmp_path, TODAY)

    assert waivers.actives and "in 2 day(s)" in waivers.warnings[0]


def test_permanent_waiver_is_always_shown(tmp_path: Path) -> None:
    write(tmp_path, waiver(until="never"))

    waivers = load(tmp_path, TODAY)

    assert waivers.actives[0].until is None and "permanent" in waivers.warnings[0]


@pytest.mark.parametrize(
    ("fields", "message"),
    [
        ({"rule": "PERSONAL-DATA"}, "cannot be waived"),
        ({"rule": "DONNEES-PERSO"}, "[PERSONAL-DATA] cannot be waived"),
        ({"reason": None}, "`reason` missing"),
        ({"file": "ci.yml"}, "only one"),
        ({"motif": "x"}, "unknown key"),
    ],
)
def test_malformed_waiver_is_refused(tmp_path: Path, fields: dict[str, Any], message: str) -> None:
    write(tmp_path, waiver(**fields))

    assert message in load(tmp_path, TODAY).errors[0]


def test_waiver_excludes_its_paths_from_the_rule(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    today = datetime.date.today()
    write(repo, waiver(paths=["src/long.py"], since=today, until=today))

    assert check(Repo(repo, load_charter(repo))) == 0
    assert "FILE-SIZE (src/long.py)" in capsys.readouterr().out


def test_without_waiver_the_rule_fails(repo: Path) -> None:
    assert check(Repo(repo, load_charter(repo))) == 1


def test_a_charter_of_before_0_4_is_read_under_its_french_names(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (repo / "charter.toml").unlink()
    (repo / "charte.toml").write_text('envergure = "flame"\n' + LEGACY_CHARTER)
    today = datetime.date.today()
    write(repo, waiver(rule="TAILLE-FICHIER", paths=["src/long.py"], since=today, until=today))

    config = load_charter(repo)

    assert config["size"] == "flame"
    assert config["ratchets"]["file-size"]["max_lines"] == 3
    assert check(Repo(repo, config)) == 0
    assert "FILE-SIZE (src/long.py)" in capsys.readouterr().out


def test_waiver_matching_nothing_fails(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    today = datetime.date.today()
    write(repo, waiver(paths=["src/gone.py"], since=today, until=today))

    assert check(Repo(repo, load_charter(repo))) == 1
    assert "no file for src/gone.py" in capsys.readouterr().out


def test_waiver_of_an_unknown_rule_fails(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    today = datetime.date.today()
    write(repo, waiver(rule="MADE-UP", since=today, until=today))

    assert check(Repo(repo, load_charter(repo))) == 1
    assert "no such rule" in capsys.readouterr().out


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def template_version(template: Path, tag: str, ci: str) -> None:
    (template / "ci.yml").write_text(ci)
    (template / "autre.txt").write_text(f"{tag}\n")
    git(template, "add", "-A")
    git(template, "commit", "-qm", tag)
    git(template, "tag", tag)


@pytest.fixture
def generated(tmp_path: Path) -> Path:
    """A repo generated from v1 of a small template, `ci.yml` edited and frozen; the template is
    at v2."""
    template, project = tmp_path / "modele", tmp_path / "projet"
    template.mkdir()
    git(template, "init", "-q")
    (template / "copier.yml").write_text("_answers_file: .copier-answers.yml\n")
    (template / "{{_copier_conf.answers_file}}.jinja").write_text(
        "{{ _copier_answers | to_nice_yaml }}"
    )
    template_version(template, "v1", "a\nb\n")
    copier.run_copy(str(template), project, vcs_ref="v1", defaults=True, quiet=True)
    (project / "ci.yml").write_text("a\nlocal\n")
    today = datetime.date.today()
    write(project, waiver(rule=None, file="ci.yml", since=today, until=today))
    git(project, "init", "-q")
    git(project, "add", "-A")
    git(project, "commit", "-qm", "init")
    template_version(template, "v2", "a\nb2\n")
    return project


def test_update_leaves_frozen_files_alone(generated: Path) -> None:
    apply_template(generated)

    assert (generated / "ci.yml").read_text() == "a\nlocal\n"
    assert (generated / "autre.txt").read_text() == "v2\n"


def test_update_reports_what_kiln_changed_in_frozen_files(
    generated: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    template = str(generated.parent / "modele")
    apply_template(generated)

    report_frozen_drift(generated, template, "v1", template_commit(generated))

    out = capsys.readouterr().out
    assert "ci.yml" in out and "-b\n+b2" in out


def test_waiver_also_applies_to_a_rule_that_scans_the_whole_repo(repo: Path) -> None:
    checked = Repo(repo, load_charter(repo))
    checked.waived = ["src/long.py"]

    assert repo / "src/long.py" not in checked.tracked([])
