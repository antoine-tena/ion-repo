import importlib.util
import io
import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

HOOK_PATH = Path(__file__).resolve().parent.parent / "plugins/repo/hooks/session_start.py"
CHANGELOG = """# Changes

## v0.4.0 — 2026-10-20
- **Breaking**: the charter is in English.
- `ion repo new` asks fewer questions.

## v0.3.5 — 2026-10-17
- Faster `ion repo status`.

## v0.3.4 — 2026-10-16
- **Cassant** : old change, already applied.
"""
ION_REPO_ANSWERS = "_commit: 8e6427b\n_src_path: https://github.com/antoine-tena/ion-repo.git\n"


def load_hook() -> ModuleType:
    spec = importlib.util.spec_from_file_location("session_start", HOOK_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def hook(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """The hook on a fake ion-repo repo, without real network or installed tool."""
    module = load_hook()
    monkeypatch.setattr(module, "git_root", lambda cwd: tmp_path / "myapp")
    monkeypatch.setattr(module, "kiln_repo", lambda cwd: (tmp_path / "myapp", "8e6427b"))
    monkeypatch.setattr(module, "installed_kiln", lambda: ("git", "ancien"))
    monkeypatch.setattr(module, "fetch_changelog", lambda tag: CHANGELOG)
    return module


def released(tag: str = "v0.4.0", commit: str = "nouveau") -> Callable[[], tuple[str, str]]:
    return lambda: (tag, commit)


def test_answers_are_read_without_yaml() -> None:
    hook = load_hook()

    assert hook.answer(ION_REPO_ANSWERS, "_commit") == "8e6427b"
    assert (
        hook.answer(ION_REPO_ANSWERS, "_src_path") == "https://github.com/antoine-tena/ion-repo.git"
    )
    assert hook.answer(ION_REPO_ANSWERS, "absent") == ""


def test_an_update_merged_on_the_integration_branch_is_not_offered_again(
    tmp_path: Path,
) -> None:
    # A branch cut before a teammate merged `ion repo update` into develop (#50).
    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True)

    git("init", "-q", "-b", "develop")
    answers = tmp_path / ".copier-answers.yml"
    answers.write_text(ION_REPO_ANSWERS.replace("8e6427b", "v0.4.4-63-gb2b0bb5"))
    git("add", ".")
    git("commit", "-qm", "update")
    git("update-ref", "refs/remotes/origin/develop", "HEAD")
    hook = load_hook()

    assert hook.integrated_commit(tmp_path, "e63f9f0") == "v0.4.4-63-gb2b0bb5"
    assert hook.integrated_commit(tmp_path, "v0.4.5-rc.1") == "v0.4.5-rc.1"
    git("update-ref", "-d", "refs/remotes/origin/develop")
    assert hook.integrated_commit(tmp_path, "e63f9f0") == "e63f9f0"


def test_releases_order_by_number_not_by_text() -> None:
    hook = load_hook()

    assert hook.release_key("v0.10.0") > hook.release_key("v0.9.3")
    assert hook.release_key("v0.4.0") > hook.release_key("v0.4.0-rc.3")
    assert hook.release_key("v0.4.0-2-gabc1234") == (0, 4, 0, hook.FINAL)
    assert hook.release_key("8e6427b") is None
    assert hook.is_repo_late("8e6427b", "v0.3.0")
    assert hook.is_repo_late("v0.4.0-rc.1", "v0.4.0")
    assert not hook.is_repo_late("v0.4.0", "v0.4.0")


def test_refusals_push_the_question_back_further_and_further(hook: ModuleType) -> None:
    state: dict[str, Any] = {}
    asked_at = []
    for session in range(1, 110):
        if hook.instructions(".", state, release=released()):
            asked_at.append(session)
            hook.reminders.record(state, hook.TOOL_KEY, "no")

    assert asked_at == [1, 6, 16, 46, 96]


def test_after_four_refusals_uninstalling_is_offered(hook: ModuleType) -> None:
    state: dict[str, Any] = {}
    for _ in range(4):
        hook.reminders.record(state, hook.TOOL_KEY, "no")
    state["questions"]["tool"]["next"] = 0

    assert "Uninstall ion-repo" in hook.instructions(".", state, release=released())


def test_repo_question_follows_a_tool_update(hook: ModuleType) -> None:
    message = hook.instructions(".", {}, release=released())

    assert "The ion-repo tool installed" in message
    assert "Once the tool is updated successfully" in message
    assert "`/repo:update` with the argument `tool`" in message
    assert "`/repo:update` with the argument `repo`" in message


def test_refused_tool_update_also_silences_the_repo(hook: ModuleType) -> None:
    state: dict[str, Any] = {}
    hook.instructions(".", state, release=released())
    hook.reminders.record(state, hook.TOOL_KEY, "no")

    assert hook.instructions(".", state, release=released()) == ""


def test_up_to_date_tool_asks_only_for_the_repo(
    hook: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(hook, "installed_kiln", lambda: ("git", "nouveau"))

    message = hook.instructions(".", {}, release=released())

    assert message.startswith("ion-repo v0.4.0 is out; myapp starts from 8e6427b")
    monkeypatch.setattr(hook, "kiln_repo", lambda cwd: (Path("myapp"), "v0.4.0"))
    assert hook.instructions(".", {}, release=released()) == ""


def test_no_release_means_no_question(hook: ModuleType) -> None:
    assert hook.instructions(".", {}, release=lambda: None) == ""


def test_outside_kiln_repos_the_hook_says_nothing(
    hook: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(hook, "kiln_repo", lambda cwd: None)
    state: dict[str, Any] = {}

    assert [hook.instructions(".", state, release=released()) for _ in range(20)] == [""] * 20
    assert state == {}


def test_the_link_of_kiln_0_3_is_removed_but_not_a_real_folder(tmp_path: Path) -> None:
    hook = load_hook()
    linked, kept = tmp_path / "linked", tmp_path / "kept"
    (linked / ".claude").mkdir(parents=True)
    (linked / ".claude/kiln").symlink_to(tmp_path / "plugins/base", target_is_directory=True)
    (kept / ".claude/kiln").mkdir(parents=True)

    hook.remove_legacy_link(linked)
    hook.remove_legacy_link(kept)

    assert not (linked / ".claude/kiln").is_symlink()
    assert (kept / ".claude/kiln").is_dir()


def fake_tool(tool_dir: Path, name: str, dist_info: str, direct_url: str | None) -> Path:
    """The tool's `site-packages`."""
    metadata = tool_dir / name / "lib/python3.14/site-packages" / dist_info
    metadata.mkdir(parents=True)
    (metadata / "METADATA").write_text("Metadata-Version: 2.4\nName: kiln-cli\nVersion: 0.4.0\n")
    if direct_url is not None:
        (metadata / "direct_url.json").write_text(direct_url)
    return metadata.parent


def uv_tool_dir(module: ModuleType, tool_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def run(*command: str) -> subprocess.CompletedProcess[str]:
        assert command == ("uv", "tool", "dir")
        return subprocess.CompletedProcess(command, 0, stdout=f"{tool_dir}\n")

    monkeypatch.setattr(module, "run", run)


def test_a_pypi_install_is_read_from_its_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    fake_tool(tmp_path, "kiln-cli", "kiln_cli-0.4.0.dist-info", None)
    uv_tool_dir(hook, tmp_path, monkeypatch)

    assert hook.installed_kiln() == ("pypi", "v0.4.0")
    assert not hook.has_legacy_tool()
    assert not hook.is_tool_outdated(("pypi", "v0.4.0"), "v0.4.0", "abc")
    assert hook.is_tool_outdated(("pypi", "v0.4.0"), "v0.4.1", "abc")


def test_an_ion_repo_install_is_found_and_upgraded_under_its_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    fake_tool(tmp_path, "ion-repo", "ion_repo-0.4.0.dist-info", None)
    uv_tool_dir(hook, tmp_path, monkeypatch)

    assert hook.installed_kiln() == ("pypi", "v0.4.0")
    assert hook.tool_update_command(("pypi", "v0.4.0"), "v0.4.1").startswith(
        'uv tool install --force "ion-repo==0.4.1" && '
    )


def test_a_tester_s_kiln_cli_tool_is_replaced_by_ion_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    fake_tool(tmp_path, "kiln-cli", "kiln_cli-0.4.0.dist-info", None)
    uv_tool_dir(hook, tmp_path, monkeypatch)

    # Installed again after the uninstall, which removes the commands both tools carry.
    assert hook.tool_update_command(("pypi", "v0.4.0"), "v0.4.1").startswith(
        'uv tool install ion-sh && uv tool install --force "ion-repo==0.4.1" && '
        'uv tool uninstall kiln-cli && uv tool install --force "ion-repo==0.4.1" && '
    )


def test_the_old_kiln_tool_is_still_found_and_removed_on_update(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    fake_tool(
        tmp_path, "kiln", "kiln-0.3.0.dist-info", '{"url": "x", "vcs_info": {"commit_id": "c0"}}'
    )
    uv_tool_dir(hook, tmp_path, monkeypatch)

    assert hook.installed_kiln() == ("git", "c0")
    command = hook.tool_update_command(("git", "c0"), "v0.4.0")
    assert command.startswith('uv tool uninstall kiln && uv tool install --force "git+')
    # A copy of a checkout is replaced by the release: only a release updates a repo.
    command = hook.tool_update_command(("directory", "v0.3.4-105-gd800ca1"), "v0.4.0-rc.1")
    assert command.startswith(
        'uv tool uninstall kiln && uv tool install --force "git+https://github.com/'
        'antoine-tena/ion-repo@v0.4.0-rc.1"'
    )


def test_promoted_versions_come_from_pypi_and_candidates_from_github(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    uv_tool_dir(hook, tmp_path, monkeypatch)

    assert hook.tool_update_command(("pypi", "v0.4.0"), "v0.4.1").startswith(
        'uv tool install --force "ion-repo==0.4.1" && '
    )
    assert hook.tool_update_command(None, "v0.4.1").startswith('uv tool install --force "ion-repo')
    assert '"git+https://github.com/antoine-tena/ion-repo@v0.5.0-rc.1"' in hook.tool_update_command(
        ("pypi", "v0.4.1"), "v0.5.0-rc.1"
    )


def test_the_logo_is_the_one_of_kiln() -> None:
    from ion_repo import banner

    hook = load_hook()

    assert hook.LOGO == banner.LOGO
    assert {key: color.true_color for key, color in banner.LOGO_COLORS.items()} == hook.LOGO_COLORS


def test_the_user_sees_the_logo_above_the_question(
    hook: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)

    found = hook.offer(".", {}, release=released())

    assert found is not None
    assert found.notice.startswith("\n")
    assert hook.render_logo()[0].rstrip() in found.notice
    assert "ion-repo v0.4.0\x1b[0m  \x1b[38;2;140;140;135mupdate available" in found.notice
    assert "breaking\x1b[0m The charter is in English" in found.notice
    assert "ion repo new asks fewer questions" in found.notice


def test_without_colors_the_notice_is_one_line(
    hook: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr(hook, "installed_kiln", lambda: ("git", "nouveau"))
    monkeypatch.setattr(hook, "kiln_repo", lambda cwd: (Path("myapp"), "v0.3.4"))

    found = hook.offer(".", {}, release=released())

    assert found is not None
    assert found.notice == (
        "ion-repo v0.4.0 · update available · The charter is in English · "
        "ion repo new asks fewer questions · Faster ion repo status"
    )


def test_the_notice_waits_for_the_first_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    spec = importlib.util.spec_from_file_location(
        "first_prompt", HOOK_PATH.with_name("first_prompt.py")
    )
    assert spec is not None and spec.loader is not None
    first_prompt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(first_prompt)
    monkeypatch.setattr(hook, "NOTICES_DIR", tmp_path)
    monkeypatch.setattr(first_prompt, "NOTICES_DIR", tmp_path)
    hook.save_notice("abc", "the logo")

    def prompt() -> str:
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"session_id": "abc"})))
        output = io.StringIO()
        monkeypatch.setattr("sys.stdout", output)
        first_prompt.main()
        return output.getvalue()

    assert json.loads(prompt()) == {"systemMessage": "the logo"}
    assert prompt() == ""


def test_changes_are_shortened_to_a_headline() -> None:
    hook = load_hook()

    assert hook.headline("**Cassant** : le suivi passe en anglais") == "Le suivi passe en anglais"
    assert hook.headline("`ion-repo` répond en 0,12 s (commandes à la demande)") == (
        "ion-repo répond en 0,12 s"
    )
    assert hook.headline("Le modèle suit l'outil installé : `ion repo update` applique…") == (
        "Le modèle suit l'outil installé"
    )
    assert hook.headline("`ion repo waive` : ajoute une dérogation") == (
        "ion repo waive : ajoute une dérogation"
    )
    long = "`ion repo new` sans `gh`, ou hors terminal sans connexion, crée le projet en local"
    assert hook.headline(long) == "ion repo new sans gh, ou hors terminal sans connexion…"


def test_fixes_come_after_the_other_changes() -> None:
    hook = load_hook()
    changelog = "## v0.3.5 — 2026-10-17\n- Correctifs : a fix.\n- A feature.\n"

    shown = hook.headlines(hook.changes_between("v0.3.4", "v0.3.5", changelog))

    assert shown == [(False, "A feature"), (False, "Correctifs : a fix")]


def test_the_question_only_says_the_move(hook: ModuleType) -> None:
    message = hook.instructions(".", {}, release=released())

    assert '"Update ion-repo to v0.4.0?"' in message
    assert '"Update myapp from 8e6427b to v0.4.0?"' in message
    assert "the charter is in English" not in message
    assert 'If "Update": skill `/repo:update` with the argument `tool`' in message


def test_breaking_changes_of_skipped_releases_only() -> None:
    hook = load_hook()

    changes = hook.changes_between("v0.3.4", "v0.4.0-rc.1", CHANGELOG)

    assert changes.passed == ["v0.4.0", "v0.3.5"]
    assert changes.breaking == ["**Breaking**: the charter is in English."]
    assert hook.changes_between(None, "v0.3.5", CHANGELOG).passed == ["v0.3.5"]


def test_a_checkout_copy_is_up_to_date_only_when_it_is_the_release(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    site = fake_tool(
        tmp_path,
        "kiln-cli",
        "kiln_cli-0.4.0.dist-info",
        '{"url": "file:///src/ion_repo", "dir_info": {}}',
    )
    uv_tool_dir(hook, tmp_path, monkeypatch)

    # A copy from before the record: unknown, so offered the release.
    assert hook.installed_kiln() == ("directory", "")
    assert hook.is_tool_outdated(("directory", ""), "v0.4.0-rc.1", "c1")

    (site / "ion_repo").mkdir()
    (site / "ion_repo/_build.json").write_text('{"describe": "v0.3.4-105-gd800ca1"}')
    install = hook.installed_kiln()
    assert install == ("directory", "v0.3.4-105-gd800ca1")
    assert hook.is_tool_outdated(install, "v0.4.0-rc.1", "c1")
    assert not hook.is_tool_outdated(("directory", "v0.4.0-rc.1"), "v0.4.0-rc.1", "c1")


def fake_ci(
    hook: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    runs: list[dict[str, str]] | None,
    steps: int = 3,
) -> None:
    """git says the integration branch is develop; gh lists `runs` (None: gh missing), each of
    their jobs having run `steps` steps."""
    real_run: Callable[..., subprocess.CompletedProcess[str]] = hook.run

    def run(*command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        if command[0] == "gh":
            if runs is None:
                raise FileNotFoundError("gh")
            if command[1:3] == ("run", "view"):
                jobs = [{"name": "tests", "steps": [{"name": "step"}] * steps}]
                return subprocess.CompletedProcess(command, 0, stdout=json.dumps({"jobs": jobs}))
            return subprocess.CompletedProcess(command, 0, stdout=json.dumps(runs))
        if "origin/develop" in command:
            return subprocess.CompletedProcess(command, 0, stdout="abc\n")
        return real_run(*command, cwd=cwd)

    monkeypatch.setattr(hook, "run", run)


def ci_run(workflow: str, status: str, conclusion: str, title: str = "Merge") -> dict[str, str]:
    return {
        "workflowName": workflow,
        "status": status,
        "conclusion": conclusion,
        "displayTitle": title,
        "url": f"https://github.com/o/r/actions/runs/{title}",
    }


def test_a_red_integration_branch_is_said_before_any_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "charter.toml").write_text("")
    assert hook.follows_kiln(tmp_path)

    # The last finished run of each workflow counts; a running one waits for its verdict.
    fake_ci(
        hook,
        monkeypatch,
        [
            ci_run("kiln", "in_progress", "", "next"),
            ci_run("kiln", "completed", "failure", "fix: x"),
            ci_run("kiln", "completed", "success", "older"),
            ci_run("pages", "completed", "success"),
        ],
    )
    said = hook.red_ci(tmp_path)
    assert said.startswith('The CI of `develop` is red: kiln on "fix: x"')
    assert "tell the user" in said and "pages" not in said

    fake_ci(hook, monkeypatch, [ci_run("kiln", "completed", "success", "fix: x")])
    assert hook.red_ci(tmp_path) == ""
    fake_ci(hook, monkeypatch, None)
    assert hook.red_ci(tmp_path) == ""


def test_a_run_github_never_started_is_not_a_failure_to_fix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "charter.toml").write_text("")

    # Billing or a spending limit: GitHub fails every job before its first step.
    fake_ci(hook, monkeypatch, [ci_run("CI", "completed", "failure", "Merge")], steps=0)
    said = hook.red_ci(tmp_path)
    assert said.startswith("The CI of `develop` did not run: GitHub started none of the jobs of CI")
    assert "nothing to fix" in said and "ion repo ci" in said and "is red" not in said


def test_the_red_ci_is_only_said_in_repos_kiln_looks_after(tmp_path: Path) -> None:
    hook = load_hook()
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)

    assert not hook.follows_kiln(tmp_path)
    (tmp_path / "src/ion_repo").mkdir(parents=True)
    (tmp_path / "src/ion_repo/versions.py").write_text("")
    assert hook.follows_kiln(tmp_path)


def test_a_red_local_ci_is_read_from_its_git_note(tmp_path: Path) -> None:
    hook = load_hook()
    origin, repo = tmp_path / "origin.git", tmp_path / "repo"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "develop", str(origin)], check=True)
    subprocess.run(["git", "clone", "-q", str(origin), str(repo)], check=True)
    git = ["git", "-C", str(repo)]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "start"], check=True)
    subprocess.run([*git, "push", "-q", "origin", "develop"], check=True)
    subprocess.run([*git, "config", "statusline.ci", "locale"], check=True)

    assert hook.red_ci(repo) == ""  # never replayed: nothing to say
    note = ["notes", "--ref=refs/notes/ci", "add", "-f", "-m"]
    subprocess.run([*git, *note, "kiln ci: failure\nbackend: tests", "origin/develop"], check=True)
    assert hook.red_ci(repo).startswith("The CI of `develop` is red: `ion repo ci` failed")
    subprocess.run([*git, *note, "kiln ci: success", "origin/develop"], check=True)
    assert hook.red_ci(repo) == ""


def test_every_start_recalls_that_errors_may_come_from_kiln(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    hook = load_hook()
    monkeypatch.setattr(hook, "git_root", lambda cwd: None)
    monkeypatch.setattr(hook.place, "context", lambda cwd: "")
    monkeypatch.setattr(sys, "argv", ["session_start.py"])
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"source": "clear", "cwd": "/"}'))

    hook.main()

    said = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert said == f"{hook.ERROR_ORIGIN}\n\n{hook.SKILL_FRAME}"


def test_skill_frame_has_kiln_frame_draw_cornerless_rules() -> None:
    hook = load_hook()
    assert "`ion-repo frame <plugin> <skill>`" in hook.SKILL_FRAME
    assert not set("╔╗╚╝") & set(hook.SKILL_FRAME)


def beta_machine(
    hook: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, place: str = "kiln"
) -> Path:
    """A machine on the beta channel, with ion-repo's checkout in its code directory, at `place`."""
    checkout = tmp_path / "code" / place
    (checkout / "src/ion_repo").mkdir(parents=True)
    (checkout / "src/ion_repo/versions.py").write_text("")
    config = tmp_path / "config.toml"
    config.write_text(f'channel = "beta"\ncode_dir = "{tmp_path / "code"}"\n')
    monkeypatch.setattr(hook, "CONFIG_PATH", config)
    return checkout


def test_on_the_beta_channel_the_editable_checkout_is_never_outdated(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    checkout = beta_machine(hook, tmp_path, monkeypatch)
    fake_tool(
        tmp_path / "tools",
        "kiln-cli",
        "kiln_cli-0.4.4.dist-info",
        json.dumps({"url": f"file://{checkout}", "dir_info": {"editable": True}}),
    )
    uv_tool_dir(hook, tmp_path / "tools", monkeypatch)

    assert hook.follows_candidates()
    assert hook.installed_kiln() == ("editable", str(checkout))
    assert hook.tool_status() == "up to date"


def test_on_the_beta_channel_the_checkout_may_sit_in_a_folder_of_the_code_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    checkout = beta_machine(hook, tmp_path, monkeypatch, place="tools/ion-repo")
    fake_tool(
        tmp_path / "uv-tools",
        "kiln-cli",
        "kiln_cli-0.4.4.dist-info",
        json.dumps({"url": f"file://{checkout}", "dir_info": {"editable": True}}),
    )
    uv_tool_dir(hook, tmp_path / "uv-tools", monkeypatch)

    assert hook.kiln_checkout() == checkout
    assert hook.tool_status() == "up to date"
    # A link left at the old place, while open sessions still read their hooks there.
    (tmp_path / "code/kiln").symlink_to(checkout)
    assert hook.kiln_checkout() == checkout
    assert hook.tool_status() == "up to date"


def test_on_the_beta_channel_a_release_is_replaced_by_the_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    checkout = beta_machine(hook, tmp_path, monkeypatch)
    monkeypatch.setattr(hook, "installed_kiln", lambda: ("pypi", "v0.4.4"))
    monkeypatch.setattr(hook, "has_legacy_tool", lambda: False)

    assert hook.tool_status().startswith(f"uv tool install --force --editable {checkout} && ")


def test_on_the_beta_channel_without_checkout_the_tool_follows_github_develop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    config = tmp_path / "config.toml"
    config.write_text(f'canal = "beta"\ndossier_code = "{tmp_path}"\n')
    monkeypatch.setattr(hook, "CONFIG_PATH", config)
    monkeypatch.setattr(hook, "has_legacy_tool", lambda: False)
    monkeypatch.setattr(hook, "installed_pypi_name", lambda: "ion-repo")

    def run(*command: str) -> subprocess.CompletedProcess[str]:
        assert command[-1] == "refs/heads/develop"
        return subprocess.CompletedProcess(command, 0, stdout="c2\trefs/heads/develop\n")

    monkeypatch.setattr(hook, "run", run)

    assert not hook.is_beta_tool_outdated(("git", "c2"))
    assert hook.is_beta_tool_outdated(("git", "c1"))
    assert "git+https://github.com/antoine-tena/ion-repo@develop" in hook.tool_update_command(
        ("git", "c1"), ""
    )


def test_tool_update_moves_an_installed_plugin_to_the_marketplace_version(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # `claude plugin install` is a no-op for a plugin already installed (#58); `install
    # --machine` installs it when missing, kiln's catalogue moved to ion-repo's.
    hook = load_hook()
    uv_tool_dir(hook, tmp_path, monkeypatch)

    command = hook.tool_update_command(("pypi", "v0.4.0"), "v0.4.1")
    assert command.endswith(
        "ion-repo install --machine && claude plugin marketplace update ion-repo "
        "&& claude plugin update repo@ion-repo --scope user"
    )


# --- sessions kept by /repo:pause (ion-repo#T-344)
# -----------------------------------------------------


def test_a_paused_session_is_listed_at_the_next_start_then_leaves_the_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`ion repo pause` writes the place; the next start lists it; resumed, or its branch deleted,
    it is gone."""
    from ion_repo import pause

    hook = load_hook()
    paused = sys.modules["paused"]
    sessions = tmp_path / "sessions"
    monkeypatch.setattr(pause, "SESSIONS_DIR", sessions)
    monkeypatch.setattr(paused, "SESSIONS_DIR", sessions)
    repo = tmp_path / "shop"
    repo.mkdir()
    for command in (
        ["init", "-q", "-b", "feat/cart"],
        ["commit", "-q", "--allow-empty", "-m", "a"],
    ):
        subprocess.run(["git", *command], cwd=repo, check=True)
    for session, name in (("aaa", "cart: totals"), ("bbb", "cart: coupons")):
        monkeypatch.setenv(pause.SESSION_VARIABLE, session)
        pause.pause(repo, name, "merge feat/cart")
    capsys.readouterr()

    shown = hook.paused_sessions({"source": "startup", "session_id": "new"})
    assert shown.startswith("Paused sessions (/repo:pause):")
    assert "⏸ cart: totals  (shop · feat/cart, 1 min ago)" in shown
    assert "    next: merge feat/cart\n    claude --resume aaa" in shown

    assert hook.paused_sessions({"source": "resume", "session_id": "aaa"}) == ""
    assert "cart: totals" not in hook.paused_sessions({"source": "startup", "session_id": "new"})

    subprocess.run(["git", "switch", "-q", "-c", "main"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "-q", "-D", "feat/cart"], cwd=repo, check=True)
    assert hook.paused_sessions({"source": "startup", "session_id": "new"}) == ""
    assert list(sessions.iterdir()) == []


def test_pause_needs_a_claude_code_session(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ion_repo import pause
    from ion_repo.shell import KilnError

    monkeypatch.delenv(pause.SESSION_VARIABLE, raising=False)
    with pytest.raises(KilnError, match="no Claude Code session"):
        pause.pause(tmp_path, "x", "")


def test_on_the_beta_channel_the_checkout_may_sit_in_a_tool_folder_of_a_family(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook = load_hook()
    checkout = beta_machine(hook, tmp_path, monkeypatch, place="family/ion-repo/ion-repo")

    assert hook.kiln_checkout() == checkout


# --- other sessions on the same repo (ion-repo#T-384)
# ------------------------------------------------------


def _session(
    claude: Path, name: str, cwd: Path, *, pid: int | None, age: float = 0, branch: str = "develop"
) -> None:
    project = claude / "projects" / "launch"
    project.mkdir(parents=True, exist_ok=True)
    transcript = project / f"{name}.jsonl"
    lines = [{"cwd": str(cwd), "gitBranch": branch, "type": "user"}, {"type": "last-prompt"}]
    transcript.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    os.utime(transcript, (1_000_000 - age, 1_000_000 - age))
    if pid is not None:
        records = claude / "sessions"
        records.mkdir(exist_ok=True)
        (records / f"{pid}.json").write_text(json.dumps({"sessionId": name}), encoding="utf-8")


def _other_sessions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[ModuleType, Path, Path]:
    load_hook()
    others = sys.modules["others"]
    claude = tmp_path / "claude"
    monkeypatch.setattr(others, "CLAUDE_DIR", claude)
    repo = tmp_path / "shop"
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return others, claude, repo


def test_a_running_session_at_work_in_a_worktree_of_the_repo_is_told(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    others, claude, repo = _other_sessions(monkeypatch, tmp_path)
    worktree = repo / ".claude" / "worktrees" / "cart"
    _session(claude, "aaa", worktree, pid=os.getpid(), age=60, branch="feat/cart")

    told = others.context(str(repo), "mine", now=1_000_000)

    assert "[OTHER-SESSION]" in told
    assert "feat/cart" in told
    assert "aaa" in told


def test_a_session_written_under_two_launch_folders_is_told_once(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    others, claude, repo = _other_sessions(monkeypatch, tmp_path)
    _session(claude, "aaa", repo, pid=os.getpid(), age=120, branch="develop")
    worktree_folder = claude / "projects" / "launch--claude-worktrees-cart"
    worktree_folder.mkdir()
    line = json.dumps({"cwd": str(repo), "gitBranch": "feat/cart"}) + "\n"
    (worktree_folder / "aaa.jsonl").write_text(line, encoding="utf-8")
    os.utime(worktree_folder / "aaa.jsonl", (1_000_000 - 60, 1_000_000 - 60))

    told = others.context(str(repo), "mine", now=1_000_000)

    assert told.count("session aaa") == 1
    assert "feat/cart" in told


@pytest.mark.parametrize(
    ("name", "place", "pid", "age"),
    [
        ("mine", "shop", "self", 60),  # the session itself
        ("aaa", "shop", "self", 11 * 60),  # silent for too long
        ("aaa", "shop", None, 60),  # closed: no record of it
        ("aaa", "shop", "dead", 60),  # closed: its process is gone
        ("aaa", "shop-other", "self", 60),  # another repo, even with the same prefix
    ],
)
def test_a_session_not_at_work_on_this_repo_is_not_told(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    name: str,
    place: str,
    pid: str | None,
    age: int,
) -> None:
    others, claude, repo = _other_sessions(monkeypatch, tmp_path)
    process = None
    if pid == "self":
        process = os.getpid()
    elif pid == "dead":
        ended = subprocess.Popen(["true"])
        ended.wait()
        process = ended.pid
    _session(claude, name, tmp_path / place, pid=process, age=age)

    assert others.context(str(repo), "mine", now=1_000_000) == ""


def test_other_sessions_are_said_at_start_and_resume_only(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    others, claude, repo = _other_sessions(monkeypatch, tmp_path)
    hook = sys.modules["session_start"] if "session_start" in sys.modules else load_hook()
    _session(claude, "aaa", repo, pid=os.getpid())
    monkeypatch.setattr(others.time, "time", lambda: 1_000_000)

    for source, expected in (
        ("startup", True),
        ("resume", True),
        ("clear", False),
        ("compact", False),
    ):
        payload = {"source": source, "cwd": str(repo), "session_id": "mine"}
        assert bool(hook.other_sessions(payload)) is expected


def test_outside_a_repo_nothing_is_told(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    others, _, _ = _other_sessions(monkeypatch, tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))

    assert others.context(str(outside), "mine") == ""
