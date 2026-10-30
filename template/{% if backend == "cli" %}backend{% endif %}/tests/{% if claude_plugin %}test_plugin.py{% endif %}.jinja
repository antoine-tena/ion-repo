"""The Claude Code plugin at the root of the repo: what Claude Code would refuse to load."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
SKILLS = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def test_each_cataloged_plugin_has_its_manifest() -> None:
    for plugin in MARKETPLACE["plugins"]:
        manifest = ROOT / plugin["source"] / ".claude-plugin/plugin.json"
        assert json.loads(manifest.read_text())["name"] == plugin["name"]


def test_each_skill_is_named_like_its_folder() -> None:
    assert SKILLS
    for skill in SKILLS:
        front_matter = FRONT_MATTER.match(skill.read_text())
        assert front_matter, f"{skill}: no front matter"
        fields = dict(line.split(": ", 1) for line in front_matter[1].splitlines() if ": " in line)
        assert fields.get("name") == skill.parent.name
        assert fields.get("description")
