"""`kiln score` (T-46): any repo measured against the grid, the same number twice, nothing
written, waivers apart, and what the grid does not know listed. `--roadmap` (T-129): what needs
judgment handed to Claude with its places, a false positive dismissed on its path, a gap proven
closed by `--rule`, tickets written once."""

import datetime
import json
import subprocess
import sys
from pathlib import Path

import pytest

from kiln import cli
from kiln.grid import roadmap, score
from kiln.shell import KilnError

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


def test_a_language_not_scored_yet_is_said_beside_the_score(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    files = {**GOOD, "Cargo.toml": "[package]\n", "src/main.rs": "fn main() {}\n"}

    score.show(score.score_repo(make(tmp_path, files)))

    header = capsys.readouterr().out.strip().splitlines()[:4]
    assert any("not scored yet: Rust" in line for line in header)


@pytest.mark.parametrize(
    ("files", "uncovered"),
    [
        ({"App.sln": "", "App/App.csproj": "<Project/>", "App/Main.cs": ""}, ["C# (.NET)"]),
        ({".classpath": "", "src/Main.java": "class Main {}"}, ["Java"]),
        ({"pom.xml": "<project/>", "src/Main.java": "class Main {}"}, ["Java (Maven)"]),
        ({"web/index.php": "<?php"}, ["PHP"]),
    ],
)
def test_a_stack_known_by_its_sources_alone_is_listed(
    tmp_path: Path, files: dict[str, str], uncovered: list[str]
) -> None:
    report = score.score_repo(make(tmp_path, {**GOOD, **files}))

    assert report.uncovered == tuple(f"{stack}: not covered by the grid yet" for stack in uncovered)


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


def test_the_score_closes_a_screen_long_with_gaps(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # An old repo lists a hundred lines of gaps: its score would scroll out of sight.
    root = make(tmp_path, {**GOOD, "app.py": "import os  # noqa\n"})
    report = score.score_repo(root)
    score.show(report)
    last = capsys.readouterr().out.rstrip().splitlines()[-1]
    assert f"{report.score}/100" in last and "1 gap" in last

    score.show(score.score_repo(make(tmp_path / "good", GOOD)))
    assert "gap" not in capsys.readouterr().out.rstrip().splitlines()[-1]


def test_a_missing_folder_is_said(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kiln", "score", str(tmp_path / "nowhere")])
    with pytest.raises(SystemExit):
        cli.main()
    assert "no folder" in capsys.readouterr().err


# --- the roadmap ---

LEGACY = {
    **GOOD,
    "app.py": "try:\n    pass\nexcept:\n    pass\n",
    "db.py": 'def find(cursor, name):\n    cursor.execute(f"SELECT * FROM t WHERE n = {name}")\n',
}
BACKLOG = """# Backlog

**Next free: T-07.**

## 🟡 Normal

## ✅ Done
"""


def test_the_roadmap_leaves_scripts_out_and_puts_sure_gaps_first(tmp_path: Path) -> None:
    report = score.score_repo(make(tmp_path, LEGACY))

    items = report.roadmap()

    assert all(not found.by_script for found in items)
    assert [found.rule for found in items].index("BARE-EXCEPT") < [
        found.rule for found in items
    ].index("SQL-PARAMETERS")
    sql = next(found for found in items if found.rule == "SQL-PARAMETERS")
    assert sql.confirm and sql.locations == ("db.py:2",)


def test_a_false_positive_dismissed_on_its_path_is_never_flagged_again(tmp_path: Path) -> None:
    root = make(tmp_path, LEGACY)
    (root / "kiln-waivers.toml").write_text(
        '[[waiver]]\nrule = "SQL-PARAMETERS"\npaths = ["db.py"]\n'
        'reason = "false positive: a constant"\nby = "a"\nsince = 2026-10-20\nuntil = "never"\n'
    )

    found = score.rule_finding(score.score_repo(root), "SQL-PARAMETERS")

    assert found is not None and found.status == "waived"


def test_rule_fails_while_the_gap_is_open_and_passes_once_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, LEGACY)
    report = score.score_repo(root)
    with pytest.raises(KilnError, match="BARE-EXCEPT still open"):
        roadmap.show_rule(report, score.rule_finding(report, "BARE-EXCEPT"), "BARE-EXCEPT")

    (root / "app.py").write_text("try:\n    pass\nexcept ValueError:\n    pass\n")
    report = score.score_repo(root)
    roadmap.show_rule(report, score.rule_finding(report, "BARE-EXCEPT"), "BARE-EXCEPT")

    assert "BARE-EXCEPT: pass" in capsys.readouterr().out


def test_write_turns_items_into_tickets_once(tmp_path: Path) -> None:
    root = make(tmp_path, {**LEGACY, "docs/backlog/backlog.md": BACKLOG})
    report = score.score_repo(root)
    today = datetime.date(2026, 10, 21)

    written = roadmap.write_tickets(root, report, today)
    again = roadmap.write_tickets(root, report, today)

    text = (root / roadmap.BACKLOG).read_text()
    assert written[0] == "T-07" and again == []
    assert f"Next free: T-{7 + len(written):02d}" in text
    assert "grid rule `BARE-EXCEPT`" in text and "- [ ] `app.py:3`" in text
    assert text.index("### T-07") > text.index("## 🟡 Normal") > 0


def test_without_a_backlog_write_says_how_to_get_one(tmp_path: Path) -> None:
    root = make(tmp_path, LEGACY)

    with pytest.raises(KilnError, match="kiln adopt"):
        roadmap.write_tickets(root, score.score_repo(root))
