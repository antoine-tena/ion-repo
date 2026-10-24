"""`kiln waive`: lists, adds or renews a waiver of `kiln-waivers.toml`.

The command fills in what one forgets by hand (author, dates, tier) and refuses what `charter`
would refuse. It only touches the entry concerned: the rest of the file, comments included,
stays as is.
"""

import datetime
import re
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

from kiln import ui
from kiln.charter.cli import waivers_of
from kiln.charter.config import load
from kiln.charter.repo import Repo
from kiln.charter.waivers import NEVER, TIERS_DAYS, WAIVERS_FILE, is_waivable, max_days
from kiln.renames import rule_id
from kiln.shell import KilnError

RULE_ID = re.compile(r"[A-Z0-9+-]+")
TIERS = ", ".join(map(str, TIERS_DAYS[:-1])) + f" then {TIERS_DAYS[-1]}"
HEADER = f"""\
# This repo's waivers of kiln's rules ([WAIVERS]), checked by `charter`.
# kiln never rewrites this file; `kiln waive` adds or renews an entry.
# Duration at most: {TIERS} days, next tier at each renewal.
"""


@dataclass(frozen=True)
class WaiveRequest:
    target: str  # rule identifier, or path of a file to freeze
    reason: str
    paths: tuple[str, ...] = ()
    renew: bool = False
    permanent: bool = False
    upstream: str = ""


def show_waivers(root: Path) -> None:
    waivers = waivers_of(_repo(root))
    if not (waivers.actives or waivers.errors):
        ui.note(f"No waiver ({WAIVERS_FILE}). To add one: kiln waive <RULE> --reason …")
        return
    lines = [
        f"- {w.label}: {w.reason} ({w.by}, until {w.until or 'never'}, {w.renewals} renewal(s))"
        for w in waivers.actives
    ]
    lines += [f"! {message}" for message in waivers.warnings + waivers.errors]
    ui.panel(f"Waivers ({WAIVERS_FILE})", lines)


def waive(root: Path, request: WaiveRequest, today: datetime.date | None = None) -> None:
    today = today or datetime.date.today()
    if not request.reason.strip():
        raise KilnError('a waiver needs a reason: --reason "why"')
    is_rule = RULE_ID.fullmatch(request.target) is not None
    if is_rule and not is_waivable(request.target):
        raise KilnError(f"[{request.target}] cannot be waived")
    if not is_rule and request.paths:
        raise KilnError("--paths only goes with a rule; a file is frozen whole")
    path = root / WAIVERS_FILE
    text = path.read_text("utf-8") if path.exists() else HEADER
    blocks = _split(text)
    key = "rule" if is_rule else "file"
    index = next(
        (
            i
            for i, block in enumerate(blocks[1:], start=1)
            if _matches(block, key, request.target, request.paths)
        ),
        None,
    )
    if request.renew and index is None:
        raise KilnError(f"no waiver to renew for {request.target}")
    if not request.renew and index is not None:
        raise KilnError(f"{request.target} is already waived: --renew to extend it")
    renewals = 0 if index is None else _renewals(blocks[index]) + 1
    until = NEVER if request.permanent else today + datetime.timedelta(days=max_days(renewals))
    entry = {
        key: request.target,
        "paths": list(request.paths),
        "reason": request.reason.strip(),
        "by": _git_user(root),
        "since": today,
        "until": until,
        "renewals": renewals,
        "upstream": request.upstream,
    }
    block = _block(entry)
    if index is None:
        blocks.append(block)
    else:
        blocks[index] = block
    previous = path.read_text("utf-8") if path.exists() else None
    path.write_text(_join(blocks), "utf-8")
    target = rule_id(request.target) if is_rule else request.target
    # Read as of the day the waiver was written, not the clock's: a waiver written for a given
    # day is valid on that day.
    problems = [error for error in waivers_of(_repo(root), today).errors if target in error]
    if problems:
        _restore(path, previous)
        raise KilnError("waiver refused: " + "; ".join(problems))
    ui.note(
        f"{request.target} waived until {until} ({WAIVERS_FILE}, to commit). If the rule is "
        "wrong for everyone: skill /kiln:report, then --upstream <link>."
    )


def _repo(root: Path) -> Repo:
    return Repo(root, load(root))


def _split(text: str) -> list[str]:
    """Header, then one block per `[[waiver]]` (the comments that follow it included)."""
    parts = re.split(r"(?m)^(?=\[\[waiver\]\]\s*$)", text)
    return parts if parts else [""]


def _join(blocks: list[str]) -> str:
    return (
        "".join(b if b.endswith("\n\n") else b.rstrip("\n") + "\n\n" for b in blocks).rstrip("\n")
        + "\n"
    )


def _matches(block: str, key: str, target: str, paths: tuple[str, ...]) -> bool:
    try:
        entries = tomllib.loads(block).get("waiver", [])
    except tomllib.TOMLDecodeError:
        return False
    return any(
        e.get(key) == target and (not paths or tuple(e.get("paths", [])) == paths) for e in entries
    )


def _renewals(block: str) -> int:
    return int(tomllib.loads(block)["waiver"][0].get("renewals", 0))


def _block(entry: dict[str, object]) -> str:
    lines = ["[[waiver]]"]
    for key, value in entry.items():
        if value in ("", [], None):
            continue
        lines.append(f"{key} = {_toml(value)}")
    return "\n".join(lines) + "\n"


def _toml(value: object) -> str:
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml(v) for v in value) + "]"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _restore(path: Path, previous: str | None) -> None:
    if previous is None:
        path.unlink()
    else:
        path.write_text(previous, "utf-8")


def _git_user(root: Path) -> str:
    """Author of the waiver: git's `user.name`, "unknown" if it is not set."""
    found = subprocess.run(
        ["git", "config", "user.name"], cwd=root, capture_output=True, text=True, check=False
    )
    return found.stdout.strip() or "unknown"
