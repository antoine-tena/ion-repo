"""Draw the release plan of `ROADMAP.md` and `ROADMAP.fr.md` from the backlog.

    uv run python scripts/roadmap.py

The plan lives in the `## 🚀 Releases` section of `docs/backlog/backlog.md` (`/kiln:backlog
plan`); the roadmap shows it to people who never open the backlog: each release with what it
brings and why its work goes together, grouped by milestone. Only the part between the markers
is drawn, the same in both languages (the backlog is written in English); the words around it are
written by hand. `tests/test_docs.py` fails when the roadmap no longer shows the plan.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "docs/backlog/backlog.md"
ROADMAPS = (ROOT / "ROADMAP.md", ROOT / "ROADMAP.fr.md")
START = "<!-- roadmap:start: drawn from docs/backlog/backlog.md by scripts/roadmap.py -->"
END = "<!-- roadmap:end -->"
# The milestones whose releases are shown open; the later ones fold, for a page that reads.
OPEN = 2
RELEASE = re.compile(r"^### (v(\d+)\.(\d+)\.\d+) · (.+)$")


def releases() -> list[tuple[str, str, str, str, int]]:
    """Each planned release: version, milestone, title, why, tickets."""
    text = BACKLOG.read_text(encoding="utf-8")
    section = text[text.index("## 🚀 Releases") : text.index("## 🔴 Critical")]
    found = []
    for block in section.split("\n### ")[1:]:
        heading, *lines = ("### " + block).strip().splitlines()
        release = RELEASE.match(heading)
        if release is None:  # what shipped is in the changelog
            continue
        version, major, minor, title = release.groups()
        why = " ".join(line for line in lines if not line.startswith(("- ", "  ")))
        tickets = sum(1 for line in lines if line.startswith("- T-"))
        found.append((version, f"v{major}.{minor}", title, why, tickets))
    return found


def several(count: int, word: str) -> str:
    return f"{count} {word}{'s' * (count > 1)}"


def work(why: str, tickets: int) -> str:
    if why.startswith("Frozen:"):
        return "in its candidate"
    return several(tickets, "ticket") if tickets else "fixes as they come"


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def draw() -> str:
    plan = releases()
    milestones = list(dict.fromkeys(milestone for _, milestone, *_ in plan))
    lines = [START, ""]
    for rank, milestone in enumerate(milestones):
        rows = [release for release in plan if release[1] == milestone]
        table = ["| Release | What it brings | Why together | Planned work |", "|---|---|---|---|"]
        table += [
            f"| {version} | {cell(title)} | {cell(why)} | {work(why, tickets)} |"
            for version, _, title, why, tickets in rows
        ]
        count = several(len(rows), "release")
        if rank < OPEN:
            lines += [f"### {milestone}.x · {count}", "", *table, ""]
        else:
            summary = f"<details><summary><b>{milestone}.x</b> · {count}</summary>"
            lines += [summary, "", *table, "", "</details>", ""]
    return "\n".join([*lines, END])


def main() -> None:
    drawn = draw()
    for path in ROADMAPS:
        text = path.read_text(encoding="utf-8")
        new = text[: text.index(START)] + drawn + text[text.index(END) + len(END) :]
        if new != text:
            path.write_text(new, encoding="utf-8")
        print(f"{path.name}: {'drawn' if new != text else 'up to date'}")


if __name__ == "__main__":
    main()
