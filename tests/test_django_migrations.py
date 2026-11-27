"""[MIGRATIONS] numbering: no gap, and a repeated number only when a merge migration follows."""

import subprocess
from pathlib import Path

import pytest

from ion_repo.charter.bans import django_migrations
from ion_repo.charter.repo import Repo

PARAMS = {"files": "backend/**/migrations/*.py"}


def _repo(root: Path, names: list[str]) -> Repo:
    folder = root / "backend/app/migrations"
    folder.mkdir(parents=True)
    for name in ["__init__.py", *names]:
        (folder / name).write_text("x = 1\n")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return Repo(root, {})


@pytest.mark.parametrize(
    "names",
    [
        ["0001_initial.py", "0002_more.py"],
        ["0001_initial.py", "0002_a.py", "0002_b.py", "0003_merge_a_b.py"],
        ["0001_initial.py", "0002_a.py", "0002_b.py", "0003_merge_20261127.py", "0004_next.py"],
    ],
)
def test_sequences_that_pass(tmp_path: Path, names: list[str]) -> None:
    assert django_migrations(_repo(tmp_path, names), PARAMS) == []


@pytest.mark.parametrize(
    "names",
    [
        ["0001_initial.py", "0003_gap.py"],
        ["0001_initial.py", "0002_a.py", "0002_b.py"],
        ["0001_initial.py", "0002_a.py", "0002_b.py", "0003_not_a_merge.py"],
        ["0001_initial.py", "badly_named.py"],
    ],
)
def test_sequences_that_fail(tmp_path: Path, names: list[str]) -> None:
    failures = django_migrations(_repo(tmp_path, names), PARAMS)
    assert failures
    assert "numbered without gaps" in failures[0]
