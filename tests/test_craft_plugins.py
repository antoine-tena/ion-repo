import json
from pathlib import Path

import pytest
import yaml

from ion_repo import craft_plugins, pieces

WEBSITE = {"name": "shop", "frontend": "nuxt", "owner": "antoine-tena", "deploy": "none"}
SETTINGS = ".claude/settings.json"


def _project(tmp_path: Path, answers: dict[str, object], *kept: str) -> Path:
    project = tmp_path / "shop"
    (project / ".claude").mkdir(parents=True)
    (project / SETTINGS).write_text(
        json.dumps({"env": {"A": "1"}, "enabledPlugins": {"host@ion-host": True}}, indent=2) + "\n",
        encoding="utf-8",
    )
    (project / ".copier-answers.yml").write_text(
        yaml.safe_dump({**answers, "kept": list(kept)}), encoding="utf-8"
    )
    return project


def _table_row(tool: str) -> pieces.Piece:
    (piece,) = [piece for piece in pieces.table("") if piece.tool == tool]
    return piece


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        ({"frontend": "nuxt", "owner": "someone"}, ["ion-design"]),
        ({"frontend": "astro", "owner": "antoine-tena"}, ["ion-design", "ion-words", "ion-media"]),
        ({"frontend": "streamlit", "owner": "antoine-tena"}, []),
        ({"frontend": "none", "owner": "antoine-tena"}, []),
    ],
)
def test_a_website_brings_its_crafts_and_private_ones_stay_in_the_studio(
    answers: dict[str, object], expected: list[str]
) -> None:
    found = [p.tool for p in pieces.table("") if pieces.brought(p, {"name": "shop", **answers})]

    assert [tool for tool in found if tool != "ion-host"] == expected


def test_a_tools_own_repo_never_takes_its_craft() -> None:
    answers = {"name": "ion-design", "frontend": "nuxt", "owner": "antoine-tena"}

    assert not pieces.brought(_table_row("ion-design"), answers)


def test_a_kept_settings_file_gets_the_crafts_and_loses_nothing(tmp_path: Path) -> None:
    project = _project(tmp_path, WEBSITE, SETTINGS)

    added = craft_plugins.add_craft_plugins(project, "", [])

    settings = json.loads((project / SETTINGS).read_text(encoding="utf-8"))
    assert added == ["design@ion-design", "words@ion-words", "media@ion-media"]
    assert settings["env"] == {"A": "1"}
    assert list(settings["enabledPlugins"]) == ["host@ion-host", *added]
    assert settings["extraKnownMarketplaces"]["ion-design"] == {
        "source": {"source": "github", "repo": "antoine-tena/ion-design"},
        "autoUpdate": True,
    }


def test_a_second_update_adds_nothing(tmp_path: Path) -> None:
    project = _project(tmp_path, WEBSITE, SETTINGS)
    craft_plugins.add_craft_plugins(project, "", [])
    before = (project / SETTINGS).read_text(encoding="utf-8")

    assert craft_plugins.add_craft_plugins(project, "", []) == []
    assert (project / SETTINGS).read_text(encoding="utf-8") == before


def test_settings_the_template_renders_are_left_to_it(tmp_path: Path) -> None:
    project = _project(tmp_path, WEBSITE)

    assert craft_plugins.add_craft_plugins(project, "", []) == []


def test_frozen_settings_are_left_alone(tmp_path: Path) -> None:
    project = _project(tmp_path, WEBSITE, SETTINGS)

    assert craft_plugins.add_craft_plugins(project, "", [SETTINGS]) == []


def test_unreadable_settings_are_left_alone(tmp_path: Path) -> None:
    project = _project(tmp_path, WEBSITE, SETTINGS)
    (project / SETTINGS).write_text("{", encoding="utf-8")

    assert craft_plugins.add_craft_plugins(project, "", []) == []
    assert (project / SETTINGS).read_text(encoding="utf-8") == "{"
