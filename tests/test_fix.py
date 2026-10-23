"""`kiln fix` (T-126) and its first converters (T-127, T-128): one commit per rule on a work
branch, undone when the checks turn red, nothing written by a dry run, and each converter
closing its rule. The network (commit SHAs, digests) is faked."""

import subprocess
from pathlib import Path

import pytest

from kiln.grid import detectors, fix
from kiln.grid.facts import read_repo
from kiln.grid.fixers import FIXERS, ci, containers, python, resolve
from kiln.grid.model import load_rules
from kiln.shell import KilnError

SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"
DIGEST = "sha256:" + "a" * 64
RULES = {rule.id: rule for rule in load_rules()}


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(resolve, "commit_of", lambda repo, ref: SHA)
    monkeypatch.setattr(resolve, "exact_version", lambda repo, sha: "v4.2.2")
    monkeypatch.setattr(resolve, "latest_release", lambda repo, major=None: "v4.2.0")
    monkeypatch.setattr(resolve, "image_digest", lambda image: DIGEST)


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


def closes(rule_id: str, root: Path) -> bool:
    """The converter of `rule_id` runs, and the rule's detector passes afterwards."""
    rule = RULES[rule_id]
    assert detectors.detect(rule.detector, read_repo(root)).status == detectors.FAIL
    FIXERS[rule.fixer].convert(read_repo(root))
    return detectors.detect(rule.detector, read_repo(root)).status == detectors.PASS


WORKFLOW = ".github/workflows/ci.yml"
CONVERTED = {
    "PINNED-ACTIONS": {
        WORKFLOW: "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n"
        "      - uses: 'owner/repo/.github/workflows/x.yml@main' # kept\n"
    },
    "UPDATE-COOLDOWN": {
        ".github/dependabot.yml": "version: 2\nupdates:\n  - package-ecosystem: uv\n"
        "    directory: /\n  - package-ecosystem: npm\n    directory: /web\n"
    },
    "DEPENDENCY-UPDATES": {"uv.lock": "", "web/package.json": "{}", "Containerfile": "FROM a\n"},
    "WORKFLOW-PERMISSIONS": {WORKFLOW: "on: push\njobs:\n  a:\n    runs-on: x\n"},
    "SECRET-SCAN": {".pre-commit-config.yaml": "repos:\n  - repo: local\n    hooks: []\n"},
    "CI-PRESENT": {"package.json": '{"scripts": {"lint": "eslint", "test": "vitest"}}'},
    "NO-OBSOLETE-BACKPORTS": {"requirements.txt": "flask==3.1\ntyping==3.7.4.3\n"},
    "PYTHON-LINTER": {
        "pyproject.toml": "[project]\nname = 'a'\n\n[tool.black]\nline-length = 88\n"
    },
    "TS-EXPECT-ERROR": {"a.ts": "// @ts-ignore\nconst x = 1\n"},
    "IMAGES-BY-DIGEST": {"Dockerfile": "FROM node:24 AS build\nFROM build\n"},
    "CURRENT-DEBIAN": {"Dockerfile": f"FROM python:3.12-slim-bookworm@{DIGEST}\n"},
    "NON-ROOT-CONTAINERS": {"Dockerfile": 'FROM python:3.14-slim\nCOPY . .\nCMD ["app"]\n'},
    "SUPPORTED-RUNTIMES": {
        ".nvmrc": "18\n",
        "package.json": '{"engines": {"node": ">=16"}}',
        "Dockerfile": "FROM node:18-alpine\n",
    },
}


@pytest.mark.parametrize("rule_id", sorted(CONVERTED))
def test_each_converter_closes_its_rule(tmp_path: Path, rule_id: str) -> None:
    assert closes(rule_id, make(tmp_path, CONVERTED[rule_id]))


def test_every_converter_named_by_a_rule_has_a_case() -> None:
    assert {rule.id for rule in RULES.values() if rule.fixer} == set(CONVERTED) | {
        "LOCKED-DEPENDENCIES",  # needs uv and the index: run by hand on the training repos
        # The compressor finds its own gaps and runs the tests: tests/test_compressor.py.
        "DEAD-CODE",
        "UNUSED-DEPENDENCIES",
    }


def test_pinned_actions_keep_their_exact_version_as_a_comment(tmp_path: Path) -> None:
    root = make(tmp_path, CONVERTED["PINNED-ACTIONS"])
    ci.pin_actions(read_repo(root))
    text = (root / WORKFLOW).read_text()
    assert f"uses: actions/checkout@{SHA} # v4.2.2\n" in text
    assert f"uses: 'owner/repo/.github/workflows/x.yml@{SHA}' # kept" in text


def test_the_exact_version_is_the_most_precise_tag_on_the_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    refs = {"main": SHA, "v7": SHA, "v7.0": SHA, "v7.0.1": SHA, "v7.0.0": "0" * 40}
    monkeypatch.undo()  # the real lookup, on faked refs
    monkeypatch.setattr(resolve, "remote_refs", lambda repo: refs)

    assert resolve.exact_version("actions/checkout", SHA) == "v7.0.1"
    assert resolve.exact_version("actions/checkout", "1" * 40) is None


def test_dependabot_also_updates_the_actions_of_composite_actions(tmp_path: Path) -> None:
    composite = "runs:\n  using: composite\n  steps:\n"
    root = make(
        tmp_path,
        {
            WORKFLOW: "jobs:\n  a:\n    steps:\n      - uses: ./.github/actions/setup\n",
            ".github/actions/setup/action.yml": f"{composite}    - uses: astral-sh/setup-uv@v7\n",
            "actions/plain/action.yml": f"{composite}    - run: echo nothing to update\n",
        },
    )

    ci.add_dependabot(read_repo(root))

    text = (root / ".github/dependabot.yml").read_text()
    folders = '    directories:\n      - "/"\n      - "/.github/actions/setup"\n'
    assert f"github-actions\n{folders}" in text
    assert "/actions/plain" not in text


def test_a_workflow_that_writes_is_left_to_judgment(tmp_path: Path) -> None:
    root = make(tmp_path, {WORKFLOW: "jobs:\n  a:\n    steps:\n      - run: git push\n"})
    assert ci.add_permissions(read_repo(root)) == []


def test_a_server_base_keeps_its_user(tmp_path: Path) -> None:
    root = make(tmp_path, {"Dockerfile": "FROM php:8-apache\n"})
    assert containers.add_user(read_repo(root)) == []
    root = make(tmp_path / "node", {"Dockerfile": 'FROM node:24\nCMD ["x"]\n'})
    containers.add_user(read_repo(root))
    assert (root / "Dockerfile").read_text() == 'FROM node:24\nUSER node\nCMD ["x"]\n'


def test_black_line_length_is_carried_over_to_ruff(tmp_path: Path) -> None:
    root = make(tmp_path, CONVERTED["PYTHON-LINTER"])
    python.add_ruff(read_repo(root))
    assert "[tool.ruff]\nline-length = 88\n" in (root / "pyproject.toml").read_text()


# --- the engine -----------------------------------------------------------------------------


def test_one_commit_per_rule_on_a_work_branch(tmp_path: Path) -> None:
    root = make(tmp_path, {**CONVERTED["NO-OBSOLETE-BACKPORTS"], **CONVERTED["TS-EXPECT-ERROR"]})

    outcomes = fix.fix(root)

    fixed = {found.rule for found in outcomes if found.status == "fixed"}
    assert {"NO-OBSOLETE-BACKPORTS", "TS-EXPECT-ERROR", "CI-PRESENT"} <= fixed
    assert git(root, "branch", "--show-current").startswith("kiln/fix-")
    log = git(root, "log", "--format=%s%n%b", "main..")
    assert "fix(NO-OBSOLETE-BACKPORTS): obsolete backports removed" in log
    assert "Source: https://pypi.org/project/typing/" in log and fix.UNVERIFIED in log


def test_the_checks_type_the_files_the_mypy_config_names(tmp_path: Path) -> None:
    root = make(tmp_path, {"pyproject.toml": '[tool.mypy]\nfiles = ["src"]\n', "uv.lock": ""})
    assert ["uv", "run", "mypy"] in fix.check_commands(root)

    (root / "pyproject.toml").write_text("[tool.mypy]\nstrict = true\n")
    assert ["uv", "run", "mypy", "."] in fix.check_commands(root)


def test_checks_red_before_the_fix_are_named_not_taken_for_no_tests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    monkeypatch.setattr(fix, "check_commands", lambda root: [["true"], ["mypy", "."]])
    monkeypatch.setattr(fix, "run_checks", lambda root, commands: commands != [["mypy", "."]])

    fix.fix(root, only="TS-EXPECT-ERROR")

    log = git(root, "log", "--format=%b", "main..")
    assert "unverified: `mypy .` was red before the fix" in log
    assert fix.UNVERIFIED not in log
    assert "`mypy .` was red before the fix" in capsys.readouterr().out


def test_a_converter_that_turns_the_checks_red_is_undone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    monkeypatch.setattr(fix, "check_commands", lambda root: [["true"]])
    calls = iter([True, False])
    monkeypatch.setattr(fix, "run_checks", lambda root, commands: next(calls))

    outcomes = fix.fix(root, only="TS-EXPECT-ERROR")

    assert [(found.rule, found.status) for found in outcomes] == [("TS-EXPECT-ERROR", "reverted")]
    assert "@ts-ignore" in (root / "a.ts").read_text()
    assert git(root, "log", "--oneline", "main..") == ""


def test_a_dry_run_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])

    fix.fix(root, dry_run=True, only="TS-EXPECT-ERROR")

    assert "+// @ts-expect-error" in capsys.readouterr().out
    assert git(root, "status", "--porcelain") == ""
    assert git(root, "branch", "--show-current").strip() == "main"
    assert "@ts-ignore" in (root / "a.ts").read_text()


def test_a_dirty_tree_is_refused(tmp_path: Path) -> None:
    root = make(tmp_path, {"a.ts": "x\n"})
    (root / "a.ts").write_text("y\n")
    with pytest.raises(KilnError, match="uncommitted"):
        fix.fix(root)


def test_a_dry_run_leaves_a_dirty_tree_alone(tmp_path: Path) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    (root / "notes.md").write_text("draft\n")

    fix.fix(root, dry_run=True, only="TS-EXPECT-ERROR")

    assert git(root, "status", "--porcelain").strip() == "?? notes.md"


def test_files_the_repo_ignores_are_still_committed(tmp_path: Path) -> None:
    root = make(tmp_path, {".gitignore": ".*\n", "uv.lock": ""})
    git(root, "add", "--force", ".gitignore")
    git(root, "commit", "-q", "-m", "ignore")

    fix.fix(root, only="DEPENDENCY-UPDATES")

    assert ".github/dependabot.yml" in git(root, "ls-files")


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("node", ("registry-1.docker.io", "library/node")),
        ("docker.io/library/node", ("registry-1.docker.io", "library/node")),
        ("docker.io/bitnami/redis", ("registry-1.docker.io", "bitnami/redis")),
        ("bitnami/redis", ("registry-1.docker.io", "bitnami/redis")),
        ("ghcr.io/astral-sh/uv", ("ghcr.io", "astral-sh/uv")),
        ("localhost:5000/app", ("localhost:5000", "app")),
    ],
)
def test_docker_hub_images_are_asked_of_its_registry(name: str, expected: tuple[str, str]) -> None:
    """`docker.io/library/node` named in full answers at registry-1.docker.io, not docker.io."""
    assert resolve.registry_path(name) == expected
