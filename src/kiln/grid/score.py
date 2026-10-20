"""`kiln score`: any repo measured against the grid in seconds, without a token.

Each scored rule (level `adopt`) whose facts the repo has runs its detector; a rule with nothing
to look at (`n/a`) or outside the repo's stacks is left out of the count, and a waived one
(`kiln-waivers.toml`) is shown apart as an accepted deviation. The score is the share of the
rules that apply which pass, out of 100, overall and per pillar: every rule weighs the same,
so the number says how many of today's practices the repo follows. Deterministic, offline by
default, and nothing is written in the repo.
"""

import datetime
import json
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path, PurePosixPath

from kiln import ui
from kiln.charter.waivers import Waiver
from kiln.charter.waivers import load as load_waivers
from kiln.grid import detectors
from kiln.grid.facts import Repo, read_repo
from kiln.grid.model import PILLARS, Rule, load_rules

# The version of the `--json` output; it only goes up when a field changes meaning or leaves.
SCHEMA = 1
PASSED, FAILED, WAIVED, LEFT_OUT = "pass", "fail", "waived", "n/a"
TOP_GAPS = 3
SHOWN_LOCATIONS = 3
# Manifests of stacks the grid does not cover yet: listed at the end, never counted (T-38).
UNCOVERED = {
    "composer.json": "PHP",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "Gemfile": "Ruby",
    "mix.exs": "Elixir",
    "pubspec.yaml": "Dart",
    "Package.swift": "Swift",
}
ENDOFLIFE_API = "https://endoflife.date/api/{product}.json"


@dataclass(frozen=True)
class Finding:
    rule: str
    title: str
    pillar: str
    status: str  # pass, fail, waived, n/a
    why: str
    source: str
    fix: str  # what closes the gap
    regime: str
    locations: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True)
class Report:
    root: str
    score: int | None  # None when no rule applies
    pillars: dict[str, int | None]
    facts: tuple[str, ...]
    findings: tuple[Finding, ...]
    uncovered: tuple[str, ...] = ()
    schema: int = SCHEMA
    checked: str = field(default_factory=lambda: datetime.date.today().isoformat())

    @property
    def gaps(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.status == FAILED]

    def top_gaps(self) -> list[Finding]:
        """The gaps to close first: every rule weighs the same, so the cheapest first (a script
        closes it), then the strict ones (their detector is exact)."""
        return sorted(
            self.gaps,
            key=lambda found: (found.fix != "kiln fix", found.regime != "strict", found.rule),
        )[:TOP_GAPS]


def score_repo(root: Path, rules: list[Rule] | None = None) -> Report:
    repo = read_repo(root)
    waivers = load_waivers(root)
    findings = [
        _finding(rule, repo, waivers.for_rule(rule.id) or waivers.for_rule(rule.charter_rule))
        for rule in (rules if rules is not None else load_rules())
        if rule.is_scored and set(rule.applies) <= repo.facts
    ]
    counted = [found for found in findings if found.status in (PASSED, FAILED)]
    return Report(
        root=str(root),
        score=_percent(counted),
        pillars={
            pillar: _percent([found for found in counted if found.pillar == pillar])
            for pillar in PILLARS
        },
        facts=tuple(sorted(repo.facts)),
        findings=tuple(findings),
        uncovered=tuple(_uncovered(repo)),
    )


def _finding(rule: Rule, repo: Repo, waived: list[Waiver]) -> Finding:
    outcome = detectors.detect(rule.detector, repo)
    status = {detectors.PASS: PASSED, detectors.FAIL: FAILED}.get(outcome.status, LEFT_OUT)
    if waived and status == FAILED:
        status = WAIVED
    return Finding(
        rule=rule.id,
        title=rule.title,
        pillar=rule.pillar,
        status=status,
        why=rule.why,
        source=rule.sources[0].url if rule.sources else "",
        fix="kiln fix" if rule.fixer else "by judgment (Claude Code)",
        regime=rule.regime,
        locations=outcome.locations if status != PASSED else (),
        detail=outcome.detail if status != PASSED else "",
    )


def _percent(findings: list[Finding]) -> int | None:
    if not findings:
        return None
    return round(100 * sum(found.status == PASSED for found in findings) / len(findings))


def _uncovered(repo: Repo) -> list[str]:
    found = {
        UNCOVERED[PurePosixPath(name).name]
        for name in repo.files
        if PurePosixPath(name).name in UNCOVERED
    }
    return sorted(f"{stack}: not covered by the grid yet" for stack in found)


def refresh_end_of_life() -> None:
    """`--online`: the end-of-life dates of the runtimes from endoflife.date, for this run."""
    for runtime, product in (("python", "python"), ("node", "nodejs")):
        with urllib.request.urlopen(ENDOFLIFE_API.format(product=product), timeout=10) as answer:
            cycles = json.load(answer)
        detectors.END_OF_LIFE[runtime] = {
            str(cycle["cycle"]): str(cycle["eol"])
            for cycle in cycles
            if isinstance(cycle.get("eol"), str)
        }


# --- output ---------------------------------------------------------------------------------


def badge(report: Report) -> str:
    value = "n/a" if report.score is None else f"{report.score}%2F100"
    color = (
        "lightgrey"
        if report.score is None
        else "brightgreen"
        if report.score >= 90
        else "yellow"
        if report.score >= 70
        else "orange"
        if report.score >= 50
        else "red"
    )
    image = f"https://img.shields.io/badge/kiln_score-{value}-{color}"
    return f"[![kiln score]({image})](https://github.com/antoine-tena/kiln)"


def as_json(report: Report) -> str:
    data = asdict(report)
    data["top_gaps"] = [found.rule for found in report.top_gaps()]
    return json.dumps(data, indent=2, ensure_ascii=False)


def show(report: Report, *, every: bool = False) -> None:
    score = "n/a" if report.score is None else f"{report.score}/100"
    title = ui.paint("kiln score", ui.FIRE, bold=True)
    print(f"\n  {title}  {ui.paint(score, ui.GLOW, bold=True)}")
    pillars = [f"{pillar} {value}" for pillar, value in report.pillars.items() if value is not None]
    print(ui.paint(f"  {'  ·  '.join(pillars)}", ui.STONE_LIGHT))
    print(ui.paint(f"  stacks: {', '.join(report.facts) or 'none found'}", ui.STONE))
    counted = [found for found in report.findings if found.status in (PASSED, FAILED)]
    passed = sum(found.status == PASSED for found in counted)
    print(ui.paint(f"  {passed} of {len(counted)} rules met", ui.STONE))
    if top := report.top_gaps():
        print(f"\n  {ui.paint('Close first', ui.FIRE, bold=True)}")
        for found in top:
            print(f"    {ui.paint(found.rule, ui.EMBER, bold=True)}  {found.title}")
    _section("Gaps", report.gaps, ui.EMBER, locations=True, every=every)
    waived = [found for found in report.findings if found.status == WAIVED]
    _section("Waived (accepted deviations)", waived, ui.STONE, locations=False, every=every)
    if every:
        met = [found for found in report.findings if found.status == PASSED]
        _section("Met", met, ui.MOSS, locations=False, every=every)
        left_out = [found for found in report.findings if found.status == LEFT_OUT]
        _section("Nothing to look at", left_out, ui.STONE, locations=False, every=every)
    if report.uncovered:
        print(f"\n  {ui.paint('What the grid does not know', ui.FIRE, bold=True)}")
        for line in report.uncovered:
            print(ui.paint(f"    {line}", ui.STONE))
    hint = "" if every else "--all for every rule and location · "
    print(ui.paint(f"\n  {hint}kiln grid <ID> for a rule in full", ui.STONE))
    print(ui.paint('  A deviation this repo accepts: kiln waive <ID> --reason "…"', ui.STONE))


def _section(
    title: str, findings: list[Finding], color: ui.Color, *, locations: bool, every: bool
) -> None:
    if not findings:
        return
    print(f"\n  {ui.paint(title, ui.FIRE, bold=True)}")
    for found in findings:
        print(f"    {ui.paint(found.rule, color, bold=True)}  {found.title}")
        if not locations:
            continue
        print(ui.paint(f"      why: {found.why}", ui.STONE_LIGHT))
        where = found.locations if every else found.locations[:SHOWN_LOCATIONS]
        for location in where:
            print(ui.paint(f"      {location}", ui.STONE))
        if (more := len(found.locations) - len(where)) > 0:
            print(ui.paint(f"      … and {more} more", ui.STONE))
        if found.detail:
            print(ui.paint(f"      {found.detail}", ui.STONE))
        print(ui.paint(f"      fix: {found.fix} · source: {found.source}", ui.STONE))
