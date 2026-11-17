"""`ion repo pause` without a name: names proposed from the work at hand."""

import subprocess
from pathlib import Path

from ion_repo.pause import suggested_names


def git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)


def test_names_come_from_branch_tickets_and_last_commit(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "-b", "develop")
    backlog = tmp_path / "docs" / "backlog" / "backlog.md"
    backlog.parent.mkdir(parents=True)
    backlog.write_text(
        "### T-12 · Done one\n- **Status**: todo\n"
        "### acme#T-13 · The pause names\n"
        "- **Status**: in progress — branch feat/x, since 2026-10-26\n"
    )
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "feat: first")
    assert suggested_names(tmp_path) == ["acme#T-13: The pause names", "feat: first"]
    git(tmp_path, "switch", "-q", "-c", "feat/pause-names")
    assert suggested_names(tmp_path)[0] == "pause names"


def test_tickets_in_progress_are_read_from_the_folder(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "-b", "develop")
    tickets = tmp_path / "docs/backlog/tickets"
    tickets.mkdir(parents=True)
    (tickets / "acme-T-12.md").write_text("# acme#T-12 · Waiting\n- **Status**: todo\n")
    (tickets / "acme-T-13.md").write_text(
        "# acme#T-13 · The pause names\n"
        "- **Status**: in progress — branch feat/x, since 2026-10-26\n"
    )
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "feat: first")
    assert suggested_names(tmp_path) == ["acme#T-13: The pause names", "feat: first"]
