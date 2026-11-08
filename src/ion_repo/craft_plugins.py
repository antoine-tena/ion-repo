"""The crafts' plugins in a repo that keeps its own `.claude/settings.json` (`kept`, an adopted
repo): the template never renders that file there, so a project would miss the skills of its
crafts. `ion repo update` adds what `pieces` in `copier.yml` brings, and nothing else: a plugin the
repo lists is never removed, a repo's own keys are left as they are."""

import json
from collections.abc import Sequence
from pathlib import Path

from ion_score import ui

from ion_repo import migrations
from ion_repo.pieces import Piece, brought, table
from ion_repo.stack import kept_of

SETTINGS_FILE = ".claude/settings.json"


def add_craft_plugins(root: Path, source: str, frozen: Sequence[str]) -> list[str]:
    """The plugins added to the kept settings, none when ion-repo renders that file itself."""
    if SETTINGS_FILE not in kept_of(root) or SETTINGS_FILE in frozen:
        return []
    path = root / SETTINGS_FILE
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        ui.note(f"{SETTINGS_FILE} left as it is, it cannot be read: {error}")
        return []
    answers = migrations.raw_answers(root)
    wanted = [piece for piece in table(source) if brought(piece, answers)]
    added = _add(settings, wanted)
    if added:
        path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        ui.note(f"plugins of this project's crafts enabled: {', '.join(added)}")
    return added


def _add(settings: dict[str, object], wanted: Sequence[Piece]) -> list[str]:
    enabled = settings.get("enabledPlugins")
    catalogs = settings.get("extraKnownMarketplaces")
    enabled = enabled if isinstance(enabled, dict) else {}
    catalogs = catalogs if isinstance(catalogs, dict) else {}
    added = []
    for piece in wanted:
        plugin = f"{piece.plugin}@{piece.tool}"
        if plugin not in enabled:
            enabled[plugin] = True
            added.append(plugin)
        catalogs.setdefault(
            piece.tool, {"source": {"source": "github", "repo": piece.repo}, "autoUpdate": True}
        )
    if added:
        settings["enabledPlugins"] = enabled
        settings["extraKnownMarketplaces"] = catalogs
    return added
