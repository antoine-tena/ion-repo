"""`kiln fix` (T-126) and its first converters (T-127, T-128): one commit per rule on a work
branch, undone when the checks turn red, nothing written by a dry run, and each converter
closing its rule. The network (commit SHAs, digests) is faked."""

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from kiln.grid import checks, detectors, fix, roadmap, score
from kiln.grid.facts import Repo, read_repo
from kiln.grid.fixers import FIXERS, ci, containers, python, resolve
from kiln.grid.model import load_rules
from kiln.shell import KilnError

SHA = "b4ffde65f46336ab88eb53be808477a3936bae11"
DIGEST = "sha256:" + "a" * 64
RULES = {rule.id: rule for rule in load_rules()}


IMAGE_BUILDS = checks.image_builds


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(resolve, "commit_of", lambda repo, ref: SHA)
    monkeypatch.setattr(resolve, "exact_version", lambda repo, sha: "v4.2.2")
    monkeypatch.setattr(resolve, "latest_release", lambda repo, major=None: "v4.2.0")
    monkeypatch.setattr(resolve, "image_digest", lambda image: DIGEST)
    # podman starts every service hardened; tests below say otherwise when they need to.
    monkeypatch.setattr(containers, "_podman_ready", lambda: True)
    monkeypatch.setattr(containers, "_starts", lambda root, name, text, services: set(services))
    # No image is built here: the test that needs a build gives its own.
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


def closes(rule_id: str, root: Path) -> bool:
    """The converter of `rule_id` runs, and the rule's detector passes afterwards."""
    rule = RULES[rule_id]
    assert detectors.detect(rule.detector, read_repo(root)).status == detectors.FAIL
    FIXERS[rule.fixer].convert(read_repo(root))
    return detectors.detect(rule.detector, read_repo(root)).status == detectors.PASS


WORKFLOW = ".github/workflows/ci.yml"
# A CI that only builds: no lint, no tests, no audit.
BUILD_ONLY = (
    "on: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - run: make\n"
)
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
    "HARDENED-CONTAINERS": {
        "compose.yaml": "services:\n  app:\n    build: .\n  db:\n    image: postgres\n"
    },
    "WORKFLOW-INJECTION": {
        WORKFLOW: "jobs:\n  a:\n    steps:\n"
        '      - run: echo "${{ github.event.pull_request.title }}"\n'
    },
    "LINT-IN-CI": {WORKFLOW: BUILD_ONLY, "pyproject.toml": "[tool.ruff]\n"},
    "TESTS-IN-CI": {
        WORKFLOW: BUILD_ONLY,
        "web/package.json": '{"scripts": {"test": "vitest"}}',
        "web/pnpm-lock.yaml": "",
    },
    "VULNERABILITY-AUDIT": {WORKFLOW: BUILD_ONLY, "uv.lock": ""},
    "NO-TRACKED-ENV": {".env": "A=1\n", "web/.env.local": "export B=2\n"},
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


def test_a_service_is_hardened_under_its_own_keys_and_comments_stay() -> None:
    text = (
        "# the stack\nname: shop\nservices:\n  web:\n    image: nginx  # front\n"
        "    read_only: true\n  worker:\n      build: .\nvolumes:\n  data: {}\n"
    )
    assert containers.harden_text(text, ["web", "worker"]) == (
        "# the stack\nname: shop\nservices:\n  web:\n"
        "    cap_drop: [ALL]\n    security_opt: [no-new-privileges:true]\n    tmpfs: [/tmp]\n"
        "    image: nginx  # front\n    read_only: true\n  worker:\n"
        "      read_only: true\n      cap_drop: [ALL]\n"
        "      security_opt: [no-new-privileges:true]\n      tmpfs: [/tmp]\n"
        "      build: .\nvolumes:\n  data: {}\n"
    )


def test_a_service_that_does_not_start_hardened_is_left_as_it_was(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    compose = "services:\n  app:\n    build: .\n  web:\n    image: nginx\n"
    root = make(tmp_path, {"compose.yaml": compose})
    monkeypatch.setattr(containers, "_starts", lambda root, name, text, services: {"app"})

    assert containers.harden_compose(read_repo(root)) == ["compose.yaml"]
    text = (root / "compose.yaml").read_text()
    assert text.startswith("services:\n  app:\n    read_only: true\n")
    assert text.endswith("  web:\n    image: nginx\n")
    assert "compose.yaml (web)" in capsys.readouterr().out


def test_hardening_is_never_guessed_without_podman(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make(tmp_path, CONVERTED["HARDENED-CONTAINERS"])
    monkeypatch.setattr(containers, "_podman_ready", lambda: False)
    with pytest.raises(KilnError, match="podman and podman-compose are needed"):
        containers.harden_compose(read_repo(root))


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


@pytest.mark.parametrize("convert", [containers.move_runtimes, containers.move_to_trixie])
def test_an_old_runtime_on_an_old_debian_moves_both_at_once(
    tmp_path: Path, convert: Callable[[Repo], list[str]]
) -> None:
    # Neither python:3.8-trixie nor python:3.13-buster was ever built.
    root = make(tmp_path, {"Dockerfile": f"FROM python:3.8-buster@{DIGEST}\n"})
    convert(read_repo(root))
    assert (root / "Dockerfile").read_text() == f"FROM python:3.13-trixie@{DIGEST}\n"


def test_requirements_alone_become_a_uv_project_or_are_restored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # T-159: pyproject.toml and uv.lock from requirements.txt, which stays as their export.
    root = make(tmp_path, {"requirements.txt": "flask\n", "requirements-dev.txt": "pytest\n"})
    ran: list[list[str]] = []

    resolvable = True

    def uv(command: list[str], cwd: Path) -> bool:
        ran.append(command)
        if command[1] == "init":
            (cwd / "pyproject.toml").write_text("[project]\n")
        return not (command[1] == "add" and not resolvable)

    monkeypatch.setattr(python, "_uv", uv)
    assert python._uv_project(read_repo(root)) == [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
    ]
    assert [command[1] for command in ran] == ["init", "add", "add", "export", "export"]

    (root / "pyproject.toml").unlink()
    resolvable = False
    assert python._uv_project(read_repo(root)) == []
    assert not (root / "pyproject.toml").exists()
    assert (root / "requirements.txt").read_text() == "flask\n"


def test_black_line_length_is_carried_over_to_ruff(tmp_path: Path) -> None:
    root = make(tmp_path, CONVERTED["PYTHON-LINTER"])
    python.add_ruff(read_repo(root))
    assert "[tool.ruff]\nline-length = 88\n" in (root / "pyproject.toml").read_text()


# --- the engine -----------------------------------------------------------------------------


def fix_branch(root: Path) -> str:
    """The branch `kiln fix` left, the latest when there are several."""
    branches = git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads/kiln/").split()
    return sorted(branches, key=len)[-1] if branches else ""


def test_one_commit_per_rule_on_a_work_branch(tmp_path: Path) -> None:
    root = make(tmp_path, {**CONVERTED["NO-OBSOLETE-BACKPORTS"], **CONVERTED["TS-EXPECT-ERROR"]})

    outcomes = fix.fix(root)

    fixed = {found.rule for found in outcomes if found.status == "fixed"}
    assert {"NO-OBSOLETE-BACKPORTS", "TS-EXPECT-ERROR", "CI-PRESENT"} <= fixed
    # T-171: the user's tree stays where it was, only the branch remains.
    assert git(root, "branch", "--show-current").strip() == "main"
    assert git(root, "status", "--porcelain") == ""
    assert git(root, "worktree", "list").count("\n") == 1
    assert fix_branch(root).startswith("kiln/fix-")
    log = git(root, "log", "--format=%s%n%b", f"main..{fix_branch(root)}")
    assert "fix(NO-OBSOLETE-BACKPORTS): obsolete backports removed" in log
    assert "Source: https://pypi.org/project/typing/" in log and fix.UNVERIFIED in log


def commands(root: Path) -> list[tuple[str, ...]]:
    return [check.argv for check in checks.find(root)]


def test_the_checks_type_the_files_the_mypy_config_names(tmp_path: Path) -> None:
    root = make(tmp_path, {"pyproject.toml": '[tool.mypy]\nfiles = ["src"]\n', "uv.lock": ""})
    assert ("uv", "run", "mypy") in commands(root)

    (root / "pyproject.toml").write_text("[tool.mypy]\nstrict = true\n")
    assert ("uv", "run", "mypy", ".") in commands(root)


def test_checks_are_found_one_folder_down(tmp_path: Path) -> None:
    # Most repos keep their code in backend/ and frontend/: every commit was "unverified" (T-159).
    root = make(
        tmp_path,
        {
            "backend/pyproject.toml": "[tool.ruff]\n",
            "backend/uv.lock": "",
            "backend/manage.py": "",
            "frontend/package.json": '{"scripts": {"lint": "x", "typecheck": "y", "dev": "z"}}',
            "frontend/yarn.lock": "",
            "node_modules/x/package.json": '{"scripts": {"test": "x"}}',
        },
    )

    assert [str(check) for check in checks.find(root)] == [
        "uv run ruff check (in backend/)",
        "uv run python manage.py test (in backend/)",
        "yarn run lint (in frontend/)",
        "yarn run typecheck (in frontend/)",
    ]


def test_bun_and_npm_are_told_apart_by_their_lock(tmp_path: Path) -> None:
    root = make(tmp_path, {"package.json": '{"scripts": {"test": "x"}}', "bun.lock": ""})
    assert commands(root) == [("bun", "run", "test")]
    (root / "bun.lock").unlink()
    assert commands(root) == [("npm", "run", "test")]


def test_a_check_is_red_missing_or_timed_out_and_says_so(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make(tmp_path, {"README.md": "# a\n"})
    red = checks.run(root, checks.Check(("sh", "-c", "echo boom; exit 1")))
    assert (red.status, red.log, red.reason) == (
        "red",
        "boom\n",
        "`sh -c echo boom; exit 1` was red before the fix",
    )
    missing = checks.run(root, checks.Check(("yarn-not-here", "test")))
    assert missing.reason == "yarn-not-here missing (install it)"
    assert checks.Result(checks.Check(("yarn",)), "missing").reason.startswith(
        "yarn missing (corepack"
    )
    monkeypatch.setattr(checks, "CHECK_TIMEOUT", 0.2)
    slow = checks.run(root, checks.Check(("sh", "-c", "echo waiting; sleep 5")))
    assert slow.status == "timeout" and "timed out after 0.2 s" in slow.reason


def test_checks_red_before_the_fix_are_named_and_the_green_ones_judge(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    found = [checks.Check(("true",)), checks.Check(("false",)), checks.Check(("no-such-tool",))]
    monkeypatch.setattr(checks, "find", lambda root: found)

    fix.fix(root, only="TS-EXPECT-ERROR")

    log = git(root, "log", "--format=%b", f"main..{fix_branch(root)}")
    assert "Checked: true" in log and "unverified" not in log
    out = capsys.readouterr().out
    assert "not judging: `false` was red before the fix" in out
    assert "not judging: no-such-tool missing" in out


def test_no_green_check_leaves_every_commit_unverified_with_why(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    monkeypatch.setattr(checks, "find", lambda root: [checks.Check(("false",))])

    fix.fix(root, only="TS-EXPECT-ERROR")

    log = git(root, "log", "--format=%b", f"main..{fix_branch(root)}")
    assert "unverified: `false` was red before the fix" in log
    assert fix.UNVERIFIED not in log


def test_a_converter_that_turns_the_checks_red_is_undone_and_handed_to_claude(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    # Green before the fix, red once a converter wrote its first file.
    breaks = checks.Check(("sh", "-c", "git diff --quiet HEAD || { echo 'tsc: TS2578'; exit 1; }"))
    monkeypatch.setattr(checks, "find", lambda root: [breaks])

    outcomes = fix.fix(root, only="TS-EXPECT-ERROR")

    assert [(found.rule, found.status) for found in outcomes] == [("TS-EXPECT-ERROR", "reverted")]
    assert "@ts-ignore" in (root / "a.ts").read_text()
    assert fix_branch(root) == ""  # nothing committed: no branch left
    log = checks.reverted(root)["TS-EXPECT-ERROR"]
    assert "tsc: TS2578" in log.read_text()
    report = score.score_repo(root)
    assert "TS-EXPECT-ERROR" in [found.rule for found in report.roadmap()]
    capsys.readouterr()
    roadmap.show_roadmap(report)
    assert f"kiln fix's converter broke a check, undone: {log}" in capsys.readouterr().out


@pytest.mark.parametrize(("built_before", "status"), [(True, "reverted"), (False, "fixed")])
def test_an_image_a_converter_touched_is_built(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, built_before: bool, status: str
) -> None:
    # T-159: a converter that breaks the image is undone; an image red before cannot judge.
    root = make(tmp_path, CONVERTED["NON-ROOT-CONTAINERS"])
    monkeypatch.setattr(checks, "find", lambda root: [checks.Check(("true",))])
    build = checks.Check(("sh", "-c", "echo 'useradd: not found'; exit 1"))
    monkeypatch.setattr(checks, "image_builds", lambda root, changed: [build])
    monkeypatch.setattr(fix, "_built_before", lambda root, check: built_before)

    outcomes = fix.fix(root, only="NON-ROOT-CONTAINERS")

    assert [found.status for found in outcomes] == [status]
    if built_before:
        assert "useradd: not found" in checks.reverted(root)["NON-ROOT-CONTAINERS"].read_text()
    else:
        assert "was red before the fix" in git(root, "log", "--format=%b", "-1", fix_branch(root))


def test_only_container_files_are_built(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(checks.shutil, "which", lambda name: f"/usr/bin/{name}")
    builds = IMAGE_BUILDS(tmp_path, ["api/Dockerfile", "web/app.Dockerfile", "README.md"])
    assert [build.argv[-3:] for build in builds] == [
        ("-f", "api/Dockerfile", "api"),
        ("-f", "web/app.Dockerfile", "web"),
    ]


def test_a_kiln_repo_is_checked_whole_before_and_after(tmp_path: Path) -> None:
    # `kiln check` alone looks at the branch's changes: a converter touching a file with older
    # debt (a Dockerfile the charter bans) would be blamed for it and undone.
    root = make(tmp_path, {".copier-answers.yml": "_commit: v0.4.5\n"})
    assert commands(root) == [("kiln", "check", "--all")]


def test_a_dry_run_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])

    fix.fix(root, dry_run=True, only="TS-EXPECT-ERROR")

    assert "+// @ts-expect-error" in capsys.readouterr().out
    assert git(root, "status", "--porcelain") == ""
    assert git(root, "branch", "--show-current").strip() == "main"
    assert "@ts-ignore" in (root / "a.ts").read_text()


def test_a_dirty_tree_is_left_alone_and_the_fix_starts_from_the_last_commit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    (root / "a.ts").write_text("// mine\n")

    fix.fix(root, only="TS-EXPECT-ERROR")

    assert "uncommitted changes left out" in capsys.readouterr().out
    assert (root / "a.ts").read_text() == "// mine\n"
    assert "@ts-expect-error" in git(root, "show", f"{fix_branch(root)}:a.ts")


def test_a_second_run_takes_over_its_branch_or_gets_a_suffix(tmp_path: Path) -> None:
    """A branch holding only `kiln fix` commits starts again from the last commit; one a person
    committed on is never touched."""
    root = make(tmp_path, CONVERTED["TS-EXPECT-ERROR"])
    fix.fix(root, only="TS-EXPECT-ERROR")
    first = fix_branch(root)
    fix.fix(root, only="TS-EXPECT-ERROR")
    assert fix_branch(root) == first
    assert git(root, "rev-list", "--count", f"main..{first}").strip() == "1"

    git(root, "switch", "-q", first)
    (root / "notes.md").write_text("mine\n")
    git(root, "add", "notes.md")
    git(root, "commit", "-q", "-m", "docs: my notes")
    git(root, "switch", "-q", "main")
    fix.fix(root, only="TS-EXPECT-ERROR")
    assert fix_branch(root) == f"{first}-2"
    assert "docs: my notes" in git(root, "log", "--format=%s", first)


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

    assert ".github/dependabot.yml" in git(root, "ls-tree", "-r", "--name-only", fix_branch(root))


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


def test_kiln_update_converts_in_place_and_spares_frozen_files(tmp_path: Path) -> None:
    """`kiln update`'s pass (T-159): the converters run in the tree, nothing committed, and a
    frozen file comes out as it went in."""
    frozen = ".github/workflows/deploy.yml"
    unpinned = "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n"
    root = make(tmp_path, {WORKFLOW: unpinned, frozen: unpinned, "README.md": "# a\n"})
    head = git(root, "rev-parse", "HEAD")
    assert "PINNED-ACTIONS" in fix.convert_in_place(root, [frozen])
    assert f"actions/checkout@{SHA}" in (root / WORKFLOW).read_text()
    assert (root / frozen).read_text() == unpinned
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "branch", "--show-current").strip() == "main"


def test_kiln_update_names_a_converter_that_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def offline(repo: str, ref: str) -> str:
        raise KilnError("GitHub unreachable")

    monkeypatch.setattr(resolve, "commit_of", offline)
    unpinned = "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v4\n"
    root = make(tmp_path, {WORKFLOW: unpinned, "README.md": "# a\n"})
    assert "PINNED-ACTIONS" not in fix.convert_in_place(root, [])
    assert "PINNED-ACTIONS left for kiln fix: GitHub unreachable" in capsys.readouterr().out


INJECTED = """on: pull_request_target
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ github.event.pull_request.title }}"
      - name: body
        env:
          TOKEN: ${{ secrets.T }}
        run: |
          echo "${{ github.event.issue.body }}" ${{ github.sha }}
      - run: echo "${{ github.event.issue.title || 'x' }}"
      - uses: actions/github-script@v7
        with:
          script: console.log("${{ github.event.issue.title }}")
      - shell: pwsh
        run: echo "${{ github.head_ref }}"
"""


def test_event_text_reaches_the_shell_through_env_and_the_rest_stays(tmp_path: Path) -> None:
    """T-173: a bare context read moves to the step's `env:` (its own, or one added after the
    script); an expression with more in it, `github-script` and pwsh stay for judgment."""
    root = make(tmp_path, {WORKFLOW: INJECTED})
    assert FIXERS["move_to_env"].convert(read_repo(root)) == [WORKFLOW]
    text = (root / WORKFLOW).read_text()
    assert (
        '      - run: echo "${PULL_REQUEST_TITLE}"\n'
        "        env:\n"
        "          PULL_REQUEST_TITLE: ${{ github.event.pull_request.title }}\n"
    ) in text
    assert (
        "        env:\n"
        "          ISSUE_BODY: ${{ github.event.issue.body }}\n"
        "          TOKEN: ${{ secrets.T }}\n"
        "        run: |\n"
        '          echo "${ISSUE_BODY}" ${{ github.sha }}\n'
    ) in text
    for kept in ("|| 'x' }}", 'console.log("${{ github', 'echo "${{ github.head_ref }}"'):
        assert kept in text
    outcome = detectors.workflow_injection(read_repo(root))
    # The three left, three lines lower for the `env:` lines added above them.
    assert outcome.locations == (f"{WORKFLOW}:15", f"{WORKFLOW}:18", f"{WORKFLOW}:20")


def test_a_windows_workflow_is_left_to_judgment(tmp_path: Path) -> None:
    windows = INJECTED.replace("runs-on: ubuntu-latest", "runs-on: windows-latest")
    root = make(tmp_path, {WORKFLOW: windows})
    assert FIXERS["move_to_env"].convert(read_repo(root)) == []


def test_event_text_already_in_env_is_not_an_injection(tmp_path: Path) -> None:
    safe = (
        'jobs:\n  a:\n    steps:\n      - run: echo "$TITLE"\n        env:\n'
        "          TITLE: ${{ github.event.pull_request.title }}\n"
    )
    root = make(tmp_path, {WORKFLOW: safe})
    assert detectors.workflow_injection(read_repo(root)).status == detectors.PASS


def test_missing_jobs_come_as_workflows_of_their_own(tmp_path: Path) -> None:
    """Lint and tests as the repo declares them, folder by folder, installed from their lock;
    the audit also every Monday. The repo's own workflow is left as it is."""
    root = make(
        tmp_path,
        {
            WORKFLOW: BUILD_ONLY,
            "pyproject.toml": "[tool.ruff]\n[tool.pytest.ini_options]\n",
            "requirements.txt": "flask\n",
            "web/package.json": '{"scripts": {"lint": "eslint", "test": "vitest"}}',
            "web/package-lock.json": "{}",
        },
    )
    lint = FIXERS["add_lint_job"].convert(read_repo(root))
    tests = FIXERS["add_test_job"].convert(read_repo(root))
    audit = FIXERS["add_audit"].convert(read_repo(root))
    assert (lint, tests, audit) == (
        [".github/workflows/lint.yml"],
        [".github/workflows/tests.yml"],
        [".github/workflows/audit.yml"],
    )
    workflows = root / ".github/workflows"
    assert (
        (workflows / "lint.yml")
        .read_text()
        .endswith(
            "      - run: uvx ruff check\n      - run: cd web && npm ci\n"
            "      - run: cd web && npm run lint\n"
        )
    )
    assert (
        "      - run: pip install -r requirements.txt pytest\n"
        in (workflows / "tests.yml").read_text()
    )
    audited = (workflows / "audit.yml").read_text()
    assert '    - cron: "0 6 * * 1"\n' in audited
    assert audited.endswith(
        "      - run: uvx pip-audit -r requirements.txt\n"
        "      - run: cd web && npm audit --omit=dev --audit-level=high\n"
    )
    assert (root / WORKFLOW).read_text() == BUILD_ONLY


def test_no_job_is_added_without_a_github_ci(tmp_path: Path) -> None:
    root = make(tmp_path, {".gitlab-ci.yml": "build:\n  script: make\n", "uv.lock": ""})
    assert FIXERS["add_audit"].convert(read_repo(root)) == []


def test_a_tracked_env_leaves_git_not_the_disk(tmp_path: Path) -> None:
    root = make(
        tmp_path,
        {".env": "SECRET=abc\n# a note\nexport OTHER = 2\n", ".gitignore": "node_modules"},
    )
    assert FIXERS["untrack_env"].convert(read_repo(root)) == [".gitignore", ".env.example"]
    assert (root / ".env").read_text().startswith("SECRET=abc")
    assert git(root, "ls-files", ".env") == ""
    assert (root / ".env.example").read_text() == "SECRET=\nOTHER=\n"
    assert (root / ".gitignore").read_text().startswith("node_modules\n.env\n.env.local\n")


def test_a_rule_an_earlier_converter_closed_is_left_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The minimal CI runs the linters: LINT-IN-CI, next in the plan, adds no second workflow."""
    root = make(tmp_path, {"pyproject.toml": "[tool.ruff]\n", "uv.lock": "", "a.py": "x = 1\n"})
    monkeypatch.setattr(
        fix, "plan", lambda root, only=None: [RULES["CI-PRESENT"], RULES["LINT-IN-CI"]]
    )
    outcomes = {found.rule: found for found in fix.fix(root)}
    assert outcomes["CI-PRESENT"].status == "fixed"
    assert outcomes["LINT-IN-CI"].note == fix.CLOSED
    assert not (root / ".github/workflows/lint.yml").exists()


def test_the_throwaway_worktree_has_what_the_checks_need(tmp_path: Path) -> None:
    """The installed Node dependencies linked, the local settings copied, at the root and one
    folder down; the worktree gone afterwards."""
    root = make(tmp_path / "repo", {".gitignore": ".env\nnode_modules\n", "web/package.json": "{}"})
    (root / ".env").write_text("A=1\n")
    (root / "web/node_modules/x").mkdir(parents=True)
    with fix.scratch_worktree(root, "--detach") as copy:
        assert (copy / ".env").read_text() == "A=1\n"
        assert (copy / "web/node_modules").resolve() == (root / "web/node_modules").resolve()
        assert (copy / "web/node_modules/x").is_dir()
    assert not copy.exists()
    assert (root / "web/node_modules/x").is_dir()
