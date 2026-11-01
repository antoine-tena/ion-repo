"""What the grid does not know, told to ion-repo with the user's yes (ion-repo#T-38)."""

import json
import subprocess
from pathlib import Path

import pytest

from ion_repo.grid import gap_report, score


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["celery>=5", "acme-internal-billing"]\n'
    )
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    return tmp_path


class FakeGh:
    """`gh` answering from a list of open issues; records what would be posted."""

    def __init__(self, issues: list[dict[str, object]]) -> None:
        self.issues = issues
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, *args: str) -> subprocess.CompletedProcess[str]:
        self.calls.append(args)
        if args[:2] == ("issue", "list"):
            return subprocess.CompletedProcess(args, 0, json.dumps(self.issues), "")
        if args[:2] == ("issue", "create"):
            return subprocess.CompletedProcess(args, 0, "https://github.com/x/issues/9\n", "")
        return subprocess.CompletedProcess(args, 0, "", "")


@pytest.fixture
def gh(monkeypatch: pytest.MonkeyPatch) -> FakeGh:
    fake = FakeGh([])
    monkeypatch.setattr(gap_report, "_gh", fake)
    monkeypatch.setattr("ion_repo.grid.gap_report.shutil.which", lambda name: "/usr/bin/gh")
    return fake


def test_a_known_package_the_grid_does_not_cover_is_named_and_a_private_one_never(
    repo: Path,
) -> None:
    report = score.score_repo(repo)

    assert "celery (task queue): not covered by the grid yet" in report.uncovered
    assert not any("acme" in line for line in report.uncovered)


def test_a_yes_opens_one_issue_with_the_line_only_and_never_offers_it_again(
    repo: Path, gh: FakeGh
) -> None:
    report = score.score_repo(repo)

    gap_report.offer(repo, report, lambda prompt: "y")
    gap_report.offer(repo, report, lambda prompt: pytest.fail("asked twice"))

    created = [call for call in gh.calls if call[:2] == ("issue", "create")]
    assert len(created) == 1
    title, body = created[0][created[0].index("--title") + 1], created[0][-1]
    assert title == "Grid gap: celery (task queue)"
    assert body.startswith("celery (task queue): not covered by the grid yet\n")
    assert str(repo) not in body


def test_an_open_issue_for_the_same_gap_gets_a_thumbs_up_instead(repo: Path, gh: FakeGh) -> None:
    gh.issues = [{"number": 77, "title": "Grid gap: celery (task queue)"}]

    gap_report.offer(repo, score.score_repo(repo), lambda prompt: "y")

    assert not any(call[:2] == ("issue", "create") for call in gh.calls)
    assert (
        "api",
        "-X",
        "POST",
        "repos/antoine-tena/ion-repo/issues/77/reactions",
        "-f",
        "content=+1",
    ) in gh.calls


def test_never_holds_for_the_repo_and_no_terminal_asks_nothing(repo: Path, gh: FakeGh) -> None:
    report = score.score_repo(repo)

    gap_report.offer(repo, report, None)
    gap_report.offer(repo, report, lambda prompt: "v")
    gap_report.offer(repo, report, lambda prompt: pytest.fail("asked after never"))

    assert gh.calls == []


def test_without_gh_a_prefilled_link_is_given(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("ion_repo.grid.gap_report.shutil.which", lambda name: None)

    said = gap_report.tell("PHP: not covered by the grid yet")

    assert "https://github.com/antoine-tena/ion-repo/issues/new?title=Grid+gap%3A+PHP" in said
