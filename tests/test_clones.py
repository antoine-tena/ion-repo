"""`ion repo clones`: the branch's new duplicated code, the copy beside its original."""

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from ion_repo import clones
from ion_repo.shell import KilnError


def _side(name: str, start: int, end: int) -> dict[str, Any]:
    return {"name": name, "start": start, "end": end}


REPORT = {
    "duplicates": [
        {
            "firstFile": _side("app/Access.vue", 2, 25),
            "secondFile": _side("app/Demo.vue", 2, 25),
            "kind": "renamed",
            "isNew": True,
        },
        {
            "firstFile": _side("app/old.py", 1, 9),
            "secondFile": _side("app/older.py", 3, 11),
            "kind": "exact",
            "isNew": False,
        },
    ]
}


def _fake_jscpd(
    monkeypatch: pytest.MonkeyPatch, report: dict[str, Any] | None, calls: list[list[str]]
) -> None:
    def run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if report is None:
            return subprocess.CompletedProcess(command, 2, "", "bad ref")
        output = Path(command[command.index("--output") + 1])
        (output / clones.REPORT).write_text(json.dumps(report), encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(clones, "require_tools", lambda *_: None)
    monkeypatch.setattr(clones, "changed_files", lambda _root: ["app/Demo.vue"])


def test_only_new_clones_show_the_copy_before_its_original(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []
    _fake_jscpd(monkeypatch, REPORT, calls)
    found = clones.new_clones(tmp_path, base="abc123")
    assert [clone.line() for clone in found] == [
        "app/Demo.vue:2-25 ← app/Access.vue:2-25 (renamed)"
    ]
    command = calls[0]
    assert command[:4] == ["uvx", "--from", clones.JSCPD, "jscpd"]
    assert command[command.index("--baseline-from-ref") + 1] == "abc123"
    assert "--ignore-identifiers" in command


def test_a_repo_config_adds_its_ignores_to_the_defaults(tmp_path: Path) -> None:
    (tmp_path / clones.CONFIG).write_text(
        json.dumps({"ignore": ["**/fixtures/**", "**/*.json"]}), encoding="utf-8"
    )
    patterns = clones.ignored(tmp_path)
    assert patterns[: len(clones.IGNORED)] == list(clones.IGNORED)
    assert patterns[len(clones.IGNORED) :] == ["**/fixtures/**"]


def test_jscpd_failing_is_an_error_not_an_empty_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fake_jscpd(monkeypatch, None, [])
    with pytest.raises(KilnError, match="bad ref"):
        clones.new_clones(tmp_path, base="nowhere")


def test_no_new_clone_says_so(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _fake_jscpd(monkeypatch, {"duplicates": []}, [])
    clones.clones(tmp_path, base="abc123")
    printed = capsys.readouterr()
    assert "No new duplicated code" in printed.out + printed.err
