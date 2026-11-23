"""Counters of [CONSTANTS]: bare words, durations without a unit, shared homonyms."""

import subprocess
from pathlib import Path

from ion_repo.charter.constants import constant_homonyms, constant_names, constant_units
from ion_repo.charter.repo import Repo

PARAMS = {"files": ["*.py", "*.ts", "*.vue"]}


def _repo(root: Path, files: dict[str, str]) -> Repo:
    for name, text in files.items():
        (root / name).write_text(text)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return Repo(root, {})


def test_bare_words_and_technical_types_are_counted(tmp_path: Path) -> None:
    source = "LABEL = 1\n_SALT = 'a'\nROLE_LIST = []\nROW_GAP = 8\n\ndef f():\n    URL = 1\n"
    vue = "<script setup>\nconst W = 3\nconst BAR_COLORS = {}\n</script>\n"
    count, detail = constant_names(_repo(tmp_path, {"a.py": source, "b.vue": vue}), PARAMS)
    assert count == 4
    assert "b.vue:2  W" in detail


def test_durations_need_a_unit_unless_the_type_carries_it(tmp_path: Path) -> None:
    source = "A_TIMEOUT = 5\nB_TTL_SECONDS = 5\nC_DELAY = timedelta(days=1)\n"
    assert constant_units(_repo(tmp_path, {"a.py": source}), PARAMS)[0] == 1


def test_homonyms_count_only_when_shared(tmp_path: Path) -> None:
    files = {
        "a.py": "ROW_SIZE = 1\nPAGE_SIZE = 1\n",
        "b.py": "ROW_SIZE = 2\nPAGE_SIZE = 2\n",
        "c.py": "from a import ROW_SIZE\nfrom b import ROW_SIZE as other\n",
        "d.ts": "export const ROW_SIZE = 1\n",
    }
    count, detail = constant_homonyms(_repo(tmp_path, files), PARAMS)
    assert count == 2
    assert detail == ["a.py:1  ROW_SIZE", "b.py:1  ROW_SIZE"]
