"""`ion repo eval-skills`: the cases it picks, the command it builds, the three ok it waits for."""

import sys
from pathlib import Path

import pytest

from ion_repo import eval_skills
from ion_repo.shell import KilnError

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def no_launch(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    """Records what would have been run: no Claude session starts from a test."""
    launched: list[list[str]] = []

    monkeypatch.setattr(eval_skills, "launch", lambda command, _: launched.append(command))
    return launched


def test_every_case_is_tagged_with_a_skill_or_none() -> None:
    skills = {path.name for path in (ROOT / eval_skills.SKILLS).iterdir() if path.is_dir()}
    cases = eval_skills.case_tags(ROOT / eval_skills.EVALS)

    assert len(cases) == 13
    for name, tags in cases.items():
        assert "trigger" in tags
        own = set(tags) - {"trigger"}
        assert own == {eval_skills.NEGATIVE_TAG} or (own == {name} and name in skills), name


def test_command_locks_runs_ablation_concurrency_model_and_publishing() -> None:
    command = eval_skills.eval_command(["pause", "none"], 1.5)

    joined = " ".join(command)
    for locked in (
        "--runs 1",
        "--ablation none",
        "-j 1",
        "--model opus",
        "--max-cost-usd 1.5",
        "--no-publish",
    ):
        assert locked in joined
    assert command[-3:] == ["--tag", "pause", "none"]


def test_dry_run_shows_the_session_count_and_starts_nothing(
    no_launch: list[list[str]], capsys: pytest.CaptureFixture[str]
) -> None:
    eval_skills.eval_skills(ROOT, ["pause"], dry_run=True)

    out = capsys.readouterr().out
    assert "Cases: none-for-loop, none-rename, pause" in out
    assert "Sessions: 3 opus" in out
    assert no_launch == []


def test_without_a_terminal_nothing_starts(
    no_launch: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)

    with pytest.raises(KilnError, match="in a terminal"):
        eval_skills.eval_skills(ROOT, ["pause"])
    assert no_launch == []


def test_anything_but_three_ok_starts_nothing(
    no_launch: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    answers = iter(["ok", "ok", "oui"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    with pytest.raises(KilnError, match="nothing was started"):
        eval_skills.eval_skills(ROOT, ["pause"])
    assert no_launch == []


def test_three_ok_start_the_eval(
    no_launch: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: "ok")

    eval_skills.eval_skills(ROOT, ["pause"])

    assert len(no_launch) == 1
    assert no_launch[0][:4] == ["claude", "plugin", "eval", "plugins/repo"]
