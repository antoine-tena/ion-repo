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
    assert session.find_ticket(shop, "shop#T-07").branch == "chore/t07-write-season-guide"
    assert session.find_ticket(shop, "T-07").effort == "medium"


def test_branch_says_what_it_is_in_ascii_and_short() -> None:
    block = "- **Type**: bug\n- **Effort**: XS"
    title = "Intitulés de modules abîmés dans les jeux de données"

    branch = session._ticket("learnagement#T-15", 15, title, block).branch

    assert branch == "fix/t15-intitules-modules-abimes-jeux-donnees"


def test_line_names_the_session_and_sends_it_to_the_ticket(shop: Path) -> None:
    line = session.command(shop, ["T-06"])

    assert line.startswith(
        "cd ~/code/shop && claude --model sonnet --effort low"
        " --name 'shop#T-06_free-registrations-can-cancelled' 'Work on shop#T-06"
    )
    worktree = "/repo:worktree fix/t06-free-registrations-can-cancelled,"
    assert f"{worktree} then /repo:backlog start shop#T-06" in line
    assert "/repo:merge" in line


def test_several_tickets_take_the_highest_effort_and_the_notes(shop: Path) -> None:
    line = session.command(shop, ["T-06", "T-05"], notes=["Leave the buyer's cart alone."])

    assert "--effort high --name 'shop#T-06 shop#T-05' " in line
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


@pytest.fixture
def shop_folder(shop: Path) -> Path:
    """The same backlog, split into a folder: one file per ticket."""
    from ion_repo.backlog import split_into_folder

    (shop / ".copier-answers.yml").write_text("name: shop\n")
    assert split_into_folder(shop)
    return shop


def test_a_ticket_file_is_read_and_cited_by_the_prompt(shop_folder: Path) -> None:
    ticket = session.find_ticket(shop_folder, "T-05")
    assert (ticket.effort, ticket.branch) == ("high", "fix/two-coaches")
    assert session.find_ticket(shop_folder, "T-07").effort == "medium"

    line = session.command(shop_folder, ["T-06"])

    assert "Work on shop#T-06 (Free registrations can be cancelled) from" in line
    assert " docs/backlog/tickets/shop-T-06.md." in line
    with pytest.raises(KilnError, match=r"closed, see docs/backlog/done\.md"):
        session.find_ticket(shop_folder, "T-04")


def test_session_line_names_the_model_effort_and_branch() -> None:
    block = "- **Type**: task\n- **Effort**: L\n- **Session**: opus xhigh, feat/the-whole-thing\n"

    one = session._ticket("shop#T-09", 9, "Whole thing", block)

    assert (one.model, one.effort, one.branch) == ("opus", "xhigh", "feat/the-whole-thing")


def test_session_line_without_a_model_is_sonnet_and_the_former_form_still_reads() -> None:
    bare = session._ticket("shop#T-09", 9, "A", "- **Effort**: S\n- **Session**: high\n")
    former = session._ticket("shop#T-09", 9, "A", "- **Effort**: S · **Session**: high, fix/a\n")

    assert (bare.model, bare.effort) == ("sonnet", "high")
    assert (former.model, former.effort, former.branch) == ("sonnet", "high", "fix/a")


def test_the_line_takes_the_model_of_its_session(shop_folder: Path) -> None:
    ticket_file = shop_folder / "docs/backlog/tickets/shop-T-06.md"
    ticket_file.write_text(
        ticket_file.read_text().replace("- **Opened**", "- **Session**: opus high\n- **Opened**")
    )

    assert " --model opus --effort high " in session.command(shop_folder, ["T-06"])
    assert " --model sonnet --effort high " in session.command(shop_folder, ["T-07"], effort="high")


def test_subagent_brief_sends_to_the_ticket_and_neither_merges_nor_asks(shop_folder: Path) -> None:
    text = session.brief(shop_folder, "T-06", notes=["T-05 edits the same page."])

    assert "shop#T-06 · Free registrations can be cancelled" in text
    assert "Session: sonnet, effort low." in text
    assert f"{Path.home() / 'code/shop'}/docs/backlog/tickets/shop-T-06.md" in text
    assert "/repo:worktree fix/t06-free-registrations-can-cancelled" in text
    assert "Note: T-05 edits the same page." in text
    assert "/repo:merge" not in text and "Ask the user" not in text
    assert text.splitlines()[-1].endswith("deviations from the ticket, questions for the user.")


def test_subagent_takes_one_ticket(shop_folder: Path) -> None:
    with pytest.raises(KilnError, match="one ticket"):
        session.session(shop_folder, ["T-05", "T-06"], subagent=True)
