"""The grid: what kiln holds as the best way to work today, one small TOML file per rule.

Everything else reads it: `kiln grid` shows it, `kiln score` measures a repo against it, `kiln
fix` closes what a script can close, and Claude gets the rest. A rule lives in
`rules/<theme>/<RULE-ID>.toml` and sits on two axes, its theme (what it speaks of) and its scope
(whom it applies to), with a level (the Technology Radar's adopt, trial, assess, hold) and a
regime (strict, ratchet, review). Authority comes from sources, weighed in the doctrine's order:
official docs, security advisories, measured studies, adoption data, blogs.
"""

import datetime
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

RULES_DIR = Path(__file__).parent / "rules"

PILLARS = ("methods", "standards", "readability", "slimming", "versions")
# The vision's closed list of themes (17 October 2026).
THEMES = (
    "structure",
    "code-standards",
    "api-typing",
    "architecture",
    "data-migrations",
    "background-tasks",
    "concurrency",
    "cache",
    "errors-logs",
    "app-security",
    "personal-data",
    "supply-chain",
    "tests",
    "performance",
    "front-accessibility",
    "containers",
    "operations",
    "observability",
    "ci-cd",
    "git-versions",
    "docs-tracking",
    "ai-assisted",
    "business-domain",
)
SCOPES = ("universal", "language", "framework", "tool", "domain")
# Thoughtworks' Technology Radar: only `adopt` counts in the score; `trial` is shown,
# `assess` and `hold` are kept for the record and for the rules to come.
LEVELS = ("adopt", "trial", "assess", "hold")
SCORED_LEVELS = frozenset({"adopt"})
REGIMES = ("strict", "ratchet", "review")
PROFILES = ("solo", "association", "company", "university", "enterprise")
# Who can find a gap, and who can close it (doctrine 5: the script first, Claude next).
DETECTION = ("script", "approximate", "judgment")
FIXING = ("script", "judgment")
# Weighed in this order, the most reliable first (doctrine, principle 3).
SOURCE_KINDS = ("docs", "advisory", "study", "adoption", "blog")
# An `adopt` rule whose sources were all checked longer ago is stale: the grid keeps up.
SOURCE_MAX_AGE = datetime.timedelta(days=183)


class GridError(ValueError):
    """A rule file that does not hold."""


@dataclass(frozen=True)
class Source:
    url: str
    kind: str
    checked: datetime.date


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    pillar: str
    theme: str
    scope: str
    scope_name: str  # the language, framework, tool or domain; "" when universal
    level: str
    regime: str
    profiles: tuple[str, ...]
    why: str
    sources: tuple[Source, ...]
    applies: tuple[str, ...]  # facts the repo must have (`ion_repo.grid.facts`); empty: always
    detector: Mapping[str, object]
    fixer: str  # name of a converter of `kiln fix`; "" when only judgment fixes it
    since: str
    switch_when: str = ""
    charter_rule: str = ""  # the charter rule that enforces it in kiln's repos
    detectable: str = "script"  # script, approximate (the script flags, Claude confirms), judgment
    fixable: str = "judgment"  # script (a converter can), judgment
    settings: Mapping[str, str] = field(default_factory=dict)
    # An unscored rule whose gap `kiln score` still shows, as advice, to the repos it applies to.
    advice: bool = False
    path: Path = Path()

    @property
    def is_scored(self) -> bool:
        return self.level in SCORED_LEVELS

    @property
    def scope_label(self) -> str:
        return f"{self.scope}: {self.scope_name}" if self.scope_name else self.scope


def load_rules(directory: Path = RULES_DIR) -> list[Rule]:
    """Every rule of the grid, sorted by theme then ID; a `GridError` names a broken file."""
    rules = [load_rule(path) for path in sorted(directory.glob("*/*.toml"))]
    return sorted(rules, key=lambda rule: (THEMES.index(rule.theme), rule.id))


def load_rule(path: Path) -> Rule:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise GridError(f"{path}: {error}") from error
    try:
        scope = data["scope"]
        return Rule(
            id=str(data["id"]),
            title=str(data["title"]),
            pillar=str(data["pillar"]),
            theme=str(data["theme"]),
            scope=str(scope["kind"]),
            scope_name=str(scope.get("name", "")),
            level=str(data["level"]),
            regime=str(data["regime"]),
            profiles=tuple(map(str, data["profiles"])),
            why=str(data["why"]),
            sources=tuple(_source(source) for source in data.get("sources", [])),
            applies=tuple(map(str, data.get("applies", []))),
            detector=dict(data.get("detector", {})),
            fixer=str(data.get("fixer", "")),
            since=str(data["since"]),
            switch_when=str(data.get("switch_when", "")),
            charter_rule=str(data.get("charter_rule", "")),
            detectable=str(data.get("detectable", "script")),
            fixable=str(data.get("fixable", "script" if data.get("fixer") else "judgment")),
            settings={str(key): str(value) for key, value in data.get("settings", {}).items()},
            advice=bool(data.get("advice", False)),
            path=path,
        )
    except (KeyError, TypeError) as error:
        raise GridError(f"{path}: missing or malformed field {error}") from error


def _source(data: Mapping[str, object]) -> Source:
    checked = data["checked"]
    if not isinstance(checked, datetime.date):
        raise GridError(f"source {data.get('url')}: `checked` must be a date (2026-10-19)")
    return Source(str(data["url"]), str(data["kind"]), checked)


def problems(rules: list[Rule], today: datetime.date | None = None) -> list[str]:
    """What breaks the grid's own rules: unique IDs, closed lists, files named after their
    rule and theme, fresh sources for every scored rule."""
    today = today or datetime.date.today()
    found: list[str] = []
    seen: dict[str, Path] = {}
    for rule in rules:
        where = f"{rule.id} ({rule.path.name})"
        if rule.id in seen:
            found.append(f"{where}: ID already used by {seen[rule.id]}")
        seen[rule.id] = rule.path
        if rule.path.stem != rule.id or rule.path.parent.name != rule.theme:
            found.append(f"{where}: the file must be rules/{rule.theme}/{rule.id}.toml")
        for name, value, allowed in (
            ("pillar", rule.pillar, PILLARS),
            ("theme", rule.theme, THEMES),
            ("scope", rule.scope, SCOPES),
            ("level", rule.level, LEVELS),
            ("regime", rule.regime, REGIMES),
            ("detectable", rule.detectable, DETECTION),
            ("fixable", rule.fixable, FIXING),
        ):
            if value not in allowed:
                found.append(f"{where}: {name} {value!r} is not one of {', '.join(allowed)}")
        found += [
            f"{where}: profile {profile!r} is not one of {', '.join(PROFILES)}"
            for profile in rule.profiles
            if profile not in PROFILES
        ]
        if (rule.scope == "universal") == bool(rule.scope_name):
            found.append(f"{where}: a universal scope has no name, the others have one")
        found += [
            f"{where}: source kind {source.kind!r} is not one of {', '.join(SOURCE_KINDS)}"
            for source in rule.sources
            if source.kind not in SOURCE_KINDS
        ]
        if rule.advice and (rule.is_scored or not rule.detector or not rule.applies):
            found.append(f"{where}: advice is for an unscored rule with a detector and facts")
        if rule.is_scored and not rule.detector:
            found.append(f"{where}: an adopt rule is scored, it needs a detector")
        if rule.is_scored and not any(
            today - source.checked <= SOURCE_MAX_AGE for source in rule.sources
        ):
            found.append(f"{where}: an adopt rule needs a source checked in the last six months")
    return found
