"""The backlog folder: tickets and releases read the same from a folder or a former single file."""

from pathlib import Path

import pytest
from packaging.version import Version

from ion_repo import backlog_map, tracker
from ion_repo.backlog import split_into_folder
from ion_repo.release import planned_release

SINGLE = """# Backlog

**Next free: acme#T-04.**

## 🚀 Releases

### v0.1.10 · Later
- acme#T-03 · Third (M)

### v0.1.9 · First
Why: the first.
- acme#T-01 · First (S)

## 🔴 Critical

### acme#T-01 · First
- **Type**: bug
- **Status**: in progress — branch fix/t01, since 2026-11-17
- **Opened**: 2026-11-17
- **Effort**: S · **Owner**: @ann · **Due**: —
- **Origin**: —

## 🟡 Normal

### acme#T-03 · Third
- **Type**: task
- **Status**: todo
- **Opened**: 2026-11-17
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: —
"""


@pytest.fixture(params=["single", "folder"])
def acme(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    (tmp_path / "docs/backlog").mkdir(parents=True)
    (tmp_path / "docs/backlog/backlog.md").write_text(SINGLE)
    (tmp_path / ".copier-answers.yml").write_text("name: acme\n")
    if request.param == "folder":
        assert split_into_folder(tmp_path)
    return tmp_path


def test_both_forms_read_the_same(acme: Path) -> None:
    assert [one.ticket_id for one in tracker.open_tickets(acme)] == ["acme#T-01", "acme#T-03"]
    first = tracker.find(acme, 1)
    assert first is not None and first.priority == "critical" and first.field("Owner") == "@ann"
    assert tracker.find(acme, 2) is None
    assert tracker.next_free(acme) == 4
    assert backlog_map.draw(acme) == [
        "Production: unknown (no tag on main)",
        "",
        "v0.1.9 · First",
        "  acme#T-01 · 🔴 in progress · S · sonnet low · — · First",
        "",
        "v0.1.10 · Later",
        "  acme#T-03 · 🟡 todo · M · sonnet medium · — · Third",
    ]


def test_releases_come_in_version_order_with_their_tickets(acme: Path) -> None:
    found = tracker.releases(acme)
    if tracker.is_folder(acme):  # files sort by version, not by name
        assert [one.version for one in found] == ["0.1.9", "0.1.10"]
    first = next(one for one in found if one.version == "0.1.9")
    assert (first.title, first.why, first.tickets) == ("First", "Why: the first.", [
        "acme#T-01 · First (S)"
    ])  # fmt: skip
    assert planned_release(acme, {Version("0.1.9")}) == (
        "0.1.10",
        "Later",
        ["acme#T-03 · Third (M)"],
    )


def test_display_name_follows_the_plan(acme: Path) -> None:
    assert tracker.display_name(acme, "acme", 1, "First") == "acme#T-01_v0.1.9_first"
    assert tracker.display_name(acme, "acme", 9, "Not planned") == "acme#T-09_not-planned"


def test_a_new_ticket_takes_the_next_free_number(tmp_path: Path) -> None:
    (tmp_path / "docs/backlog").mkdir(parents=True)
    (tmp_path / "docs/backlog/README.md").write_text("**Next free: acme#T-09.**\n")

    ticket_id, path = tracker.add_ticket(
        tmp_path, "acme", "Do it", {"Type": "task", "Priority": "important"}, "Why."
    )

    assert ticket_id == "acme#T-09" and path.name == "acme-T-09-do-it.md"
    assert (
        path.read_text()
        == "# acme#T-09 · Do it\n- **Type**: task\n- **Priority**: 🟠 important\n\nWhy.\n"
    )
    assert tracker.next_free(tmp_path) == 10
