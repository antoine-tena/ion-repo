"""`charter coverage`: the measure shown never rounds up to the floor it misses."""

from pathlib import Path

import pytest

from ion_repo.charter.python_tools import coverage, truncated
from ion_repo.charter.repo import Repo


def write_report(root: Path, line_rate: float) -> None:
    (root / "coverage.xml").write_text(f'<coverage line-rate="{line_rate}"><packages/></coverage>')


def test_a_measure_under_the_floor_is_not_rounded_up_to_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_report(tmp_path, 0.95965)
    config = {"coverage": {"report": "coverage.xml", "floors": {"TOTAL": 96}}}

    assert coverage(Repo(tmp_path, config)) == 1

    output = capsys.readouterr().out
    assert "TOTAL: 95.96 % of lines covered, under 96 %." in output
    assert "96.0 %" not in output


def test_a_measure_far_above_the_floor_is_truncated_too(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_report(tmp_path, 0.99999)
    config = {"coverage": {"report": "coverage.xml", "floors": {"TOTAL": 90}}}

    assert coverage(Repo(tmp_path, config)) == 0

    assert "TOTAL: 99.99 %: raise" in capsys.readouterr().out


def test_an_exact_value_keeps_its_digits() -> None:
    assert truncated(96.0) == "96.00"
