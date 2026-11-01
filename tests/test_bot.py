"""`ion repo bot` (ion-repo#T-59): kiln-bot's run on `kiln/bot`, one pull request's body, nothing
when
nothing changed, a person's commits never reset. The network is faked."""

import subprocess
from pathlib import Path

import pytest

from ion_repo import bot
from ion_repo.grid import checks
from ion_repo.grid.fixers import containers, resolve
from ion_repo.shell import KilnError

SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(resolve, "commit_of", lambda repo, ref: SHA)
    monkeypatch.setattr(resolve, "exact_version", lambda repo, sha: "v4.2.2")
    monkeypatch.setattr(resolve, "latest_release", lambda repo, major=None: "v4.2.0")
    monkeypatch.setattr(resolve, "image_digest", lambda image: "sha256:" + "a" * 64)
    monkeypatch.setattr(containers, "_podman_ready", lambda: False)
    monkeypatch.setattr(checks, "image_builds", lambda root, changed: [])


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True, check=True
    ).stdout


def make(root: Path, files: dict[str, str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    for name, content in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(content)
    git(root, "add", "--all")
    git(root, "commit", "-q", "-m", "start")
    return root


def test_the_week_s_fixes_become_one_pull_request_body(tmp_path: Path) -> None:
    root = make(tmp_path, {"a.ts": "// @ts-ignore\nconst x = 1\n", "README.md": "# a\n"})

    proposal = bot.run_bot(root, update=True, body_path=tmp_path / "body.md")

    assert proposal.before is not None and proposal.after is not None
    assert proposal.changed and proposal.after > proposal.before
    text = (tmp_path / "body.md").read_text()
    assert text.startswith(f"## ion repo score: {proposal.before} → {proposal.after} (+")
    assert "- **fix(TS-EXPECT-ERROR): " in text and " · Score: " in text
    # On kiln/bot, the user's tree and branch untouched.
    assert git(root, "branch", "--show-current").strip() == "main"
    assert "fix(TS-EXPECT-ERROR)" in git(root, "log", "--format=%s", "main..kiln/bot")


def test_a_second_run_starts_the_branch_again_from_the_last_commit(tmp_path: Path) -> None:
    root = make(tmp_path, {"a.ts": "// @ts-ignore\nconst x = 1\n"})
    first = bot.run(root)
    again = bot.run(root)
    assert [subject for subject, _ in again.commits] == [subject for subject, _ in first.commits]
    assert git(root, "rev-list", "--count", "main..kiln/bot").strip() == str(len(first.commits))


def test_nothing_is_proposed_when_nothing_changed(tmp_path: Path) -> None:
    root = make(tmp_path, {"README.md": "# a\n"})  # nothing a converter can close
    proposal = bot.run_bot(root, update=False, body_path=tmp_path / "body.md")
    assert not proposal.changed
    assert not (tmp_path / "body.md").exists()
    assert git(root, "branch", "--list", "kiln/bot") == ""


def test_a_person_s_commit_on_the_branch_is_never_reset(tmp_path: Path) -> None:
    root = make(tmp_path, {"README.md": "# a\n"})
    git(root, "switch", "-q", "-c", "kiln/bot")
    (root / "notes.md").write_text("mine\n")
    git(root, "add", "notes.md")
    git(root, "commit", "-q", "-m", "docs: my notes")
    git(root, "switch", "-q", "main")
    with pytest.raises(KilnError, match="kiln-bot did not write"):
        bot.run(root)
    assert "docs: my notes" in git(root, "log", "--format=%s", "kiln/bot")


def test_without_a_token_what_writes_workflows_is_left_out_and_named(tmp_path: Path) -> None:
    """GITHUB_TOKEN may never push `.github/workflows/`: those commits wait for a token."""
    root = make(
        tmp_path,
        {
            "a.ts": "// @ts-ignore\nconst x = 1\n",
            ".github/workflows/ci.yml": "on: push\njobs:\n  a:\n    runs-on: x\n    steps:\n"
            "      - run: make\n",
        },
    )
    proposal = bot.run(root, workflows=False)
    subjects = [subject for subject, _ in proposal.commits]
    assert any(subject.startswith("fix(TS-EXPECT-ERROR)") for subject in subjects)
    changed = git(root, "diff", "--name-only", "main..kiln/bot")
    assert ".github/workflows/" not in changed
    assert "fix(WORKFLOW-PERMISSIONS)" in proposal.notes[0]
    assert "KILN_BOT_TOKEN" in bot.body(proposal)
