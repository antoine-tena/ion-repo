"""Releases by name and tickets that say their release (ion-repo#T-456): read, drawn, migrated."""

import subprocess
from pathlib import Path

import pytest

from ion_repo import backlog_map, release_files, tracker
from ion_repo.shell import KilnError

TICKET = """# acme#T-{number:02d} · {title}
- **Type**: task
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-20
- **Effort**: {size} · **Owner**: — · **Due**: —{session}
- **Origin**: test

Details.
"""
OLD_THREE = """# v0.2.0 · Fast checks

Why: the checks wait for nobody.
- acme#T-01 · First (S) · low · `ion repo session acme#T-01`
- acme#T-02 · Second (M) · medium · `ion repo session acme#T-02`
- acme#T-77 · Closed since (S) · low · `ion repo session acme#T-77`
- other#T-05 · Another repo's (S)
- Browser checks: acme#T-03
"""
OLD_FIRST = "# v0.1.0 · Fast checks, first part\n\nThe first part.\n- acme#T-03 · Third (S) · low\n"
README = """# Backlog

**Next free: acme#T-04.**

## Releases

- [v0.1.0 · Fast checks, first part](releases/v0.1.0.md)
- [v0.2.0 · Fast checks](releases/v0.2.0.md)

The plan's notes and what shipped: [releases/](releases/README.md).
"""


def write(root: Path, relative: str, text: str) -> None:
    (root / relative).parent.mkdir(parents=True, exist_ok=True)
    (root / relative).write_text(text)


@pytest.fixture
def acme(tmp_path: Path) -> Path:
    write(tmp_path, ".copier-answers.yml", "name: acme\n")
    write(tmp_path, "docs/backlog/README.md", README)
    write(tmp_path, "docs/backlog/releases/README.md", "# Releases\n\nNotes.\n")
    write(tmp_path, "docs/backlog/releases/v0.2.0.md", OLD_THREE)
    write(tmp_path, "docs/backlog/releases/v0.1.0.md", OLD_FIRST)
    write(tmp_path, "docs/backlog/tickets/acme-T-01-first.md", TICKET.format(
        number=1, title="First", size="S", session=" · **Session**: high, fix/first"
    ))  # fmt: skip
    for number, title, size in ((2, "Second", "M"), (3, "Third", "S")):
        text = TICKET.format(number=number, title=title, size=size, session="")
        write(tmp_path, f"docs/backlog/tickets/acme-T-{number:02d}-{title.lower()}.md", text)
    write(tmp_path, "docs/backlog/tickets/acme-T-09-loose.md", TICKET.format(
        number=9, title="Loose", size="XS", session=""
    ))  # fmt: skip
    return tmp_path


def placed(root: Path) -> dict[str, list[str]]:
    return {
        one.name: [line.split(" · ")[0] for line in one.tickets] for one in tracker.releases(root)
    }


def test_the_migration_changes_nothing_a_reader_sees(acme: Path) -> None:
    before = placed(acme)
    versions = [one.version for one in tracker.releases(acme)]

    notes = release_files.migrate(acme)

    assert len(notes) == 2
    assert versions == ["0.1.0", "0.2.0"]
    after = placed(acme)
    before["v0.2.0"].remove("acme#T-77")  # a closed ticket leaves the plan
    assert list(after.values()) == list(before.values())
    assert [one.version for one in tracker.releases(acme)] == versions


def test_a_release_takes_the_slug_of_its_title_and_loses_its_ticket_lines(acme: Path) -> None:
    release_files.migrate(acme)

    folder = acme / "docs/backlog/releases"
    assert sorted(path.name for path in folder.glob("*.md")) == [
        "README.md",
        "fast-checks-first-part.md",
        "fast-checks.md",
    ]
    assert (folder / "fast-checks.md").read_text() == (
        "# Fast checks\n- **Version**: v0.2.0\n\nWhy: the checks wait for nobody.\n"
        "- other#T-05 · Another repo's (S)\n- Browser checks: acme#T-03\n"
    )


def test_each_listed_ticket_names_its_release_before_its_origin(acme: Path) -> None:
    release_files.migrate(acme)

    second = (acme / "docs/backlog/tickets/acme-T-02-second.md").read_text()
    assert "- **Release**: fast-checks\n- **Origin**: test" in second
    third = tracker.find(acme, 3)
    assert third is not None and third.release == "fast-checks-first-part"
    loose = tracker.find(acme, 9)
    assert loose is not None and loose.release == ""


def test_the_former_session_field_gets_its_own_line(acme: Path) -> None:
    release_files.migrate(acme)

    first = (acme / "docs/backlog/tickets/acme-T-01-first.md").read_text()
    assert (
        "- **Effort**: S · **Owner**: — · **Due**: —\n- **Session**: sonnet high, fix/first\n"
        in first
    )
    assert "· **Session**" not in first


def test_the_index_points_to_the_command_instead_of_listing_releases(acme: Path) -> None:
    release_files.migrate(acme)

    index = (acme / "docs/backlog/README.md").read_text()
    assert "releases/v0" not in index
    assert "## Releases\n\nPlanned releases and their tickets: `ion repo backlog`.\n" in index
    assert "[releases/](releases/README.md)" in index


def test_links_to_a_renamed_release_follow(acme: Path) -> None:
    write(acme, "docs/backlog/done.md", "See [it](releases/v0.2.0.md) and releases/v0.2.0.md.\n")

    release_files.migrate(acme)

    assert (acme / "docs/backlog/done.md").read_text() == (
        "See [it](releases/fast-checks.md) and releases/fast-checks.md.\n"
    )


def test_a_second_run_changes_nothing(acme: Path) -> None:
    release_files.migrate(acme)
    snapshot = {path: path.read_text() for path in (acme / "docs").rglob("*.md")}

    assert release_files.migrate(acme) == []
    assert {path: path.read_text() for path in (acme / "docs").rglob("*.md")} == snapshot


def test_two_releases_with_the_same_title_words_get_more_words_not_a_number(
    acme: Path,
) -> None:
    write(acme, "docs/backlog/releases/v0.3.0.md", "# v0.3.0 · Fast checks: the second part\n")
    write(acme, "docs/backlog/releases/v0.4.0.md", "# v0.4.0 · Fast checks: the third part\n")

    release_files.migrate(acme)

    names = sorted(path.stem for path in (acme / "docs/backlog/releases").glob("*.md"))
    assert "fast-checks-second-part" in names and "fast-checks-third-part" in names


def test_a_ticket_listed_twice_stays_in_the_earliest_release(acme: Path) -> None:
    write(acme, "docs/backlog/releases/v0.3.0.md", "# v0.3.0 · Later\n- acme#T-03 · Third (S)\n")

    release_files.migrate(acme)

    assert placed(acme)["later"] == []
    assert placed(acme)["fast-checks-first-part"] == ["acme#T-03"]


def test_the_map_lists_releases_in_version_order_then_the_unplanned(acme: Path) -> None:
    release_files.migrate(acme)
    write(acme, "docs/backlog/tickets/acme-T-02-second.md", (
        acme / "docs/backlog/tickets/acme-T-02-second.md"
    ).read_text().replace(
        "- **Origin**", "- **Touches**: backend/events, migration yes\n- **Origin**"
    ))  # fmt: skip

    lines = backlog_map.draw(acme)

    assert lines == [
        "Production: unknown (no tag on main)",
        "",
        "v0.1.0 · fast-checks-first-part · Fast checks, first part",
        "  acme#T-03 · 🟡 todo · S · sonnet low · — · Third",
        "",
        "v0.2.0 · fast-checks · Fast checks",
        "  acme#T-01 · 🟡 todo · S · sonnet high · — · First",
        "  acme#T-02 · 🟡 todo · M · sonnet medium · backend/events, migration yes · Second",
        "",
        "Unplanned",
        "  acme#T-09 · 🟡 todo · XS · sonnet low · — · Loose",
    ]


def test_the_map_of_one_release_by_name_or_version(acme: Path) -> None:
    release_files.migrate(acme)

    assert backlog_map.draw(acme, "fast-checks") == backlog_map.draw(acme, "v0.2.0")[:]
    assert backlog_map.draw(acme, "0.2.0")[0].startswith("v0.2.0 · fast-checks")
    with pytest.raises(KilnError, match="no such release"):
        backlog_map.draw(acme, "nowhere")


def test_a_ticket_naming_a_missing_release_is_flagged_not_lost(acme: Path) -> None:
    release_files.migrate(acme)
    loose = acme / "docs/backlog/tickets/acme-T-09-loose.md"
    loose.write_text(loose.read_text().replace("- **Origin**", "- **Release**: typo\n- **Origin**"))

    assert backlog_map.draw(acme)[-1].endswith("Loose · release `typo` not found")


def test_production_is_the_last_tag_of_main(acme: Path) -> None:
    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(acme), *args], check=True, capture_output=True)

    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
    git("tag", "v1.2.3")

    assert backlog_map.draw(acme)[0] == "Production: v1.2.3 (main)"
