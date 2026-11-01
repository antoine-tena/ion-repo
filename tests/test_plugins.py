import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
PLUGINS = [plugin["name"] for plugin in MARKETPLACE["plugins"]]
# Ce qui renvoie à un skill (`/repo:merge`) : la charte et les fichiers générés, les plugins
# eux-mêmes, les messages de la commande, la documentation, les consignes d'ion-repo.
CITING = (
    "template",
    "plugins",
    "src",
    "README.md",
    "README.fr.md",
    "CONTRIBUTING.md",
    "CLAUDE.md",
    ".claude/rules",
)
TEXT_SUFFIXES = {".md", ".py", ".jinja", ".json", ".yml", ".yaml", ".toml", ".sh", ".txt"}


def citing_files() -> list[Path]:
    files = []
    for name in CITING:
        path = ROOT / name
        if path.is_file():
            files.append(path)
        else:
            files += [f for f in path.rglob("*") if f.is_file() and f.suffix in TEXT_SUFFIXES]
    return files


def test_every_cited_skill_exists() -> None:
    cited = re.compile(rf"\b({'|'.join(map(re.escape, PLUGINS))}):([a-z][a-z0-9-]*)")
    missing = {
        f"{match[1]}:{match[2]} ({path.relative_to(ROOT)})"
        for path in citing_files()
        for match in cited.finditer(path.read_text(errors="ignore"))
        if not (ROOT / "plugins" / match[1] / "skills" / match[2] / "SKILL.md").is_file()
    }
    assert sorted(missing) == []


# Une règle de `.claude/rules/` ne se charge que quand Claude touche un fichier que ses `paths`
# désignent : un motif qui ne désigne plus rien (fichier renommé ou déplacé) l'éteint sans bruit.
def test_rule_paths_match_files() -> None:
    dead: dict[str, list[str]] = {}
    for rule in (ROOT / ".claude" / "rules").glob("*.md"):
        front_matter = rule.read_text().split("---")[1]
        for pattern in re.findall(r'^\s*- "([^"]+)"$', front_matter, re.M):
            if not any(ROOT.glob(pattern)):
                dead.setdefault(rule.name, []).append(pattern)
    assert dead == {}


# Une description de skill est relue à chaque message de chaque session (T-162) : courte,
# déclencheurs gardés. Les skills repris d'un autre auteur (`author:`) gardent la leur.
DESCRIPTION_MAX = 300


def test_skill_descriptions_stay_short() -> None:
    too_long = {}
    for skill in (ROOT / "plugins").glob("*/skills/*/SKILL.md"):
        front_matter = skill.read_text().split("---")[1]
        description = re.search(r"^description: (.*)$", front_matter, re.M)
        if description and "author:" not in front_matter and len(description[1]) > DESCRIPTION_MAX:
            too_long[str(skill.relative_to(ROOT))] = len(description[1])
    assert too_long == {}


def test_each_skill_is_named_after_its_folder() -> None:
    # Ligne à ligne et non en YAML : Claude Code accepte « Sans CI : elle… » sans guillemets.
    for skill in (ROOT / "plugins").glob("*/skills/*/SKILL.md"):
        front_matter = skill.read_text().split("---")[1]
        assert re.search(rf"^name: {re.escape(skill.parent.name)}$", front_matter, re.M), skill
        assert re.search(r"^description: \S", front_matter, re.M), skill


# Paths of the `base` plugin before kiln 0.4: sessions started before an update keep calling
# them in the main tree, and a missing hook blocks every tool call.
LEGACY_PATHS = (
    "plugins/base/hooks/garde-branche.py",
    "plugins/base/hooks/rtk.py",
    "plugins/base/hooks/protege-fichiers.py",
    "plugins/base/hooks/controle-fichier.py",
    "plugins/base/hooks/kiln-a-jour.py",
    "plugins/base/hooks/relances.py",
    "plugins/base/scripts/statusline.py",
    "plugins/base/scripts/preparer-worktree.sh",
)


def test_former_plugin_paths_still_exist() -> None:
    assert [path for path in LEGACY_PATHS if not (ROOT / path).is_file()] == []


def test_hooks_point_at_existing_files() -> None:
    for hooks in (ROOT / "plugins").glob("*/hooks/hooks.json"):
        for path in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"\\]+)", hooks.read_text()):
            assert (hooks.parent.parent / path).is_file(), (hooks, path)


# The hook of kiln 0.4.10 runs `claude plugin install kiln@kiln` once the catalogue has moved under
# it, and a rename would unplug the tester's plugin: the old name stays until T-373 removes it.
def test_kiln_at_kiln_stays_installable() -> None:
    entry = next(plugin for plugin in MARKETPLACE["plugins"] if plugin["name"] == "kiln")
    assert entry["source"] == "./plugins/repo"
    assert "kiln" not in MARKETPLACE["renames"]
