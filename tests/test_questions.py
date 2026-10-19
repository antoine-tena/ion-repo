import io
import sys
from pathlib import Path

import pytest
import yaml

from kiln import questions

COPIER = yaml.safe_load((Path(__file__).parents[1] / "copier.yml").read_text())


@pytest.mark.parametrize("question", questions.ESSENTIALS, ids=lambda q: q.key)
def test_the_choices_are_those_of_the_template(question: questions.Question) -> None:
    declared = COPIER[question.key]

    assert tuple(declared["choices"].items()) == question.choices
    assert declared["default"] == question.default


def test_enter_takes_the_default_and_a_number_or_a_value_picks(
    capsys: pytest.CaptureFixture[str],
) -> None:
    given = iter(["", "3", "blaze", "9", "spark"])

    def ask(_: str) -> str:
        return next(given)

    assert questions.choose(questions.SIZE, "ember", ask) == "ember"
    assert questions.choose(questions.SIZE, "ember", ask) == "flame"
    assert questions.choose(questions.SIZE, "ember", ask) == "blaze"
    assert questions.choose(questions.SIZE, "ember", ask) == "spark"
    assert "A number from 1 to 4" in capsys.readouterr().out


def test_only_the_open_questions_are_asked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setenv("LANG", "fr_FR.UTF-8")
    asked: list[str] = []

    def ask(prompt: str) -> str:
        asked.append(prompt)
        return ""

    answers = questions.ask_essentials({"name": "demo", "backend": "fastapi"}, ask)

    # The stack given by option: what you are building is not asked.
    assert answers == {"name": "demo", "backend": "fastapi", "size": "ember", "language": "fr"}
    assert len(asked) == 2


def test_outside_a_terminal_nothing_is_asked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO())

    assert questions.ask_essentials({"name": "demo"}) == {"name": "demo"}
