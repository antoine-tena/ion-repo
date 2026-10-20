"""`kiln score` (T-46): any repo measured against the grid, the same number twice, nothing
written, waivers apart, and what the grid does not know listed."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from kiln import cli
from kiln.grid import score

SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"
GOOD = {
    "README.md": "# a\n",
    "pyproject.toml": "[tool.ruff]\nline-length = 100\n\n[tool.mypy]\nstrict = true\n",
    "tests/test_app.py": "def test_app() -> None: ...\n",
    "AGENTS.md": "# a\n\n## Repo map\n",
    ".github/workflows/ci.yml": "permissions: {}\njobs:\n  a:\n    steps:\n"
    f"      - uses: actions/checkout@{SHA}\n      - run: uv run ruff check && uv run pytest\n"
    "      - run: uvx pip-audit && gitleaks detect\n",
    ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: uv\n"
    "    cooldown:\n      default-days: 7\n",
}


def make(root: Path, files: dict[str, str]) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    return root


def statuses(report: score.Report) -> dict[str, str]:
    return {found.rule: found.status for found in report.findings}


def test_a_repo_that_follows_every_rule_that_applies_scores_100(tmp_path: Path) -> None:
    report = score.score_repo(make(tmp_path, GOOD))

    assert report.score == 100, [found for found in report.findings if found.status == "fail"]
    # Rules of stacks the repo does not have are not even listed.
    assert "DJANGO-DEBUG-OFF" not in statuses(report)
    assert report.pillars["slimming"] is None


def test_gaps_lower_the_score_and_the_cheapest_come_first(tmp_path: Path) -> None:
    files = {**GOOD, ".github/workflows/ci.yml": "jobs:\n  a:\n    steps:\n      - run: pytest\n"}
    report = score.score_repo(make(tmp_path, files))

    assert report.score is not None and report.score < 100
    gaps = {found.rule for found in report.gaps}
    assert {"WORKFLOW-PERMISSIONS", "LINT-IN-CI", "SECRET-SCAN"} <= gaps
    assert len(report.top_gaps()) == score.TOP_GAPS
    assert report.top_gaps()[0].rule in gaps


def test_the_same_repo_gets_the_same_score_and_nothing_is_written(tmp_path: Path) -> None:
    root = make(tmp_path, {"app.py": "try:\n    pass\nexcept:\n    pass\n"})
    before = sorted(path.name for path in root.rglob("*"))

    first, second = score.score_repo(root), score.score_repo(root)

    assert first == second
    assert sorted(path.name for path in root.rglob("*")) == before


def test_a_waived_gap_is_shown_apart_and_not_counted(tmp_path: Path) -> None:
    root = make(tmp_path, {**GOOD, "app.py": "try:\n    pass\nexcept:\n    pass\n"})
    assert statuses(score.score_repo(root))["BARE-EXCEPT"] == "fail"
    (root / "kiln-waivers.toml").write_text(
        '[[waiver]]\nrule = "BARE-EXCEPT"\nreason = "legacy scripts"\nby = "a"\n'
        'since = 2026-10-20\nuntil = "never"\n'
    )

    report = score.score_repo(root)

    assert statuses(report)["BARE-EXCEPT"] == "waived"
    assert report.score == 100


def test_stacks_the_grid_does_not_cover_are_listed(tmp_path: Path) -> None:
    report = score.score_repo(make(tmp_path, {**GOOD, "api/composer.json": "{}"}))

    assert report.uncovered == ("PHP: not covered by the grid yet",)


def test_json_badge_and_screen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, {**GOOD, "app.py": "import os  # noqa\n"})
    monkeypatch.setattr(sys, "argv", ["kiln", "score", str(root), "--json"])
    cli.main()
    data = json.loads(capsys.readouterr().out)
    assert data["schema"] == score.SCHEMA and data["top_gaps"] == ["NOQA-CODES"]
    assert {"rule", "status", "why", "source", "fix", "locations"} <= set(data["findings"][0])

    monkeypatch.setattr(sys, "argv", ["kiln", "score", str(root), "--badge"])
    cli.main()
    assert "img.shields.io/badge/kiln_score-" in capsys.readouterr().out

    monkeypatch.setattr(sys, "argv", ["kiln", "score", str(root)])
    cli.main()
    screen = capsys.readouterr().out
    assert "kiln score" in screen and "NOQA-CODES" in screen and "app.py:1" in screen


def test_a_missing_folder_is_said(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kiln", "score", str(tmp_path / "nowhere")])
    with pytest.raises(SystemExit):
        cli.main()
    assert "no folder" in capsys.readouterr().err
