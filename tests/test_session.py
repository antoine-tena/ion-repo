"""`ion repo session`: the line that opens a Claude Code session on backlog tickets."""

from pathlib import Path

import pytest

from ion_repo import session
from ion_repo.shell import KilnError

BACKLOG = """# Backlog

**Next free: shop#T-08.**

## 🔴 Critical

### shop#T-05 · Two coaches stay two coaches
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-11-11
- **Effort**: M · **Owner**: — · **Due**: — · **Session**: high, fix/two-coaches
- **Origin**: audit

- [ ] Failing test.

### shop#T-06 · Free registrations can be cancelled
- **Type**: bug
- **Status**: todo
- **Opened**: 2026-11-11
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: the buyer's report

## 🟡 Normal

### shop#T-07 · Write the season's guide
- **Type**: task
- **Status**: todo
- **Opened**: 2026-11-11
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: —
"""


@pytest.fixture
def shop(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "docs/backlog").mkdir(parents=True)
    (tmp_path / "docs/backlog/backlog.md").write_text(BACKLOG)
    (tmp_path / "docs/backlog/done.md").write_text("- **2026-11-10** · shop#T-04 · Old · x\n")
    monkeypatch.setattr(session, "repo_name", lambda root: "shop")
    monkeypatch.setattr(session, "main_tree", lambda root: Path.home() / "code/shop")
    return tmp_path


def test_session_field_gives_effort_and_branch(shop: Path) -> None:
    ticket = session.find_ticket(shop, "T-05")

    assert (ticket.effort, ticket.branch) == ("high", "fix/two-coaches")
    assert ticket.title == "Two coaches stay two coaches"


def test_without_field_size_and_type_decide(shop: Path) -> None:
    assert session.find_ticket(shop, "6").effort == "low"
    assert session.find_ticket(shop, "shop#T-07").branch == "chore/t07"
    assert session.find_ticket(shop, "T-07").effort == "medium"


def test_line_names_the_session_and_sends_it_to_the_ticket(shop: Path) -> None:
    line = session.command(shop, ["T-06"])

    assert line.startswith(
        "cd ~/code/shop && claude --model claude-opus-5-5 --effort low"
        " --name 'T-06 Free registrations can be cancelled' 'Work on shop#T-06"
    )
    assert "/repo:worktree fix/t06, then /repo:backlog start shop#T-06" in line
    assert "/repo:merge" in line


def test_several_tickets_take_the_highest_effort_and_the_notes(shop: Path) -> None:
    line = session.command(shop, ["T-06", "T-05"], notes=["Leave the buyer's cart alone."])

    assert "--effort high --name 'T-06 T-05' " in line
    assert "in that order, one worktree and one merge per ticket" in line
    assert line.endswith("Leave the buyer\u2019s cart alone.'")


def test_effort_given_wins(shop: Path) -> None:
    assert "--effort xhigh " in session.command(shop, ["T-05"], effort="xhigh")


def test_closed_ticket_says_so(shop: Path) -> None:
    with pytest.raises(KilnError, match=r"closed, see docs/backlog/done\.md"):
        session.find_ticket(shop, "T-04")


def test_unknown_ticket_or_id_refused(shop: Path) -> None:
    with pytest.raises(KilnError, match="not an open ticket"):
        session.find_ticket(shop, "T-99")
    with pytest.raises(KilnError, match="not a ticket ID"):
        session.find_ticket(shop, "coaches")
