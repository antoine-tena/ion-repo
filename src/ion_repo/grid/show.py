"""`kiln grid`: the rules kiln holds as the best, listed or shown one by one."""

import difflib

from ion_repo import ui
from ion_repo.grid.model import THEMES, Rule, load_rules
from ion_repo.shell import KilnError

LEVEL_COLORS = {"adopt": ui.MOSS, "trial": ui.FIRE, "assess": ui.STONE, "hold": ui.EMBER}


# Shown by default: what kiln stands behind today. Drafts (assess) and dropped practices (hold)
# are asked for by level.
DEFAULT_LEVELS = frozenset({"adopt", "trial"})


def list_rules(*, theme: str | None, scope: str | None, level: str | None) -> None:
    matching = [
        rule
        for rule in load_rules()
        if (theme is None or rule.theme == theme)
        and (scope is None or scope in (rule.scope, rule.scope_name))
    ]
    rules = [
        rule
        for rule in matching
        if (rule.level == level if level is not None else rule.level in DEFAULT_LEVELS)
    ]
    hidden = len(matching) - len(rules) if level is None else 0
    if theme is not None and theme not in THEMES:
        raise KilnError(f"no theme {theme!r}: {', '.join(THEMES)}")
    if not rules:
        print(ui.paint("  no rule matches", ui.STONE))
        if hidden:
            print(ui.paint(f"  {hidden} assessed or held: kiln grid --level assess", ui.STONE))
        return
    width = max(len(rule.id) for rule in rules)
    current = ""
    for rule in rules:
        if rule.theme != current:
            current = rule.theme
            print(f"\n  {ui.paint(current.upper(), ui.FIRE, bold=True)}")
        level = ui.paint(f"{rule.level:<6}", LEVEL_COLORS[rule.level])
        print(f"    {rule.id:<{width}}  {level}  {rule.title}")
    scored = sum(rule.is_scored for rule in rules)
    print(ui.paint(f"\n  {len(rules)} rules, {scored} scored (adopt). kiln grid <ID>", ui.STONE))
    if hidden:
        print(ui.paint(f"  {hidden} more, assessed or held: kiln grid --level assess", ui.STONE))


def show_rule(rule_id: str) -> None:
    rule = find_rule(rule_id)
    print(f"\n  {ui.paint(rule.id, ui.FIRE, bold=True)}  {rule.title}")
    print(f"  {ui.paint(rule.why, ui.STONE_LIGHT)}\n")
    for label, value in describe(rule):
        print(f"  {ui.paint(f'{label:<10}', ui.STONE)} {value}")


def find_rule(rule_id: str) -> Rule:
    wanted = rule_id.upper()
    rules = load_rules()
    for rule in rules:
        if rule.id == wanted:
            return rule
    # Whole words first (`ACTIONS` → PINNED-ACTIONS, not TRANSACTIONS), then typos.
    words = set(wanted.split("-"))
    close = [rule.id for rule in rules if words & set(rule.id.split("-"))]
    close = close or difflib.get_close_matches(wanted, [rule.id for rule in rules], n=3)
    hint = f" (did you mean {', '.join(close)}?)" if close else ": kiln grid lists them"
    raise KilnError(f"no rule {rule_id}{hint}")


def describe(rule: Rule) -> list[tuple[str, str]]:
    """The rule in labelled lines: what it is, where it comes from, how it is held."""
    lines = [
        ("theme", rule.theme),
        ("scope", rule.scope_label),
        ("level", rule.level + ("" if rule.is_scored else ", not scored")),
        ("regime", rule.regime),
        ("profiles", ", ".join(rule.profiles)),
        ("detected", _detector_label(rule)),
        ("fixed", f"kiln fix ({rule.fixer})" if rule.fixer else "by judgment (Claude, roadmap)"),
    ]
    if rule.charter_rule:
        lines.append(("charter", f"[{rule.charter_rule}] in kiln's repos"))
    if rule.switch_when:
        lines.append(("switches", rule.switch_when))
    lines += [("setting", f"{key}: {value}") for key, value in rule.settings.items()]
    lines += [
        ("source", f"{source.url} ({source.kind}, checked {source.checked})")
        for source in rule.sources
    ]
    lines.append(("waive", f'kiln waive {rule.id} --reason "why this repo differs"'))
    return lines


def _detector_label(rule: Rule) -> str:
    kind = str(rule.detector.get("kind", ""))
    if kind == "python":
        return f"python check `{rule.detector.get('check')}`"
    if kind == "file":
        return ("absent: " if rule.detector.get("expect") == "absent" else "present: ") + str(
            rule.detector.get("paths")
        )
    return kind or "not yet"
