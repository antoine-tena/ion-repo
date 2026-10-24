"""`kiln score --roadmap`: what no converter closes, handed to Claude as a short list.

Most of an agent's tokens go into exploring a repo to find what to do; the roadmap gives it the
places instead, so Claude pays to think, not to search. Each item has its rule, its why, where
to look (file and line) and how to prove it closed (`kiln score --rule ID`). An approximate
detector's places are candidates "to confirm": Claude confirms or dismisses each in one look,
and a dismissal is a waiver on that path (`kiln waive ID --paths … --permanent`), never flagged
again. `--write` turns the items into tickets of `docs/backlog/backlog.md`, once each.
"""

import datetime
import re
from pathlib import Path

from kiln import ui
from kiln.grid.score import Finding, Report
from kiln.shell import KilnError

BACKLOG = Path("docs") / "backlog" / "backlog.md"
NEXT_FREE = re.compile(r"Next free: T-(\d+)")
NORMAL_SECTION = "## 🟡 Normal"
SHOWN_LOCATIONS = 5
FALSE_POSITIVE = 'kiln waive {rule} --paths <file> --permanent --reason "false positive: …"'


def show_roadmap(report: Report) -> None:
    items = report.roadmap()
    title = ui.paint("kiln roadmap", ui.FIRE, bold=True)
    print(f"\n  {title}  {ui.paint(f'{len(items)} gap(s) for Claude', ui.GLOW, bold=True)}")
    if not items:
        scripted = sum(found.by_script for found in report.gaps)
        rest = f"; {scripted} closed by script: kiln fix" if scripted else ""
        print(ui.paint(f"  Nothing that needs judgment{rest}.", ui.STONE))
        return
    print(ui.paint("  Sure gaps first, then the smallest; each one +1 rule met.", ui.STONE))
    for number, found in enumerate(items, 1):
        mark = ui.paint("  to confirm", ui.FIRE) if found.confirm else ""
        print(f"\n  {number}. {ui.paint(found.rule, ui.EMBER, bold=True)}  {found.title}{mark}")
        print(ui.paint(f"     why: {found.why}", ui.STONE_LIGHT))
        for location in found.locations[:SHOWN_LOCATIONS]:
            print(ui.paint(f"     {location}", ui.STONE))
        if (more := len(found.locations) - SHOWN_LOCATIONS) > 0:
            print(ui.paint(f"     … and {more} more (kiln score --rule {found.rule})", ui.STONE))
        if found.detail:
            print(ui.paint(f"     {found.detail}", ui.STONE))
        print(ui.paint(f"     done when: kiln score --rule {found.rule}", ui.STONE))
    print(ui.paint("\n  One at a time with Claude Code: /kiln:modernize", ui.STONE))
    print(ui.paint(f"  A false positive: {FALSE_POSITIVE.format(rule='<ID>')}", ui.STONE))


def show_rule(report: Report, found: Finding | None, rule_id: str) -> None:
    """`--rule ID`: the proof that a gap is closed; fails while it is open."""
    if found is None:
        raise KilnError(f"{rule_id}: not scored in this repo (unknown, or not for its stacks)")
    if found.status != "fail":
        ui.success(f"{rule_id}: {found.status}, {found.title}")
        return
    print(f"\n  {ui.paint(rule_id, ui.EMBER, bold=True)}  {found.title}")
    for location in found.locations:
        print(ui.paint(f"    {location}", ui.STONE))
    if found.detail:
        print(ui.paint(f"    {found.detail}", ui.STONE))
    raise KilnError(f"{rule_id} still open ({len(found.locations) or 1} place(s))")


def write_tickets(root: Path, report: Report, today: datetime.date | None = None) -> list[str]:
    """One ticket per roadmap item not tracked yet, under 🟡 Normal; returns their IDs."""
    path = root / BACKLOG
    if not path.exists():
        raise KilnError(f"no {BACKLOG} in this repo: kiln adopt sets it up")
    text = path.read_text()
    match = NEXT_FREE.search(text)
    if match is None or NORMAL_SECTION not in text:
        raise KilnError(f"{BACKLOG}: no 'Next free: T-NN' or no '{NORMAL_SECTION}' section")
    number = int(match.group(1))
    day = (today or datetime.date.today()).isoformat()
    written, tickets = [], []
    for found in report.roadmap():
        if _marker(found.rule) in text:
            continue
        tickets.append(_ticket(number, found, day))
        written.append(f"T-{number:02d}")
        number += 1
    if not tickets:
        return []
    text = NEXT_FREE.sub(f"Next free: T-{number:02d}", text, count=1)
    text = text.replace(NORMAL_SECTION, NORMAL_SECTION + "\n\n" + "\n\n".join(tickets), 1)
    path.write_text(text)
    return written


def _marker(rule_id: str) -> str:
    return f"grid rule `{rule_id}`"


def _ticket(number: int, found: Finding, day: str) -> str:
    where = "\n".join(f"- [ ] `{location}`" for location in found.locations)
    confirm = " Candidates to confirm: a false positive is dismissed by a waiver." * found.confirm
    lines = [
        f"### T-{number:02d} · {found.title}",
        "- **Type**: improvement",
        "- **Status**: todo",
        f"- **Opened**: {day}",
        "- **Effort**: S · **Owner**: — · **Due**: —",
        f"- **Origin**: kiln score --roadmap, {_marker(found.rule)}",
        "",
        f"{found.why}{confirm} Source: {found.source}. Done when `kiln score --rule {found.rule}` "
        "passes and the checks stay green (`/kiln:modernize`).",
    ]
    if where:
        lines += ["", where]
    return "\n".join(lines)
