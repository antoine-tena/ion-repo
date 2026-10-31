"""Waivers: deliberate deviations from an ion-repo rule, declared in `kiln-waivers.toml` at the root
of the repo. ion-repo never generates nor rewrites that file.

A waiver covers a rule (`rule`, an identifier of the charter), in the whole repo or in `paths`
(git patterns), with a reason, an author and an expiry. Trust is earned: the first period lasts
a week at most, then each renewal (`renewals`) lengthens the tier (a month, three months, six
months). `until = "never"` declares a permanent deviation, always shown. An expired waiver no
longer applies; a waiver that no longer matches anything fails, like a ratchet left too loose.
Some rules cannot be waived. Rule identifiers of before kiln 0.4.0 are understood.
"""

from __future__ import annotations

import datetime
import tomllib
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ion_repo.renames import rule_id

WAIVERS_FILE = "kiln-waivers.toml"
RULE_ID = "WAIVERS"
# Longest period, by number of renewals (the last tier repeats).
TIERS_DAYS = (7, 30, 90, 182)
NEVER = "never"
# Security and hygiene floors: no waiver.
NOT_WAIVABLE = frozenset({"PERSONAL-DATA", "NO-COMMIT-ON-MAIN", "LOCKED-DEPENDENCIES", "SECRETS"})
REQUIRED = ("reason", "by", "since", "until")
KNOWN_KEYS = frozenset({"rule", "paths", "file", *REQUIRED, "renewals", "upstream"})


@dataclass(frozen=True)
class Waiver:
    rule: str  # under its current name
    paths: tuple[str, ...]
    file: str
    reason: str
    by: str
    since: datetime.date
    until: datetime.date | None  # None: permanent (`until = "never"`)
    renewals: int

    @property
    def label(self) -> str:
        target = self.rule or f"file {self.file}"
        return f"{target} ({', '.join(self.paths)})" if self.paths else target


@dataclass
class Waivers:
    """Waivers read, and what reading them found (errors, warnings)."""

    actives: list[Waiver] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def for_rule(self, rule: str) -> list[Waiver]:
        return [waiver for waiver in self.actives if waiver.rule and waiver.rule == rule_id(rule)]

    def waived_paths(self, rule: str) -> list[str] | None:
        """Patterns left out for `rule`; None when a waiver covers the whole repo."""
        patterns: list[str] = []
        for waiver in self.for_rule(rule):
            if not waiver.paths:
                return None
            patterns.extend(waiver.paths)
        return patterns


def max_days(renewals: int) -> int:
    return TIERS_DAYS[min(renewals, len(TIERS_DAYS) - 1)]


def is_waivable(rule: str) -> bool:
    return rule_id(rule) not in NOT_WAIVABLE


def load(root: Path, today: datetime.date | None = None) -> Waivers:
    path = root / WAIVERS_FILE
    result = Waivers()
    if not path.exists():
        return result
    try:
        data = tomllib.loads(path.read_text("utf-8"))
    except tomllib.TOMLDecodeError as error:
        result.errors.append(f"{WAIVERS_FILE} unreadable: {error}")
        return result
    today = today or datetime.date.today()
    for index, entry in enumerate(data.get("waiver", []), start=1):
        _read(entry, f"waiver #{index}", today, result)
    return result


def _read(entry: dict[str, Any], where: str, today: datetime.date, result: Waivers) -> None:
    problems = _problems(entry)
    if problems:
        result.errors.append(f"{where}: {'; '.join(problems)}")
        return
    until = entry["until"]
    waiver = Waiver(
        rule=rule_id(entry.get("rule", "")),
        paths=tuple(entry.get("paths", [])),
        file=entry.get("file", ""),
        reason=entry["reason"],
        by=entry["by"],
        since=entry["since"],
        until=None if until == NEVER else until,
        renewals=entry.get("renewals", 0),
    )
    where = f"{where} [{waiver.label}]"
    if waiver.until is None:
        result.warnings.append(f"{where}: permanent ({waiver.reason})")
        result.actives.append(waiver)
        return
    allowed = max_days(waiver.renewals)
    days = (waiver.until - waiver.since).days
    if days > allowed:
        result.errors.append(
            f"{where}: {days} days, at most {allowed} after {waiver.renewals} renewal(s) "
            f"(tiers {', '.join(map(str, TIERS_DAYS))})"
        )
        return
    if today > waiver.until:
        result.errors.append(
            f"{where}: expired on {waiver.until}: fix it, or renew it (`ion repo waive --renew`, a "
            f"new period of {max_days(waiver.renewals + 1)} days at most)"
        )
        return
    left = (waiver.until - today).days
    if left * 2 <= days:
        result.warnings.append(f"{where}: expires on {waiver.until} (in {left} day(s))")
    result.actives.append(waiver)


def _problems(entry: dict[str, Any]) -> list[str]:
    problems = [f"unknown key `{key}`" for key in entry if key not in KNOWN_KEYS]
    problems += [f"`{key}` missing" for key in REQUIRED if not entry.get(key)]
    rule, file = entry.get("rule"), entry.get("file")
    if bool(rule) == bool(file):
        problems.append("one target, and only one: `rule` or `file`")
    if rule and not is_waivable(rule):
        problems.append(f"[{rule_id(rule)}] cannot be waived")
    if file and entry.get("paths"):
        problems.append("`paths` only goes with `rule`")
    if "since" in entry and not isinstance(entry["since"], datetime.date):
        problems.append("`since`: a date (2026-10-16)")
    until = entry.get("until")
    if until is not None and until != NEVER and not isinstance(until, datetime.date):
        problems.append(f'`until`: a date, or "{NEVER}"')
    renewals = entry.get("renewals", 0)
    if not isinstance(renewals, int) or renewals < 0:
        problems.append("`renewals`: a positive or null integer")
    return problems


def check_targets(
    waivers: Waivers, known_rules: Iterable[str], tracked: Callable[[list[str]], list[Path]]
) -> None:
    """A waiver that no longer targets anything (unknown rule, pattern without a file) is
    dropped and reported: otherwise it would silently cover the next file that matches it."""
    rules = {rule_id(rule) for rule in known_rules}
    kept = []
    for waiver in waivers.actives:
        if waiver.rule and waiver.rule not in rules:
            waivers.errors.append(f"[{waiver.label}]: no such rule in the repo's charter")
            continue
        empty = [pattern for pattern in (*waiver.paths, *filter(None, [waiver.file]))
                 if not tracked([pattern])]  # fmt: skip
        if empty:
            waivers.errors.append(f"[{waiver.label}]: no file for {', '.join(empty)}")
            continue
        kept.append(waiver)
    waivers.actives = kept
