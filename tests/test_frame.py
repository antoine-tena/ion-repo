"""`kiln frame`: the two rules of a Keramos skill answer, at the terminal's width less 6."""

from collections.abc import Iterator

import pytest

from ion_repo import frame


def printed(capsys: pytest.CaptureFixture[str]) -> list[str]:
    return capsys.readouterr().out.splitlines()


def test_given_width_sets_both_lines(capsys: pytest.CaptureFixture[str]) -> None:
    frame.frame("grog", "summary", 60)

    head, foot = printed(capsys)
    assert head == "══ ◆ keramos · grog " + "═" * 40
    assert foot == "═" * 43 + " /grog:summary ══"
    assert len(head) == len(foot) == 60


def test_terminal_width_less_the_margin(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(frame, "terminal_columns", lambda: 125)

    frame.frame("kiln", "merge")

    assert [len(line) for line in printed(capsys)] == [119, 119]


def test_no_terminal_among_the_ancestors_falls_back_to_80(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def no_terminal() -> Iterator[str]:
        yield from ()

    monkeypatch.setattr(frame, "_ancestor_terminals", no_terminal)

    frame.frame("hearth", "domain")

    head, foot = printed(capsys)
    assert len(head) == len(foot) == 74
    assert head.startswith("══ ◆ keramos · hearth ═")
    assert foot.endswith("═ /hearth:domain ══")


def test_an_unreadable_terminal_is_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(frame, "_ancestor_terminals", lambda: iter(["/dev/pts/no-such"]))

    assert frame.terminal_columns() == frame.FALLBACK_COLUMNS


def test_too_narrow_keeps_a_few_rules() -> None:
    head, foot = frame.rules("kiln", "good-first-issues", 10)

    assert head.endswith(" ═══")
    assert foot.startswith("═══ ")
