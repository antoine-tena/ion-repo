"""Status line : le choix du poste (`ion repo set statusline=…`) et le script du plugin
`ion-repo`."""

import importlib.util
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from ion_repo.config import (
    STATUSLINE_PALETTES,
    UserConfig,
    config_path,
    load_config,
    save_config,
)
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


def test_the_settings_of_before_ion_repo_0_4_14_move_to_their_new_place() -> None:
    legacy = config_path().parent.parent / "kiln" / "config.toml"
    legacy.parent.mkdir(parents=True)
    legacy.write_text('statusline = "band"\n')

    assert load_config().statusline == "band"
    assert config_path().read_text() == 'statusline = "band"\n'
    assert not legacy.parent.exists()


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
    assert 'ai_trailers = "disclose"' in (home / ".config/ion-repo/config.toml").read_text()
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


def test_the_script_runs_on_ion_repos_python_not_the_paths(home: Path) -> None:
    # Sur macOS, `python3` est en 3.9 ou 3.13 : le script, en 3.14, s'y arrête sur une erreur de
    # syntaxe et la ligne d'état reste vide.
    apply_statusline_choice("plain")

    assert settings(home)["statusLine"]["command"].startswith(f'"{sys.executable}" ')


def test_a_bare_python3_is_replaced_at_install(home: Path) -> None:
    (home / ".claude" / "settings.json").write_text(
        json.dumps(
            {
                "statusLine": {
                    "command": 'python3 "$HOME/ion-repo/plugins/repo/scripts/statusline.py"',
                    "refreshInterval": REFRESH_SECONDS,
                }
            }
        )
    )

    ensure_statusline(UserConfig(statusline="plain"))

    assert settings(home)["statusLine"]["command"] == (
        f'"{sys.executable}" "$HOME/ion-repo/plugins/repo/scripts/statusline.py"'
    )


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


def test_tickets_are_counted_in_both_forms(tmp_path: Path) -> None:
    """A repo not yet through `ion repo tickets` keeps its count, one that is too."""
    backlog = tmp_path / "docs/backlog/backlog.md"
    backlog.parent.mkdir(parents=True)
    backlog.write_text(
        "## 🔴 Critical\n\n### acme-shop#T-01 · New form\n- **Status**: todo\n\n"
        "## 🟡 Normal\n\n### T-02 · Old form\n- **Status**: todo\n"
    )

    items = load_script().backlog_items(str(tmp_path))

    assert labels(items) == ["2 tasks", f"crit{X}1"]


def test_statusline_palette_is_a_machine_key() -> None:
    assert only_machine_keys(["statusline_palette=nord"])
    assert apply_machine(UserConfig(), ["statusline_palette=nord"]).statusline_palette == "nord"
    with pytest.raises(KilnError, match="statusline_palette"):
        apply_machine(UserConfig(), ["statusline_palette=arc-en-ciel"])


def test_the_chat_palette_takes_the_chat_colors_of_a_custom_theme(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`/repo:color` writes the person's color in a custom theme: the status line follows."""
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".claude/themes").mkdir(parents=True)
    (tmp_path / ".claude/settings.json").write_text('{"theme": "custom:mine"}')
    (tmp_path / ".claude/themes/mine.json").write_text(
        '{"name": "Mine", "base": "light", "overrides": {"professionalBlue": "#4ade80"}}'
    )
    script = load_script()

    assert script.claude_theme() == "light"
    overrides = script.custom_theme(script.theme_setting())["overrides"]
    light = script.chat_palette("light", overrides)["light"]
    assert light[3] == light[4] == (74, 222, 128)
    assert light[5] == (215, 119, 87)


def test_the_chat_palette_keeps_claude_codes_colors_without_a_custom_theme() -> None:
    script = load_script()

    dark = script.chat_palette("dark", {})["dark"]
    assert dark[3] == (106, 155, 204)
    assert script.chat_palette("dark-daltonized", {"claude": "ansi:red"})["dark"][5] == (
        255,
        153,
        51,
    )


NEW_PALETTES = {
    "one-dark": ("#abb2bf", "#e5c07b", "#d19a66", "#e06c75"),
    "monokai": ("#a6a28c", "#e6db74", "#fd971f", "#f92672"),
    "everforest": ("#9da9a0", "#dbbc7f", "#e69875", "#e67e80"),
    "kanagawa": ("#a6a69c", "#e6c384", "#ffa066", "#e82424"),
    "rose-pine": ("#908caa", "#f6c177", "#ea9a97", "#eb6f92"),
    "github-dark": ("#8b949e", "#d29922", "#db6d28", "#f85149"),
    "ayu": ("#acb6bf", "#e6b450", "#ff8f40", "#f07178"),
    "material": ("#b0bec5", "#ffcb6b", "#f78c6c", "#ff5370"),
    "slate": ("#94a3b8", "#fbbf24", "#fb923c", "#f87171"),
    "zenburn": ("#9fafaf", "#f0dfaf", "#dfaf8f", "#cc9393"),
}


@pytest.mark.parametrize("name", NEW_PALETTES)
def test_the_terminal_world_palettes_are_set_with_their_levels(name: str) -> None:
    """Les palettes connues du terminal se choisissent et gardent leurs niveaux, en sombre."""
    assert apply_machine(UserConfig(), [f"statusline_palette={name}"]).statusline_palette == name
    script = load_script()
    _, stone, _, _, glow, fire, ember, _, _ = script.PALETTES[name]["dark"]
    hexes = tuple("#{:02x}{:02x}{:02x}".format(*color) for color in (stone, glow, fire, ember))
    assert hexes == NEW_PALETTES[name]
    assert len(script.PALETTES[name]["light"]) == len(script.PALETTES[name]["dark"])


ONE_HUE = ["red", "orange", "yellow", "green", "teal", "blue", "violet", "pink"]


def oklch_of(color: tuple[int, int, int]) -> tuple[float, float, float]:
    """sRGB to OKLCH (Björn Ottosson's OKLab), to measure what the eye sees."""
    linear = [
        part / 12.92 if part <= 0.04045 else ((part + 0.055) / 1.055) ** 2.4
        for part in (channel / 255 for channel in color)
    ]
    red, green, blue = linear
    long_ = (0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue) ** (1 / 3)
    medium = (0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue) ** (1 / 3)
    short = (0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue) ** (1 / 3)
    lightness = 0.2104542553 * long_ + 0.7936177850 * medium - 0.0040720468 * short
    a = 1.9779984951 * long_ - 2.4285922050 * medium + 0.4505937099 * short
    b = 0.0259040371 * long_ + 0.7827717662 * medium - 0.8086757660 * short
    return lightness, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


@pytest.mark.parametrize("shade", ["dark", "light"])
@pytest.mark.parametrize("name", ONE_HUE)
def test_a_one_hue_palette_tells_its_levels_apart_by_lightness(name: str, shade: str) -> None:
    """Une palette d'une seule teinte : un gris, puis la teinte de la moins à la plus frappante
    (sur fond sombre de la plus terne à la plus claire, sur fond clair de la plus pâle à la plus
    profonde), chaque niveau assez loin du suivant pour se lire d'un coup d'œil."""
    assert apply_machine(UserConfig(), [f"statusline_palette={name}"]).statusline_palette == name
    script = load_script()
    _, stone, _, _, glow, fire, ember, _, _ = script.PALETTES[name][shade]
    hue = script.HUES[name]
    assert oklch_of(stone)[1] < 0.03
    levels = [oklch_of(color) for color in (glow, fire, ember)]
    toward_urgent = 1 if shade == "dark" else -1  # brighter on a dark terminal, deeper on a light
    for (calmer, _, _), (sharper, _, _) in itertools.pairwise(levels):
        assert (sharper - calmer) * toward_urgent >= 0.1
    for _, chroma, angle in levels:
        assert chroma > 0.04
        assert min(abs(angle - hue), 360 - abs(angle - hue)) < 12


def test_the_old_rose_palette_is_read_as_pink() -> None:
    assert apply_machine(UserConfig(), ["statusline_palette=rose"]).statusline_palette == "pink"
    assert load_script().chosen_palette({"statusline_palette": "rose"}) == "pink"


def run_script(*arguments: str, home: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        capture_output=True,
        text=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin", "XDG_CONFIG_HOME": str(home / "config")},
        cwd=home,
        stdin=subprocess.DEVNULL,
    )


@pytest.mark.parametrize("style", ["plain", "band", "classic", "classic-band"])
def test_a_preview_draws_a_whole_session_in_the_box_of_a_choice(tmp_path: Path, style: str) -> None:
    """L'aperçu d'un choix : une session d'exemple (pas `?`), sans couleurs, sans lire stdin, et
    jamais plus large que la boîte."""
    done = run_script("--preview", "--style", style, "--width", "40", home=tmp_path)

    assert done.returncode == 0, done.stderr
    assert "\033" not in done.stdout
    assert "Opus 5.5" in done.stdout
    assert all(len(line) <= 40 for line in done.stdout.splitlines())


def test_an_unknown_option_value_is_refused_rather_than_replaced(tmp_path: Path) -> None:
    """`--palette nope` montrait `stone-fire` sans rien dire : l'aperçu mentait."""
    done = run_script("--preview", "--palette", "nope", home=tmp_path)

    assert done.returncode == 2
    assert "invalid choice: 'nope'" in done.stderr
    assert "--preview" in run_script("--help", home=tmp_path).stdout


def test_a_line_too_wide_is_cut_with_an_ellipsis_its_colors_kept() -> None:
    script = load_script()
    line = "\033[1mion-repo\033[22m develop\033[0m"

    clipped = script.clip(line, 10)

    assert script.visible_width(clipped) == 10
    assert clipped == "\033[1mion-repo\033[22m …\033[0m"
    assert script.clip(line, 40) == line


def test_statusline_palette_accepts_chat() -> None:
    assert apply_machine(UserConfig(), ["statusline_palette=chat"]).statusline_palette == "chat"


def test_levels_give_each_palette_its_four_colors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Une palette se choisit à ses couleurs : son nom ne dit rien de ce qu'on verra."""
    monkeypatch.setenv("HOME", str(tmp_path))
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--levels", "--theme", "dark"],
        capture_output=True,
        text=True,
        check=True,
    )
    levels = json.loads(done.stdout)

    assert set(levels) == set(STATUSLINE_PALETTES)
    assert levels["stone-fire"] == {
        "all well": "#8c8c87",
        "to watch": "#ffe178",
        "to handle": "#f79628",
        "urgent": "#cd3223",
    }
