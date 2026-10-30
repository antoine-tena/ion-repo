"""The GitHub settings `kiln score` reads through `gh` (T-158, T-186): answers of a fake `gh`,
admin rights required, a day of cache, nothing in CI, never a token."""

import shutil
import subprocess
from pathlib import Path

import pytest

from kiln.grid import forge

SLUG = "acme/app"
REPO = {
    "default_branch": "develop",
    "visibility": "public",
    "allow_merge_commit": True,
    "permissions": {"admin": True},
    "security_and_analysis": {
        "secret_scanning": {"status": "enabled"},
        "secret_scanning_push_protection": {"status": "disabled"},
    },
}


@pytest.fixture
def gh(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, tuple[int, object]]:
    """The answers of `gh api`, by path; every call recorded under `calls`."""
    answers: dict[str, tuple[int, object]] = {
        f"repos/{SLUG}": (0, REPO),
        f"repos/{SLUG}/rules/branches/develop": (0, [{"type": "deletion"}]),
        f"repos/{SLUG}/branches/develop/protection": (404, None),
        f"repos/{SLUG}/vulnerability-alerts": (0, None),
        f"repos/{SLUG}/automated-security-fixes": (0, {"enabled": False}),
        f"repos/{SLUG}/private-vulnerability-reporting": (0, {"enabled": True}),
        f"repos/{SLUG}/code-scanning/default-setup": (0, {"state": "not-configured"}),
    }
    calls: list[str] = []

    def api(path: str) -> tuple[int, object]:
        calls.append(path)
        return answers.get(path, (404, None))

    monkeypatch.setattr(forge, "_api", api)
    monkeypatch.setattr(forge, "ENABLED", True)
    monkeypatch.setattr(forge, "_read", {})
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    answers["calls"] = (0, calls)
    return answers


def github_repo(root: Path, url: str = f"git@github.com:{SLUG}.git") -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", url], check=True)
    return root


@pytest.mark.parametrize(
    "url",
    [f"git@github.com:{SLUG}.git", f"https://github.com/{SLUG}", f"https://github.com/{SLUG}.git/"],
)
def test_the_github_project_is_read_from_origin(tmp_path: Path, url: str) -> None:
    assert forge.github_slug(github_repo(tmp_path, url)) == SLUG


def test_a_repo_elsewhere_has_no_github_project(tmp_path: Path) -> None:
    assert forge.github_slug(github_repo(tmp_path, "https://gitlab.com/acme/app.git")) is None


def test_settings_read_through_gh(tmp_path: Path, gh: dict[str, tuple[int, object]]) -> None:
    found = forge.settings(github_repo(tmp_path))

    assert found is not None
    assert (found.default_branch, found.public, found.branch_rules) == (
        "develop",
        True,
        ("deletion",),
    )
    assert (found.secret_scanning, found.push_protection) == (True, False)
    assert (found.vulnerability_alerts, found.security_updates) == (True, False)
    assert (found.private_reporting, found.code_scanning) == (True, False)
    assert found.page("rules") == f"https://github.com/{SLUG}/settings/rules"


def test_a_classic_protection_counts_like_a_ruleset(
    tmp_path: Path, gh: dict[str, tuple[int, object]]
) -> None:
    gh[f"repos/{SLUG}/rules/branches/develop"] = (0, [])
    gh[f"repos/{SLUG}/branches/develop/protection"] = (
        0,
        {"allow_force_pushes": {"enabled": False}, "allow_deletions": {"enabled": False}},
    )
    found = forge.settings(github_repo(tmp_path))

    assert found is not None
    assert found.branch_rules == ("deletion", "non_fast_forward")


def test_alerts_off_answer_404(tmp_path: Path, gh: dict[str, tuple[int, object]]) -> None:
    gh[f"repos/{SLUG}/vulnerability-alerts"] = (404, None)
    found = forge.settings(github_repo(tmp_path))

    assert found is not None
    assert found.vulnerability_alerts is False


def test_without_admin_rights_the_settings_are_unknown(
    tmp_path: Path, gh: dict[str, tuple[int, object]]
) -> None:
    gh[f"repos/{SLUG}"] = (0, {**REPO, "permissions": {"admin": False}})

    assert forge.settings(github_repo(tmp_path)) is None


def test_gh_logged_out_means_unknown(tmp_path: Path, gh: dict[str, tuple[int, object]]) -> None:
    gh[f"repos/{SLUG}"] = (-1, None)

    assert forge.settings(github_repo(tmp_path)) is None


def test_a_read_is_kept_a_day(tmp_path: Path, gh: dict[str, tuple[int, object]]) -> None:
    root = github_repo(tmp_path / "repo")
    forge.settings(root)
    calls = gh["calls"][1]
    assert isinstance(calls, list)
    first = len(calls)
    forge._read.clear()

    assert forge.settings(root) is not None
    assert len(calls) == first
    forge._read.clear()
    forge.REFRESH = True
    try:
        forge.settings(root)
    finally:
        forge.REFRESH = False
    assert len(calls) == 2 * first


def test_nothing_is_read_in_ci_nor_without_gh(
    tmp_path: Path, gh: dict[str, tuple[int, object]], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = github_repo(tmp_path)
    monkeypatch.setattr(forge, "ENABLED", False)
    assert forge.settings(root) is None
    monkeypatch.setattr(forge, "ENABLED", True)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert forge.settings(root) is None
    assert gh["calls"][1] == []
