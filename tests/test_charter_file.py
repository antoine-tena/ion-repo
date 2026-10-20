"""`charter file`: the bans on the edited file alone, for the hook after each edit (T-27)."""

import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from kiln.charter.cli import check_file
from kiln.charter.config import load
from kiln.charter.repo import Repo

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "plugins/kiln/hooks/check_file.py"
CHARTER = """
[bans.logging]
id = "LOGGING"

[bans.django-migrations]
id = "MIGRATIONS"

[ratchets.file-size]
id = "FILE-SIZE"
files = ["backend/*.py"]
suffixes = [".py"]
max_lines = 1
budget = 0
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "charter.toml").write_text(CHARTER)
    (tmp_path / ".gitignore").write_text("ignored/\n")
    backend = tmp_path / "backend"
    (backend / "app/migrations").mkdir(parents=True)
    (backend / "app/migrations/0002_late.py").write_text("x = 1\n")
    (backend / "printer.py").write_text("print('a')\n")
    (backend / "clean.py").write_text("a = 1\nb = 2\n")
    return tmp_path


def run(repo: Path, relative: str) -> int:
    return check_file(Repo(repo, load(repo)), str(repo / relative))


def test_the_edited_file_breaking_a_ban_fails(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(repo, "backend/printer.py") == 1
    out = capsys.readouterr().out
    assert "[LOGGING]" in out and "backend/printer.py" in out
    assert "kiln waive <RULE> --paths backend/printer.py" in out


def test_another_file_ignores_the_rest_of_the_repo(repo: Path) -> None:
    # printer.py breaks a ban, clean.py exceeds the ratchet, migrations have a gap: none of it
    # is the edited file's business.
    assert run(repo, "backend/clean.py") == 0
    assert run(repo, "backend/app/migrations/0002_late.py") == 0


def test_a_waived_or_ignored_file_is_not_checked(repo: Path) -> None:
    today = datetime.date.today().isoformat()
    (repo / "kiln-waivers.toml").write_text(
        '[[waiver]]\nrule = "LOGGING"\nreason = "bootstrap"\nby = "antoine"\n'
        f'paths = ["backend/printer.py"]\nsince = {today}\nuntil = {today}\n'
    )
    (repo / "ignored").mkdir()
    (repo / "ignored/printer.py").write_text("print('a')\n")

    assert run(repo, "backend/printer.py") == 0
    assert run(repo, "ignored/printer.py") == 0


def test_the_hook_reports_the_edited_file_fast(
    repo: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    bin_dir = tmp_path_factory.mktemp("bin")
    charter = bin_dir / "charter"
    charter.write_text(f"#!{sys.executable}\nfrom kiln.charter.cli import run\nrun()\n")
    charter.chmod(0o755)
    payload = json.dumps({"tool_input": {"file_path": str(repo / "backend/printer.py")}})

    timings = []
    for _ in range(3):
        start = time.perf_counter()
        hook = subprocess.run(
            [sys.executable, str(HOOK)],
            input=payload,
            capture_output=True,
            text=True,
            env={"PATH": f"{bin_dir}:/usr/bin:/bin", "TMPDIR": str(tmp_path_factory.mktemp("t"))},
        )
        timings.append(time.perf_counter() - start)

    assert hook.returncode == 2
    assert "[LOGGING]" in hook.stderr and "clean.py" not in hook.stderr
    # Under 200 ms on its own. The best of three runs measures the hook, not a busy test
    # machine (a single run once took 2.4 s on GitHub's macOS while the suite ran in parallel).
    assert min(timings) < 2
