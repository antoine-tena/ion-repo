"""The public docs follow the code: a renamed command, plugin or workflow fails here."""

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ("README.md", "README.fr.md", "CONTRIBUTING.md")
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())


def docs() -> dict[str, str]:
    return {name: (ROOT / name).read_text(encoding="utf-8") for name in DOCS}


def test_the_home_screenshot_is_the_current_home_screen() -> None:
    spec = importlib.util.spec_from_file_location("home", ROOT / "scripts/home_screenshot.py")
    assert spec is not None and spec.loader is not None
    home = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(home)

    expected = home.svg(home.home_screen())

    assert home.SVG_PATH.read_text(encoding="utf-8") == expected, (
        "run: uv run python scripts/home_screenshot.py"
    )
    assert home.SVG_PATH.name in docs()["README.md"]


def test_installed_plugins_exist_and_former_names_are_gone() -> None:
    plugins = {plugin["name"] for plugin in MARKETPLACE["plugins"]}
    former = "|".join(map(re.escape, MARKETPLACE["renames"]))
    for name, text in docs().items():
        assert set(re.findall(r"plugin install ([\w-]+)@kiln", text)) <= plugins, name
        assert not re.findall(rf"`/?({former})(:[\w-]+)?`", text), name


def test_cited_workflows_exist() -> None:
    workflows = {path.name for path in (ROOT / ".github/workflows").glob("*.yml")}
    for name, text in docs().items():
        cited = set(re.findall(r"`([\w-]+\.yml)`", text)) - {"ci.yml", "copier.yml"}
        assert cited <= workflows, (name, sorted(cited - workflows))
