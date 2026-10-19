"""The few questions `kiln new` asks: what you are building, its size, the team's language.

Everything else takes its default (the stack follows from what you are building) or comes from
an option; `kiln new --all-questions` asks the whole Copier questionnaire instead. The choices
repeat those of `copier.yml`, which a test keeps in step.
"""

import os
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from kiln import ui


@dataclass(frozen=True)
class Question:
    key: str
    prompt: str
    choices: tuple[tuple[str, str], ...]  # (label, value)
    default: str


PROJECT_TYPE = Question(
    "project_type",
    "What are you building?",
    (
        ("A full app (API and web interface)", "app"),
        ("An API only", "api"),
        ("A content site (showcase, documentation, blog)", "site"),
        ("A data dashboard", "dashboard"),
        ("A data analysis (notebooks, figures)", "analysis"),
        ("A command-line tool (script, workstation utility)", "cli"),
    ),
    "app",
)
SIZE = Question(
    "size",
    "How hot does this one burn?",
    (
        ("Spark: a script, a personal tool, a one-off analysis", "spark"),
        ("Ember: a small app or site, one or two people, low stakes", "ember"),
        ("Flame: an app in production, real users, several contributors", "flame"),
        ("Blaze: several teams or services, high stakes", "blaze"),
    ),
    "ember",
)
LANGUAGE = Question(
    "language", "Language of the team?", (("English", "en"), ("Français", "fr")), "en"
)
ESSENTIALS = (PROJECT_TYPE, SIZE, LANGUAGE)
# The stack chosen by option: what you are building would only suggest it.
STACK_KEYS = ("backend", "frontend")


def default_language() -> str:
    return "fr" if os.environ.get("LANG", "").startswith("fr") else LANGUAGE.default


def ask_essentials(
    answers: Mapping[str, object], ask: Callable[[str], str] = input
) -> dict[str, object]:
    """The answers completed by the essential questions they leave open; none outside a
    terminal, where the defaults apply."""
    completed = dict(answers)
    if not sys.stdin.isatty():
        return completed
    for question in ESSENTIALS:
        if question.key in completed:
            continue
        if question is PROJECT_TYPE and any(key in completed for key in STACK_KEYS):
            continue
        default = default_language() if question is LANGUAGE else question.default
        completed[question.key] = choose(question, default, ask)
    return completed


def choose(question: Question, default: str, ask: Callable[[str], str] = input) -> str:
    """A numbered menu; Enter takes the default, a number or a value picks a choice."""
    values = [value for _, value in question.choices]
    print(f"\n{ui.paint(question.prompt, bold=True)}")
    for number, (label, value) in enumerate(question.choices, start=1):
        mark = ui.paint("  (default)", ui.STONE) if value == default else ""
        print(f"  {ui.paint(str(number), ui.FIRE)}  {label}{mark}")
    while True:
        reply = ask(f"Choice [{values.index(default) + 1}]: ").strip().lower()
        if not reply:
            return default
        if reply.isdigit() and 1 <= int(reply) <= len(values):
            return values[int(reply) - 1]
        if reply in values:
            return reply
        print(f"A number from 1 to {len(values)}, or one of: {', '.join(values)}.")
