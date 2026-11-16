"""An adopted npm repo stays on npm: locks, CI, rules; and `ion repo publish` on a repo already on
GitHub makes develop and protects its branches."""

import os
import subprocess
from pathlib import Path

import pytest
import yaml
from test_template import generate

from ion_repo import github, new
from ion_repo.ci.jobs import DEFAULTS, plan_job
from ion_repo.ci.runner import front_install_step
from ion_repo.ci.workflow import Job
from ion_repo.deps import lock_dependencies, sync_dependencies, update_dependencies
from ion_repo.stack import ROOT_DIR, Stack

LOGGER = '#!/bin/sh\necho "$(basename "$0") $*" >> "$CALLS"\n'
GH = LOGGER + 'case "$*" in *"--jq"*) echo "Protection main" ;; esac\n'


def _fake_bin(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, **scripts: str) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in scripts.items():
        (bin_dir / name).write_text(body)
        (bin_dir / name).chmod(0o755)
    calls = tmp_path / "calls.txt"
    calls.touch()
    monkeypatch.setenv("CALLS", str(calls))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return calls


def test_an_npm_repo_is_locked_and_synced_by_npm(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fake_bin(tmp_path, monkeypatch, npm=LOGGER, pnpm=LOGGER)
    root = tmp_path / "cinematch"
    root.mkdir()
    (root / "package-lock.json").write_text("{}")
    stack = Stack("none", "vite-react", has_podman=False, frontend_dir=ROOT_DIR)

    lock_dependencies(root, stack)
    sync_dependencies(root, stack)

    assert calls.read_text().splitlines() == ["npm install --package-lock-only", "npm install"]


def test_an_npm_front_renders_npm_rules_and_ci(tmp_path: Path) -> None:
    root = generate(tmp_path, backend="none", frontend="vite-react", node_manager="npm")

    rules = (root / ".claude/rules/ion-repo/project.md").read_text()
    assert "`npm install <package>`" in rules
    assert "never pnpm" in rules
    ci = yaml.safe_load((root / ".github/workflows/ci.yml").read_text())
    assert ci["jobs"]["frontend"]["with"]["manager"] == "npm"


def test_ion_repo_ci_installs_and_runs_an_npm_front_with_npm(tmp_path: Path) -> None:
    (tmp_path / "package-lock.json").write_text("{}")
    job = Job("frontend", "pnpm", {"directory": ".", "manager": "npm", "scripts": "lint\n"})

    assert front_install_step(tmp_path, ".").command == "npm ci"
    assert [step.command for step in plan_job(job).steps] == ["npm run lint"]
    assert DEFAULTS["pnpm"]["manager"] == "pnpm"


def test_publish_on_a_repo_already_on_github_makes_develop_and_protects_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = _fake_bin(tmp_path, monkeypatch, gh=GH)
    monkeypatch.setattr(github, "can_publish", lambda: True)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    root = tmp_path / "cinematch"
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=root, check=True)
    url = "https://github.com/someone/cinematch.git"
    subprocess.run(["git", "remote", "add", "origin", url], cwd=root, check=True)
    # Pushes land in the local bare repo; `get-url origin` still names GitHub.
    subprocess.run(["git", "config", f"url.{remote}.pushInsteadOf", url], cwd=root, check=True)

    new.publish_project(root)

    branches = subprocess.run(
        ["git", "branch", "--format=%(refname:short)"], cwd=remote, capture_output=True, text=True
    )
    assert branches.stdout.split() == ["develop"]
    logged = calls.read_text()
    assert "repo edit someone/cinematch --default-branch develop" in logged
    assert logged.count("-X POST repos/someone/cinematch/rulesets") == 1
    assert "automated-security-fixes" in logged


@pytest.mark.parametrize(
    "url", ["git@github.com:someone/cinematch.git", "https://github.com/someone/cinematch"]
)
def test_a_github_origin_names_its_repository(url: str) -> None:
    found = new.GITHUB_REPOSITORY.search(url)
    assert found is not None
    assert found["repository"] == "someone/cinematch"


FAKE_NPM_OUTDATED = (
    LOGGER
    + """case "$1" in
  outdated) echo '{"vite": {"current": "8.3.8", "latest": "8.4.0", "type": "devDependencies"},
    "react": {"current": "19.3.1", "latest": "20.0.0", "type": "dependencies"}}'; exit 1 ;;
esac
"""
)


def test_an_npm_repo_updates_its_dependencies_with_npm(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # `ion repo update` on an adopted npm repo: pnpm stopped on ERR_PNPM_NO_LOCKFILE.
    calls = _fake_bin(tmp_path, monkeypatch, npm=FAKE_NPM_OUTDATED, pnpm=LOGGER)
    root = tmp_path / "cinematch"
    root.mkdir()
    (root / "package-lock.json").write_text("{}")
    stack = Stack("none", "vite-react", has_podman=False, frontend_dir=ROOT_DIR)

    update_dependencies(root, stack, allow_major=False)

    assert calls.read_text().splitlines() == [
        "npm ci",
        "npm outdated --json",
        "npm install --save-dev vite@8.4.0",
        "npm install",
    ]
