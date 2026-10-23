"""`kiln install` outside a repo: kiln for the whole machine, only what is missing."""

import json
from pathlib import Path

import pytest

from kiln import cli, install
from kiln.config import UserConfig


@pytest.fixture
def machine(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[list[str]]:
    """A machine with uv and claude, kiln's settings recorded; the commands run are listed."""
    commands: list[list[str]] = []
    monkeypatch.setattr(install, "CLAUDE_SETTINGS", tmp_path / "settings.json")
    monkeypatch.setattr(install, "KNOWN_MARKETPLACES", tmp_path / "known_marketplaces.json")
    monkeypatch.setattr(install, "load_config", lambda: UserConfig(system="linux"))
    monkeypatch.setattr(install, "ensure_statusline", lambda config: config)
    monkeypatch.setattr(install, "run", lambda command, cwd: commands.append(command))
    monkeypatch.setattr("kiln.install.shutil.which", lambda name: f"/usr/bin/{name}")
    return commands


def test_a_bare_machine_gets_the_command_the_catalogue_and_the_plugin(
    machine: list[list[str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "kiln.install.shutil.which", lambda name: None if name == "kiln" else f"/usr/bin/{name}"
    )

    install.install_machine()

    assert machine == [
        ["uv", "tool", "install", "kiln-cli"],
        ["claude", "plugin", "marketplace", "add", "antoine-tena/kiln"],
        ["claude", "plugin", "install", "kiln@kiln", "--scope", "user"],
    ]


def test_run_again_it_does_nothing(machine: list[list[str]]) -> None:
    install.KNOWN_MARKETPLACES.write_text(json.dumps({"kiln": {}}))
    install.CLAUDE_SETTINGS.write_text(json.dumps({"enabledPlugins": {"kiln@kiln": True}}))

    install.install_machine()

    assert machine == []


def test_without_claude_code_the_plugins_wait(
    machine: list[list[str]], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "kiln.install.shutil.which", lambda name: None if name == "claude" else f"/usr/bin/{name}"
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
