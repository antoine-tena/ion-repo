"""`ion repo install` outside a repo: ion-repo for the whole machine, only what is missing."""

import json
from pathlib import Path

import pytest

from ion_repo import cli, install
from ion_repo.config import UserConfig
from ion_repo.stack import Stack


@pytest.fixture
def machine(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[list[str]]:
    """A machine with uv and claude, ion-repo's settings recorded; the commands run are listed."""
    commands: list[list[str]] = []
    monkeypatch.setattr(install, "CLAUDE_SETTINGS", tmp_path / "settings.json")
    monkeypatch.setattr(install, "KNOWN_MARKETPLACES", tmp_path / "known_marketplaces.json")
    monkeypatch.setattr(install, "load_config", lambda: UserConfig(system="linux"))
    monkeypatch.setattr(install, "ensure_statusline", lambda config: config)
    monkeypatch.setattr(install, "run", lambda command, cwd: commands.append(command))
    monkeypatch.setattr("ion_repo.install.shutil.which", lambda name: f"/usr/bin/{name}")
    return commands


def test_a_bare_machine_gets_the_command_the_catalogue_and_the_plugin(
    machine: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "ion_repo.install.shutil.which",
        lambda name: None if name in ("ion-repo", "kiln") else f"/usr/bin/{name}",
    )

    install.install_machine()

    assert machine == [
        ["uv", "tool", "install", "ion-repo"],
        ["claude", "plugin", "marketplace", "add", "antoine-tena/ion-repo"],
        ["claude", "plugin", "install", "repo@ion-repo", "--scope", "user"],
    ]


def test_run_again_it_does_nothing(machine: list[list[str]]) -> None:
    install.KNOWN_MARKETPLACES.write_text(json.dumps({"ion-repo": {}}))
    install.CLAUDE_SETTINGS.write_text(json.dumps({"enabledPlugins": {"repo@ion-repo": True}}))

    install.install_machine()

    assert machine == []


def test_without_claude_code_the_plugins_wait(
    machine: list[list[str]], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "ion_repo.install.shutil.which",
        lambda name: None if name == "claude" else f"/usr/bin/{name}",
    )

    install.install_machine()

    assert machine == []
    assert "Claude Code not found" in capsys.readouterr().out


def test_outside_a_repo_install_sets_up_the_machine(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[str] = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(install, "install_machine", lambda: calls.append("machine"))
    monkeypatch.setattr("sys.argv", ["kiln", "install"])

    try:
        cli.main()
    except SystemExit as exit_request:
        assert not exit_request.code
    assert calls == ["machine"]


def test_git_hooks_need_their_configuration(machine: list[list[str]], tmp_path: Path) -> None:
    install.install_git_hooks(tmp_path)
    assert machine == []

    (tmp_path / ".pre-commit-config.yaml").write_text("repos: []\n")
    install.install_git_hooks(tmp_path)
    assert machine == [["pre-commit", "install"]]


@pytest.mark.parametrize(
    ("stack", "hint"),
    [
        (Stack("django", "nuxt", False), "Run the project: ion repo dev"),
        (Stack("cli", "none", False), "Run the project: cd backend && uv run demo --help"),
        (Stack("cli", "none", False, backend_dir="."), "Run the project: uv run demo --help"),
        (Stack("java", "none", False, backend_dir="."), "Run the project: ./mvnw verify"),
        (Stack("none", "none", False), "Check the project: ion repo check"),
    ],
)
def test_the_last_line_names_what_the_repo_has(stack: Stack, hint: str) -> None:
    # A repo adopted without a stack of ion-repo has no backend/ to run.
    assert install.launch_hint(stack, "demo") == hint


def test_kiln_s_catalogue_leaves_once_github_s_is_installed(machine: list[list[str]]) -> None:
    catalogue = {"source": {"source": "github", "repo": "antoine-tena/kiln"}}
    install.KNOWN_MARKETPLACES.write_text(json.dumps({"kiln": catalogue}))
    plugins = {"repo@kiln": True, "pile-nuxt@kiln": True, "stripe@kiln": False}
    install.CLAUDE_SETTINGS.write_text(json.dumps({"enabledPlugins": plugins}))

    install.install_machine()

    assert machine == [
        ["claude", "plugin", "marketplace", "add", "antoine-tena/ion-repo"],
        ["claude", "plugin", "install", "repo@ion-repo", "--scope", "user"],
        ["claude", "plugin", "install", "nuxt@ion-repo", "--scope", "user"],
        ["claude", "plugin", "marketplace", "remove", "kiln"],
    ]


def test_kiln_s_catalogue_leaves_even_when_ion_repo_s_is_already_there(
    machine: list[list[str]],
) -> None:
    both = {"kiln": {"source": {"source": "github"}}, "ion-repo": {"source": {"source": "github"}}}
    install.KNOWN_MARKETPLACES.write_text(json.dumps(both))
    install.CLAUDE_SETTINGS.write_text(json.dumps({"enabledPlugins": {"repo@ion-repo": True}}))

    install.install_machine()

    assert machine == [["claude", "plugin", "marketplace", "remove", "kiln"]]


def test_kiln_s_catalogue_becomes_ion_repo_s_from_the_same_folder(machine: list[list[str]]) -> None:
    folder = {"source": {"source": "directory", "path": "/home/me/code/kiln"}}
    install.KNOWN_MARKETPLACES.write_text(json.dumps({"kiln": folder}))
    install.CLAUDE_SETTINGS.write_text(json.dumps({"enabledPlugins": {"repo@kiln": True}}))

    install.install_machine()

    assert machine == [
        ["claude", "plugin", "marketplace", "remove", "kiln"],
        ["claude", "plugin", "marketplace", "add", "/home/me/code/kiln"],
        ["claude", "plugin", "install", "repo@ion-repo", "--scope", "user"],
    ]
