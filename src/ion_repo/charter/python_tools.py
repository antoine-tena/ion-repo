"""Ratchets measured by Python tools: typing gaps (mypy) and coverage (pytest-cov)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from ion_repo.charter.config import CHARTER_FILE
from ion_repo.charter.repo import Repo

DEFAULT_MARGIN = 2


def types(repo: Repo) -> int:
    """`[types]`: `directory` (uv project), `packages` (given to mypy with -p), `budget` (gaps
    tolerated, which only goes down), `env` (variables the project's settings expect,
    overridden by the environment)."""
    params = repo.config["types"]
    env = {**params.get("env", {}), **os.environ}
    packages = [arg for package in params["packages"] for arg in ("-p", package)]
    command = ["uv", "run", "mypy", *packages]
    completed = subprocess.run(
        command,
        cwd=repo.root / params.get("directory", "backend"),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    output = completed.stdout + completed.stderr
    found = re.search(r"Found (\d+) errors? in \d+ files?", output)
    if found:
        gaps = int(found.group(1))
    elif "no issues found" in output:
        gaps = 0
    else:
        print(output, file=sys.stderr)
        print("mypy could not run: see its output above.", file=sys.stderr)
        return 2
    budget = params.get("budget", 0)
    if gaps > budget:
        print(output, file=sys.stderr)
        print(
            f"\nTyping: mypy found {gaps} gaps, for a ceiling of {budget}.\n"
            "Fix the new gaps, or annotate them with the reason.",
            file=sys.stderr,
        )
        return 1
    if gaps < budget:
        lower = f"lower `budget` of [types] to {gaps} ({CHARTER_FILE})"
        print(f"Typing: {gaps} gaps (ceiling {budget}): {lower}.")
        return 0
    print(f"Typing: {gaps} gaps, the ceiling holds ({', '.join(params['packages'])}).")
    return 0


def coverage(repo: Repo) -> int:
    """`[coverage]`: `report` (coverage.xml of `pytest --cov --cov-report=xml`), `floors`
    (percentage of covered lines for the `TOTAL` and for critical modules, which only goes up),
    `margin` (points above a floor before suggesting to raise it)."""
    params = repo.config["coverage"]
    report = repo.root / params["report"]
    if not report.exists():
        print(f"{report} not found: run `uv run pytest --cov --cov-report=xml` first.")
        return 1
    root = ET.parse(report).getroot()
    rates = {"TOTAL": float(root.get("line-rate", 0)) * 100}
    for element in root.iter("class"):
        rates[element.get("filename", "")] = float(element.get("line-rate", 0)) * 100
    margin = params.get("margin", DEFAULT_MARGIN)
    problems, to_raise = [], []
    for name, floor in params["floors"].items():
        measured = rates.get(name)
        if measured is None:
            problems.append(f"{name}: missing from the report (renamed? see [coverage.floors]).")
        elif measured < floor:
            problems.append(f"{name}: {measured:.1f} % of lines covered, under {floor} %.")
        elif measured >= floor + margin:
            raised = f"raise [coverage.floors] {name!r} to {int(measured)}"
            to_raise.append(f"{name}: {measured:.1f} %: {raised}.")
    if to_raise:
        print("Coverage going up, floors to raise (the check stays green):")
        print("\n".join(f"  {line}" for line in to_raise))
    if problems:
        print("Coverage under the floors:")
        print("\n".join(f"  {line}" for line in problems))
        return 1
    print("Coverage: every floor holds.")
    return 0
