"""Ticket IDs written `<repo>#T-NN`: the prefix comes from the repo's name, only real IDs move,
nothing else of a file does, and a second run has nothing left to do."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from ion_repo import tickets

REPO = Path(__file__).resolve().parent.parent


def repo(tmp_path: Path, name: str = "acme-shop", **files: str) -> Path:
    (tmp_path / ".copier-answers.yml").write_text(f"name: {name}\n")
    (tmp_path / "docs/backlog").mkdir(parents=True)
    for stem, text in files.items():
        (tmp_path / f"docs/backlog/{stem}.md").write_bytes(text.encode())
    return tmp_path


def converted(root: Path, stem: str = "backlog") -> str:
    tickets.write(tickets.plan(root))
    return (root / f"docs/backlog/{stem}.md").read_bytes().decode()


HEAD = "**Next free: T-20.**\n\n### T-01 · One\n\n"


def test_own_ids_take_the_repo_name_everywhere(tmp_path: Path) -> None:
    root = repo(tmp_path, backlog=HEAD + "After T-07, T-186 to T-19 and T-3.\n",
                done="- **2026-01-02** · T-06, T-07 · Closed — after T-01\n")  # fmt: skip

    text = converted(root)

    assert "**Next free: acme-shop#T-20.**" in text
    assert "### acme-shop#T-01 · One" in text
    assert "After acme-shop#T-07," in text and "and acme-shop#T-3." in text
    done = (root / "docs/backlog/done.md").read_text()
    assert done == (
        "- **2026-01-02** · acme-shop#T-06, acme-shop#T-07 · Closed — after acme-shop#T-01\n"
    )


@pytest.mark.parametrize(
    "line",
    [
        "NT-01 and MIT-0 and x-T-1",
        "see docs/T-01 and --grep=T-01 and notes/T-01.md",
        "T-12-rc and T-12x",
        "launch at T-5 days, T-2 h",
        "other#T-01 stays",
        "```\nT-01 in a block\n```",
    ],
)
def test_what_only_looks_like_an_id_stays(tmp_path: Path, line: str) -> None:
    root = repo(tmp_path, backlog=f"**Next free: T-20.**\n{line}\n")

    assert converted(root).endswith(f"{line}\n")


def test_a_number_never_given_out_stays_and_is_listed(tmp_path: Path) -> None:
    root = repo(tmp_path, backlog="**Next free: T-20.**\nCôté voisin, T-391 attend.\n")

    result = tickets.plan(root)

    assert any("T-391" in left for left in result.left)
    assert "T-391 attend" in converted(root)


def test_an_unknown_owner_is_never_taken_for_this_repo(tmp_path: Path) -> None:
    root = repo(tmp_path, backlog=HEAD + "Waiting for billing's T-03.\n")

    assert "billing's T-03." in converted(root)
    assert any("whose?" in left for left in tickets.plan(root).left)


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("(blocked: grog's T-01)", "(blocked: ion-learn#T-01)"),
        ("hearth's T-07 and T-05", "ion-host#T-07 and ion-repo#T-05"),
        ("cone's\nT-01", "ion-score#T-01"),
        ("slake's T-07", "ion-render#T-07"),
        ("grog T-01", "ion-learn#T-01"),
        ("kiln's T-05", "ion-repo#T-05"),
        ("Côté ion-host : T-391.", "Côté ion-host : ion-host#T-391."),
        ("ion-host's T-320, T-321", "ion-host#T-320, ion-host#T-321"),
    ],
)
def test_a_citation_takes_the_cited_repo_current_name(
    tmp_path: Path, written: str, expected: str
) -> None:
    root = repo(tmp_path, "ion-repo", backlog=f"**Next free: T-20.**\n{written}\n")

    assert expected in converted(root)


def test_the_family_old_names_mean_nothing_in_a_client_repo(tmp_path: Path) -> None:
    root = repo(tmp_path, "acme-shop", backlog="**Next free: T-20.**\nOur cone's T-01.\n")

    assert "cone's T-01" in converted(root)


def test_a_second_run_has_nothing_to_do_and_no_byte_is_lost(tmp_path: Path) -> None:
    source = "**Next free: T-20.**\r\n\r\n### T-01 · Café  \r\n\n\tT-02 · ok\r\nno end of file"
    root = repo(tmp_path, backlog=source)

    text = converted(root)

    assert text.replace("acme-shop#", "") == source
    assert tickets.plan(root).writes == {}


def test_nothing_is_written_without_a_yes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = repo(tmp_path, backlog=HEAD)

    assert tickets.migrate(root, ask=None) is False
    assert tickets.migrate(root, ask=lambda _: "n") is False
    assert tickets.migrate(root, dry_run=True, assume_yes=True) is False
    assert (root / "docs/backlog/backlog.md").read_text() == HEAD
    assert "acme-shop#T-NN" in capsys.readouterr().out

    assert tickets.migrate(root, ask=lambda _: "y") is True
    assert "acme-shop#T-01" in (root / "docs/backlog/backlog.md").read_text()


def test_a_rename_moves_the_own_prefix_only(tmp_path: Path) -> None:
    source = "shop#T-01, other-shop#T-02, ion-host#T-07, shop#T-1\n"
    root = repo(tmp_path, "shop", backlog=source, done="shop#T-03\n")

    assert tickets.rename_prefix(root, "shop", "new.name") == 3
    assert tickets.rename_prefix(root, "shop", "new.name") == 0
    text = (root / "docs/backlog/backlog.md").read_text()
    assert text == "new.name#T-01, other-shop#T-02, ion-host#T-07, new.name#T-1\n"


def test_the_name_is_never_a_worktree_folder(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "from-pyproject"\n')
    assert tickets.repo_name(tmp_path) == "from-pyproject"

    (tmp_path / ".copier-answers.yml").write_text("name: from-answers\n")
    assert tickets.repo_name(tmp_path) == "from-answers"


def test_ion_repo_new_writes_the_name_given(tmp_path: Path) -> None:
    """The real command, a name nothing in ion-repo knows: the generated backlog carries it, the
    tracking's how-to too, and no other repo's name is left in them."""
    name = "zorglub-42"
    environment = {**os.environ, "ION_REPO_TEMPLATE": str(REPO), "UV_NO_SYNC": "1"}
    created = subprocess.run(
        [Path(sys.executable).parent / "ion-repo", "new", name, "--no-github", "--no-install",
         "--backend", "cli", "--frontend", "none", "--language", "en"],
        cwd=tmp_path, env=environment, capture_output=True, text=True, check=False,
    )  # fmt: skip
    assert created.returncode == 0, created.stdout[-3000:] + created.stderr[-3000:]

    folder = tmp_path / name / "docs/backlog"
    backlog = (folder / "backlog.md").read_text()
    assert f"**Next free: {name}#T-02.**" in backlog
    assert f"### {name}#T-01 · Ticket title" in backlog
    assert f"· {name}#T-NN · Title" in (folder / "done.md").read_text()
    how_to = (folder / "README.md").read_text()
    assert f"`{name}#T-NN`" in how_to
    for text in (backlog, how_to):
        assert "ion-repo#" not in text and "ion-host#" not in text
    assert tickets.plan(tmp_path / name).writes == {}
