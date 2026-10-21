"""`kiln version cut` and `kiln version promote` on a throwaway repo with its own origin (T-29)."""

import datetime
import subprocess
from pathlib import Path

import pytest
from packaging.version import Version

from kiln import github_ci, shipping
from kiln.release import Tag, read_tags
from kiln.shell import KilnError

CHANGELOG = "# What's new\n\nHeader.\n\n## v0.1.0 — 2026-10-01\n- First release.\n"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def commit(repo: Path, message: str) -> None:
    (repo / "notes.txt").write_text(message)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(shipping, "LOCK", ["true"])
    monkeypatch.setattr(shipping, "CHECKS", (["true"],))
    # GitHub's CI, green unless a test says otherwise.
    monkeypatch.setattr(github_ci, "wait_until_green", lambda *_: "https://ci")
    monkeypatch.setattr(github_ci, "verdict", lambda *_: "success")
    origin, clone = tmp_path / "origin.git", tmp_path / "kiln"
    git(tmp_path, "init", "-q", "--bare", "-b", "develop", str(origin))
    git(tmp_path, "clone", "-q", str(origin), str(clone))
    (clone / "src/kiln").mkdir(parents=True)
    (clone / "src/kiln/versions.py").write_text("")
    (clone / "pyproject.toml").write_text('[project]\nname = "kiln-cli"\nversion = "0.1.0"\n')
    (clone / "CHANGELOG.md").write_text(CHANGELOG)
    for readme in shipping.READMES:
        (clone / readme).parent.mkdir(parents=True, exist_ok=True)
        (clone / readme).write_text("# kiln\n")
    (clone / "plugins/kiln/.claude-plugin").mkdir(parents=True)
    (clone / "plugins/kiln/.claude-plugin/plugin.json").write_text('{"version": "0.2.0"}\n')
    (clone / ".gitignore").write_text(".claude/\n")
    git(clone, "add", "-A")
    git(clone, "commit", "-qm", "chore: start")
    git(clone, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    git(clone, "branch", "main")
    git(clone, "push", "-q", "origin", "develop", "main", "v0.1.0")
    return clone


def publish(repo: Path, message: str) -> None:
    commit(repo, message)
    git(repo, "push", "-q", "origin", "develop")


def rewrite_draft(tree: Path, *, readmes: bool = True) -> None:
    changelog = tree / "CHANGELOG.md"
    changelog.write_text(changelog.read_text().replace(shipping.DRAFT_MARKER + "\n", ""))
    if readmes:
        for readme, _ in shipping.DOCS_BY_LANGUAGE:
            (tree / readme).write_text((tree / readme).read_text() + "What's new.\n")
    git(tree, "commit", "-qam", "docs(changelog): the entry rewritten")


def test_draft_puts_breaking_changes_first_and_leaves_chores_out() -> None:
    subjects = ["fix: a bug", "docs: typo", "feat!: renamed set", "feat: x\n\nBREAKING CHANGE: y"]

    entry = shipping.draft_entry("0.4.0", subjects, today="2026-10-19")

    assert entry.splitlines() == [
        "## v0.4.0 — 2026-10-19",
        shipping.DRAFT_MARKER,
        "- **Breaking**: Renamed set",
        "- **Breaking**: X",
        "- A bug",
    ]


def test_changelog_entry_is_the_body_of_its_version() -> None:
    changelog = CHANGELOG + "\n## v0.0.9 — 2026-09-01\n- Older.\n"

    assert shipping.changelog_entry(changelog, "0.1.0") == "- First release."
    with pytest.raises(KilnError):
        shipping.changelog_entry(changelog, "9.9.9")


def test_cut_drafts_then_tags_a_candidate_once_the_entry_is_rewritten(repo: Path) -> None:
    (repo / "plugins/kiln/hook.py").write_text("")
    publish(repo, "feat: kiln version cut")

    shipping.cut(repo)
    tree = repo / ".claude/worktrees/release-v0.1.1"
    assert '"0.1.1"' in (tree / "pyproject.toml").read_text()
    assert '"0.2.1"' in (tree / "plugins/kiln/.claude-plugin/plugin.json").read_text()
    entry = (tree / "CHANGELOG.md").read_text()
    assert entry.index("## v0.1.1") < entry.index("## v0.1.0")
    assert "- Kiln version cut" in entry

    with pytest.raises(KilnError, match="still a draft"):
        shipping.cut(repo)
    rewrite_draft(tree)
    shipping.cut(repo)

    assert "v0.1.1-rc.1" in git(repo, "ls-remote", "--tags", "origin")


def test_promote_waits_for_a_newer_candidate_then_publishes(repo: Path) -> None:
    publish(repo, "feat: one")
    shipping.cut(repo)
    rewrite_draft(repo / ".claude/worktrees/release-v0.1.1")
    shipping.cut(repo)
    with pytest.raises(KilnError, match="no candidate ready"):
        shipping.promote(repo)

    publish(repo, "fix: two")
    shipping.cut(repo)  # the open release is a candidate already: the next one starts
    # The candidate still open comes into the next release: its entry and number first.
    next_tree = repo / ".claude/worktrees/release-v0.1.2"
    assert git(next_tree, "merge-base", "--is-ancestor", "v0.1.1-rc.1", "HEAD") == ""
    changelog = (next_tree / "CHANGELOG.md").read_text()
    assert (
        changelog.index("## v0.1.2") < changelog.index("## v0.1.1") < changelog.index("## v0.1.0")
    )
    rewrite_draft(repo / ".claude/worktrees/release-v0.1.2")
    shipping.cut(repo)
    shipping.promote(repo)

    git(repo, "fetch", "-q", "origin")
    assert git(repo, "rev-list", "-n1", "v0.1.1") == git(repo, "rev-list", "-n1", "v0.1.1-rc.1")
    assert git(repo, "merge-base", "--is-ancestor", "v0.1.1", "origin/main") == ""
    assert git(repo, "merge-base", "--is-ancestor", "v0.1.1", "origin/develop") == ""
    assert "release/v0.1.1" not in git(repo, "branch", "-a")
    assert [tag.name for tag in read_tags(repo)][-1] == "v0.1.2-rc.1"


def test_promote_refuses_a_candidate_not_ready() -> None:
    now = datetime.datetime.now(datetime.UTC)
    tags = [Tag("v0.1.1-rc.1", Version("0.1.1rc1"), now)]

    with pytest.raises(KilnError, match="waiting"):
        shipping.pick_candidate(tags, "v0.1.1", lambda _: "success")
    # A newer candidate is not enough: the CI of the one promoted must be green.
    tags.append(Tag("v0.1.2-rc.1", Version("0.1.2rc1"), now))
    with pytest.raises(KilnError, match=r"CI not green \(failure\)"):
        shipping.pick_candidate(tags, "v0.1.1", lambda _: "failure")
    with pytest.raises(KilnError, match="no candidate ready"):
        shipping.pick_candidate(tags, None, lambda _: "running")


def test_cut_tags_nothing_while_the_ci_of_the_release_is_red(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    publish(repo, "feat: one")
    shipping.cut(repo)
    rewrite_draft(repo / ".claude/worktrees/release-v0.1.1")

    def red(*_: object) -> str:
        raise KilnError("the CI of release/v0.1.1 is not green (failure)")

    monkeypatch.setattr(github_ci, "wait_until_green", red)
    with pytest.raises(KilnError, match="not green"):
        shipping.cut(repo)

    remote = git(repo, "ls-remote", "origin")
    assert "refs/heads/release/v0.1.1" in remote  # pushed, for GitHub to check it
    assert "v0.1.1-rc.1" not in remote and "v0.1.1-rc.1" not in git(repo, "tag")


def test_draft_carries_what_repos_must_do_after_updating() -> None:
    subjects = ["feat: owner reserved\n\nAfter updating: give each owner's @login", "docs: typo"]

    entry = shipping.draft_entry("0.4.0", subjects, today="2026-10-19")

    assert entry.splitlines()[-2:] == [
        "- Owner reserved",
        "- **After updating**: give each owner's @login",
    ]


def test_a_fix_of_a_candidate_bumps_the_plugins_it_touches(repo: Path) -> None:
    publish(repo, "feat: one")
    shipping.cut(repo)
    tree = repo / ".claude/worktrees/release-v0.1.1"
    rewrite_draft(tree)
    shipping.cut(repo)
    manifest = tree / "plugins/kiln/.claude-plugin/plugin.json"
    tagged = manifest.read_text()

    (tree / "plugins/kiln/hook.py").write_text("fixed\n")
    git(tree, "add", "-A")
    git(tree, "commit", "-qm", "fix: the hook")
    shipping.cut(repo)

    assert "v0.1.1-rc.2" in git(repo, "ls-remote", "--tags", "origin")
    assert manifest.read_text() != tagged
    assert git(tree, "log", "-1", "--format=%s", "v0.1.1-rc.2") == (
        "chore(release): plugins of the fix bumped"
    )


def test_a_release_whose_readmes_say_nothing_new_is_not_tagged(repo: Path) -> None:
    publish(repo, "feat: one")
    shipping.cut(repo)
    tree = repo / ".claude/worktrees/release-v0.1.1"
    rewrite_draft(tree, readmes=False)

    with pytest.raises(
        KilnError,
        match=r"neither README\.md nor docs/reference\.md, README\.fr\.md nor .* since v0\.1\.0",
    ):
        shipping.cut(repo)
    assert "v0.1.1-rc.1" not in git(repo, "tag")

    # Nothing visible to say: the entry says why, and the release goes.
    changelog = tree / "CHANGELOG.md"
    changelog.write_text(
        changelog.read_text()
        .replace("## v0.1.1 — ", "## v0.1.1 — ", 1)
        .replace("- One\n", "- One\n<!-- readme: unchanged, internal only -->\n", 1)
    )
    git(tree, "commit", "-qam", "docs(changelog): nothing for the README")
    shipping.cut(repo)
    assert "v0.1.1-rc.1" in git(repo, "tag")


def test_a_cut_stopped_by_a_conflict_drafts_before_it_tags(repo: Path) -> None:
    publish(repo, "feat: first")
    shipping.cut(repo)
    rewrite_draft(repo / ".claude/worktrees/release-v0.1.1")
    shipping.cut(repo)
    publish(repo, "feat: second")
    # The state a conflict carrying release/v0.1.1 leaves: the branch, resolved by hand, and
    # neither the draft nor the numbers.
    tree = repo / ".claude/worktrees/release-v0.1.2"
    git(repo, "worktree", "add", "-q", "-b", "release/v0.1.2", str(tree), "origin/develop")
    git(tree, "merge", "-q", "--no-ff", "origin/release/v0.1.1", "-m", "Merge release/v0.1.1")

    shipping.cut(repo)

    assert "v0.1.2-rc.1" not in git(repo, "ls-remote", "--tags", "origin")
    assert shipping.DRAFT_MARKER in (tree / "CHANGELOG.md").read_text()
    assert '"0.1.2"' in (tree / "pyproject.toml").read_text()
    rewrite_draft(tree)
    shipping.cut(repo)
    assert "v0.1.2-rc.1" in git(repo, "ls-remote", "--tags", "origin")
