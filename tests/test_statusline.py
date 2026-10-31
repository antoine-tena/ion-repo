"""Status line : le choix du poste (`ion repo set statusline=…`) et le script du plugin
`ion-repo`."""

import importlib.util
import json
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from ion_repo.config import UserConfig, load_config, save_config
from ion_repo.machine import apply_machine, only_machine_keys
from ion_repo.shell import KilnError
from ion_repo.statusline import (
    REFRESH_SECONDS,
    apply_statusline_choice,
    ensure_statusline,
    is_kiln_statusline,
)
from ion_repo.trailers import apply_trailers_choice, ensure_trailers

SCRIPT = Path(__file__).parent.parent / "plugins" / "repo" / "scripts" / "statusline.py"
OWN = {"type": "command", "command": "~/bin/ma-ligne.sh"}
X = "\u00d7"  # signe de multiplication des compteurs


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("statusline_script", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Un poste avec le catalogue ion-repo déclaré là où Claude Code le range."""
    monkeypatch.setenv("HOME", str(tmp_path))
    kiln = tmp_path / "kiln"
    (kiln / "plugins" / "repo" / "scripts").mkdir(parents=True)
    (kiln / "plugins" / "repo" / "scripts" / "statusline.py").write_text("")
    plugins = tmp_path / ".claude" / "plugins"
    plugins.mkdir(parents=True)
    (plugins / "known_marketplaces.json").write_text(
        json.dumps({"kiln": {"installLocation": str(kiln)}})
    )
    return tmp_path


def settings(home: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((home / ".claude" / "settings.json").read_text())
    return loaded


def test_machine_keys_set_in_a_repo_go_to_the_machine() -> None:
    # `ion repo set statusline=custom` in a repo was refused: only repo keys were known there (#47).
    assert only_machine_keys(["statusline=custom"])
    assert only_machine_keys(["channel=beta", "statusline=band"])
    assert not only_machine_keys(["team=a"])  # a repo key as well: the repo's
    assert not only_machine_keys(["statusline=band", "name=x"])
    assert not only_machine_keys([])


def test_frozen_repos_are_kept_by_the_machine_and_can_be_cleared() -> None:
    config = apply_machine(UserConfig(), ["frozen_repos=kiln-rehearsal, courses/old"])
    save_config(config)

    assert load_config().frozen_repos == ("kiln-rehearsal", "courses/old")
    assert only_machine_keys(["frozen_repos=kiln-rehearsal"])
    assert apply_machine(config, ["frozen_repos="]).frozen_repos == ()


def test_statusline_choice_is_checked() -> None:
    assert apply_machine(UserConfig(), ["statusline=band"]).statusline == "band"
    with pytest.raises(KilnError, match="statusline"):
        apply_machine(UserConfig(), ["statusline=arc-en-ciel"])


def test_trailers_choice_is_checked() -> None:
    assert apply_machine(UserConfig(), ["ai_trailers=never"]).ai_trailers == "never"
    with pytest.raises(KilnError, match="ai_trailers"):
        apply_machine(UserConfig(), ["ai_trailers=sometimes"])


def test_never_empties_claudes_attribution_and_disclose_gives_it_back(home: Path) -> None:
    settings = home / ".claude" / "settings.json"
    settings.write_text(json.dumps({"model": "opus"}))

    apply_trailers_choice("never")
    assert json.loads(settings.read_text()) == {
        "model": "opus",
        "attribution": {"commit": "", "pr": ""},
    }
    apply_trailers_choice("disclose")
    assert json.loads(settings.read_text()) == {"model": "opus"}


def test_disclose_keeps_an_attribution_the_user_wrote(home: Path) -> None:
    settings = home / ".claude" / "settings.json"
    own = {"attribution": {"commit": "Assisted-by: Claude"}}
    settings.write_text(json.dumps(own))

    apply_trailers_choice("disclose")
    assert json.loads(settings.read_text()) == own


def test_choose_for_me_means_disclose(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    assert ensure_trailers(UserConfig()).ai_trailers == "disclose"
    assert 'ai_trailers = "disclose"' in (home / ".config/kiln/config.toml").read_text()
    assert ensure_trailers(UserConfig(ai_trailers="never")).ai_trailers == "never"


def test_styles_named_before_kiln_0_4_are_still_accepted() -> None:
    assert apply_machine(UserConfig(), ["statusline=classique-fond"]).statusline == "classic-band"
    assert apply_machine(UserConfig(), ["statusline=perso"]).statusline == "custom"


def test_a_kiln_style_installs_the_script_and_keeps_other_settings(home: Path) -> None:
    (home / ".claude" / "settings.json").write_text(json.dumps({"model": "opus"}))

    apply_statusline_choice("plain")

    assert settings(home)["model"] == "opus"
    assert is_kiln_statusline(settings(home)["statusLine"])


def test_custom_never_touches_the_users_own_statusline(home: Path) -> None:
    (home / ".claude" / "settings.json").write_text(json.dumps({"statusLine": OWN}))

    apply_statusline_choice("custom")

    assert settings(home)["statusLine"] == OWN


def test_none_removes_the_statusline(home: Path) -> None:
    apply_statusline_choice("classic")
    apply_statusline_choice("none")

    assert "statusLine" not in settings(home)


def test_switching_styles_keeps_the_kiln_command(home: Path) -> None:
    (home / ".claude" / "settings.json").write_text(
        json.dumps(
            {
                "statusLine": {
                    "command": 'python3 "$HOME/ion-repo/plugins/base/scripts/statusline.py"'
                }
            }
        )
    )

    apply_statusline_choice("band")

    assert "$HOME" in settings(home)["statusLine"]["command"]  # écrite à la main, gardée


def test_the_kiln_statusline_reruns_on_a_timer(home: Path) -> None:
    # Claude Code ne relance le script qu'à ses événements : sans minuteur, git et la CI
    # lus en arrière-plan attendent le message suivant.
    (home / ".claude" / "settings.json").write_text(
        json.dumps(
            {
                "statusLine": {
                    "command": 'python3 "$HOME/ion-repo/plugins/repo/scripts/statusline.py"'
                }
            }
        )
    )

    apply_statusline_choice("plain")

    assert settings(home)["statusLine"]["refreshInterval"] == REFRESH_SECONDS


def test_a_set_up_machine_gets_the_timer_at_install(home: Path) -> None:
    (home / ".claude" / "settings.json").write_text(
        json.dumps(
            {
                "statusLine": {
                    "command": 'python3 "$HOME/ion-repo/plugins/base/scripts/statusline.py"'
                }
            }
        )
    )

    ensure_statusline(UserConfig(statusline="plain"))

    assert settings(home)["statusLine"]["refreshInterval"] == REFRESH_SECONDS


def test_no_claude_code_leaves_the_status_line_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))

    assert ensure_statusline(UserConfig()) == UserConfig()
    assert not (tmp_path / ".claude").exists()


def test_overview_finds_the_repos_two_folders_down(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    script = load_script()
    for repo in (
        "annski",
        "family/ion-repo/ion-repo",
        "family/seal/seal",
        "_archive/old",
        "a/b/c/deep",
    ):
        (tmp_path / repo / ".git").mkdir(parents=True)
    monkeypatch.setattr(
        script, "git_state", lambda path: Path(path).relative_to(tmp_path).as_posix()
    )

    script.scan(str(tmp_path))

    assert json.loads(capsys.readouterr().out) == [
        "annski",
        "family/ion-repo/ion-repo",
        "family/seal/seal",
    ]


def test_secret_scan_ignores_rendered_examples(tmp_path: Path) -> None:
    script = load_script()
    for name in ("template/.env.example.jinja", ".env.sample", "backend/.env", ".stripe/token"):
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text("")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-f", "."], cwd=tmp_path, check=True)

    assert sorted(script.tracked_secrets(str(tmp_path))) == [".stripe/token", "backend/.env"]


def test_integration_branch_is_not_counted_as_unmerged(tmp_path: Path) -> None:
    script = load_script()
    remote, clone = tmp_path / "remote", tmp_path / "clone"
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-q", "-b", "develop", str(remote)], check=True)
    subprocess.run(
        [*git, "-C", str(remote), "commit", "-q", "--allow-empty", "-m", "a"], check=True
    )
    subprocess.run(["git", "clone", "-q", str(remote), str(clone)], check=True)
    subprocess.run([*git, "-C", str(clone), "commit", "-q", "--allow-empty", "-m", "b"], check=True)
    subprocess.run(["git", "-C", str(clone), "branch", "feat/x"], check=True)

    assert script.unmerged_branches(str(clone), "develop") == 1  # feat/x, pas develop


def sample(script: ModuleType) -> object:
    item, status = script.Item, script.Status()
    status.repo = [[item("demo", role="title"), item("⎇ develop")], [item("~2", 1)]]
    status.session = [[item("Opus", role="strong")], [item("ctx", 0, gauge=34.0, amount="136k")]]
    status.tasks = [[item("65 tasks"), item(f"urgent{X}10", 3), item(f"blocked{X}14", short="")]]
    status.env = [
        [item(f"uv{X}8")],
        [item("prod"), item("django ↓153", 2, "↓153")],
        [item(":3000 :8000")],
    ]
    return status


def session_items(script: ModuleType, payload: dict[str, Any]) -> dict[str, tuple[int, str, Any]]:
    """Session et usage de la status line, par texte : (niveau, quantité, jauge)."""
    status = script.Status()
    script.collect_session(status, payload, "")
    return {i.text: (i.level, i.amount, i.gauge) for g in status.session + status.usage for i in g}


def context(tokens: int) -> dict[str, Any]:
    usage = {
        "input_tokens": 10,
        "cache_creation_input_tokens": 990,
        "cache_read_input_tokens": tokens,
    }
    return {"context_window_size": 1_000_000, "used_percentage": 25, "current_usage": usage}


AT_400K, AT_900K = {"autoCompactWindow": "400k"}, {"autoCompactWindow": 900000}


@pytest.mark.parametrize(
    ("settings", "gauge"),
    [
        ({"settings.json": {"autoCompactWindow": 400000}}, 62.5),
        ({"settings.json": AT_900K, "settings.local.json": AT_400K}, 62.5),  # le local l'emporte
        ({"settings.json": {**AT_900K, "modelSettings": {"opus": AT_400K}}}, 62.5),  # /autocompact
        ({}, 25.0),
    ],
)
def test_context_in_tokens_its_gauge_full_at_the_compaction(
    settings: dict[str, Any], gauge: float, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("CLAUDE_CODE_AUTO_COMPACT_WINDOW", raising=False)
    (tmp_path / "repo" / ".claude").mkdir(parents=True)
    for name, content in settings.items():
        (tmp_path / "repo" / ".claude" / name).write_text(json.dumps(content), encoding="utf-8")
    payload = {
        "context_window": context(249_000),
        "workspace": {"project_dir": str(tmp_path / "repo")},
        "model": {"id": "opus"},
    }

    items = session_items(load_script(), payload)

    assert items["ctx"] == (2, "250k", gauge)  # 250k : chaque message coûte cher


def test_the_context_turns_red_once_the_cache_is_cold() -> None:
    script = load_script()

    def level(warm: bool) -> int:
        cache = {"hit_ratio": 0.9, "warm": warm}
        items = session_items(script, {"context_window": context(59_000), "prompt_cache": cache})
        return int(items["ctx"][0])

    assert (level(True), level(False)) == (0, 3)  # cache expiré : tout réécrit au message suivant


@pytest.mark.parametrize("style", ["plain", "band", "classic", "classic-band"])
@pytest.mark.parametrize("columns", [60, 90, 140])
def test_no_line_overflows(style: str, columns: int) -> None:
    script = load_script()

    lines = script.render(sample(script), style, columns)

    assert all(script.visible_width(line) <= columns for line in lines)


def test_signals_put_tasks_first_and_drop_grey_before_compacting_colour() -> None:
    script = load_script()

    signals = script.render(sample(script), "plain", 40)[2]
    plain = script.re.sub(r"\033\[[0-9;]*m", "", signals)

    assert plain.startswith(f"65 tasks urgent{X}10")  # le total reste devant ses sous-comptes
    assert "django ↓153" in plain or "↓153" in plain
    assert f"uv{X}8" not in plain  # le gris tombe en premier


BACKLOG = """# Backlog

## 🔴 Critical

### T-01 · Ship it
- **Type**: task
- **Status**: in progress — branch feat/ship, since 2026-10-16

## 🟡 Normal

### T-02 · Try an idea
- **Type**: idea
- **Status**: blocked — waiting for antoine

## ✅ Done

- **2026-10-15** · T-00 · Done already
"""

LEGACY = """# À faire

## 🔴 Critique

### AF-01 · Livrer
- **État** : à vérifier — en prod

## ✅ Fait

### AF-00 · Déjà fait
"""


def labels(group: list[Any]) -> list[str]:
    return [item.text for item in group]


def test_backlog_counts_open_tickets_and_their_status(tmp_path: Path) -> None:
    (tmp_path / "docs/backlog").mkdir(parents=True)
    (tmp_path / "docs/backlog/backlog.md").write_text(BACKLOG)
    (tmp_path / "docs/backlog/urgent.md").write_text("# Urgent\n\n- [ ] Pay — antoine\n")

    items = load_script().backlog_items(str(tmp_path))

    assert labels(items) == ["2 tasks", f"urgent{X}1", f"crit{X}1", f"doing{X}1", f"blocked{X}1"]


def test_backlog_still_reads_the_old_french_tracker(tmp_path: Path) -> None:
    (tmp_path / "docs/a-faire").mkdir(parents=True)
    (tmp_path / "docs/a-faire/a-faire.md").write_text(LEGACY)

    items = load_script().backlog_items(str(tmp_path))

    assert labels(items) == ["1 tasks", f"crit{X}1", f"review{X}1"]
