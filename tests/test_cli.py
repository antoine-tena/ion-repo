import argparse
import re
import sys
from pathlib import Path

import pytest

from ion_repo import cli, fleet, ui
from ion_repo.shell import KilnError


def run_kiln(monkeypatch: pytest.MonkeyPatch, *arguments: str) -> int:
    """`ion-repo …` dans ce processus ; renvoie le code de sortie (0 sans sys.exit)."""
    monkeypatch.setattr(sys, "argv", ["kiln", *arguments])
    try:
        cli.main()
    except SystemExit as exit_request:
        return int(exit_request.code or 0)
    return 0


@pytest.mark.parametrize("arguments", [(), ("-h",), ("--help",)])
def test_home_screen_lists_every_command_by_section(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], arguments: tuple[str, ...]
) -> None:
    assert run_kiln(monkeypatch, *arguments) == 0

    out = capsys.readouterr().out
    for title, names in cli.COMMAND_GROUPS:
        assert title.upper() in out
        assert all(name in out for name in names)
    assert "EXAMPLES" in out


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_a_command_help_is_drawn_like_the_home_screen(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], flag: str
) -> None:
    assert run_kiln(monkeypatch, "dev", flag) == 0

    out = capsys.readouterr().out
    assert "Run the project locally" in out
    assert "Usage  ion repo dev [options] [{status,logs,stop}] [service]" in out
    assert "ARGUMENTS" in out
    assert "OPTIONS" in out
    assert "Logs: keep following" in out
    assert "usage:" not in out
    assert "show this help message" not in out


def test_every_command_of_the_home_screen_exists() -> None:
    parser = cli.build_parser()
    known = {
        choice
        for action in parser._actions
        if hasattr(action, "choices") and isinstance(action.choices, dict)
        for choice in action.choices
    }
    listed = {name.split()[0] for _, names in cli.COMMAND_GROUPS for name in names}

    assert listed == known


def test_outside_a_repository_the_error_is_explained(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)

    assert run_kiln(monkeypatch, "check") == cli.EXIT_FAILURE
    assert "is not in a repo" in capsys.readouterr().err


def test_a_failed_command_ends_on_an_interrupted_recap(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def failing_dispatch(arguments: object) -> None:
        ui.step("backend : dépendances Python")
        raise KilnError("échec de `uv sync`")

    ui._steps.clear()
    monkeypatch.setattr(cli, "dispatch", failing_dispatch)

    assert run_kiln(monkeypatch, "check") == cli.EXIT_FAILURE
    captured = capsys.readouterr()
    assert "Interrupted after" in captured.out
    assert "ion-repo: échec de `uv sync`" in captured.err
    ui._steps.clear()


def test_status_outside_a_terminal_is_plain_text(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    (tmp_path / "config/kiln").mkdir(parents=True)
    (tmp_path / "config/kiln/config.toml").write_text(f'code_dir = "{tmp_path}"\n')
    monkeypatch.setattr(fleet, "latest_release", lambda **_: "v0.3.0")

    assert run_kiln(monkeypatch, "status") == 0
    out = capsys.readouterr().out
    assert "\033[" not in out
    assert out.splitlines()[0].startswith("ion-repo v")
    assert "REPO" in out


def test_bash_completion_script_lists_commands_and_options(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run_kiln(monkeypatch, "completion", "bash") == 0
    out = capsys.readouterr().out
    parser = cli.build_parser()
    subparsers = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    for name in subparsers.choices:
        assert name in out
    # a few known options
    assert "--size" in out
    assert "--all" in out
    assert "--containers" in out
    assert "complete -F _kiln_completion ion-repo" in out


@pytest.mark.parametrize(
    ("legacy", "modern"),
    [
        (["contrat"], ["contract"]),
        (["set", "--poste", "team=a"], ["set", "--global", "team=a"]),
        (["ci", "--sauter=infra", "--statut"], ["ci", "--skip=infra", "--status"]),
        (["ci", "--garder", "--sans-pousser"], ["ci", "--keep", "--no-push"]),
    ],
)
def test_the_names_of_kiln_0_3_still_work_with_a_warning(
    capsys: pytest.CaptureFixture[str], legacy: list[str], modern: list[str]
) -> None:
    assert cli.modernize(legacy) == modern
    assert "is now" in capsys.readouterr().err


def test_a_size_named_after_the_fire_still_works_with_a_warning(
    capsys: pytest.CaptureFixture[str],
) -> None:
    arguments = cli.build_parser().parse_args(["adopt", "--size", "ember"])

    assert arguments.size == "small"
    assert "`ember` is now `small`" in capsys.readouterr().err


def test_an_option_of_another_command_is_left_alone() -> None:
    assert cli.modernize(["update", "--statut"]) == ["update", "--statut"]


def test_a_long_release_note_wraps_instead_of_being_cut(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(ui, "is_styled", lambda stream=None: True)
    monkeypatch.setattr(ui, "_columns", lambda: 50)
    words = "every word of this long line must reach the reader in full, wrapped"

    ui.panel("What's new", [f"- {words}", "v0.4.1  2026-10-19"])

    text = re.sub(r"\033\[[\d;]*m", "", capsys.readouterr().out)
    assert "…" not in text
    assert " ".join(re.findall(r"│ ·? ?(.*?)\s*│", text)).split() == [
        "What's", "new", *words.split(), "v0.4.1", "2026-10-19"
    ]  # fmt: skip
    assert all(len(line) <= 50 for line in text.splitlines())


def test_code_spans_of_a_release_note_show_in_colour_without_backticks(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(ui, "is_styled", lambda stream=None: True)
    monkeypatch.setattr(ui, "_columns", lambda: 100)

    ui.panel("What's new", ["- new answer (`ci_runner`), set by `ion repo set ci_runner=github`."])

    out = capsys.readouterr().out
    text = re.sub(r"\033\[[\d;]*m", "", out)
    assert "`" not in text
    assert "new answer (ci_runner), set by ion repo set ci_runner=github." in text
    assert ui.paint("ci_runner", ui.GLOW) in out and ui.paint("set", ui.GLOW) in out
