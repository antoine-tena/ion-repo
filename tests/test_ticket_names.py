"""A ticket's file name carries a slug of its title; `ion repo update` gives one to the others."""

import subprocess
from pathlib import Path

from ion_repo import tracker
from ion_repo.ticket_names import file_name, name_ticket_files, slug


def test_a_slug_keeps_the_words_that_say_the_subject() -> None:
    assert slug("Around the next release: database refactor, migrations") == (
        "around-next-release-database-refactor-migrations"
    )
    assert slug("Découper `events/` (extraire au moins une app `finance/`)") == (
        "decouper-events-extraire-moins-app-finance"
    )
    assert slug("···") == ""


def test_a_title_with_no_word_keeps_the_bare_name() -> None:
    assert file_name("acme", 7, "Do it") == "acme-T-07-do-it.md"
    assert file_name("acme", 7, "!!") == "acme-T-07.md"


def test_bare_ticket_files_get_their_slug_and_links_follow(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    tickets = tmp_path / tracker.TICKETS_DIR
    tickets.mkdir(parents=True)
    (tickets / "acme-T-07.md").write_text("# acme#T-07 · Split the events app\n")
    (tickets / "acme-T-08-kept.md").write_text("# acme#T-08 · Other title\n")
    release = tmp_path / tracker.RELEASES_DIR / "v1.0.0.md"
    release.parent.mkdir(parents=True)
    release.write_text("See [it](../tickets/acme-T-07.md#why) and acme-T-07.mdx.\n")

    assert name_ticket_files(tmp_path) == 1

    assert sorted(path.name for path in tickets.iterdir()) == [
        "acme-T-07-split-events-app.md",
        "acme-T-08-kept.md",
    ]
    assert release.read_text() == (
        "See [it](../tickets/acme-T-07-split-events-app.md#why) and acme-T-07.mdx.\n"
    )
    assert tracker.find(tmp_path, 7) is not None and tracker.find(tmp_path, 8) is not None
    assert name_ticket_files(tmp_path) == 0
