"""Draw the release plan of `ROADMAP.md` and `ROADMAP.fr.md` from the backlog.

    uv run python scripts/roadmap.py

The plan lives in `docs/backlog/releases/`, a file per release (`/repo:backlog plan`); the
roadmap shows it to people who never open the backlog: each release with what it
brings and why its work goes together, grouped by milestone. Only the part between the markers
is drawn, the same in both languages (the backlog is written in English); the words around it are
written by hand. `tests/test_docs.py` fails when the roadmap no longer shows the plan.
"""

from pathlib import Path

from ion_repo import tracker

ROOT = Path(__file__).resolve().parent.parent
ROADMAPS = (ROOT / "ROADMAP.md", ROOT / "ROADMAP.fr.md")
START = "<!-- roadmap:start: drawn from docs/backlog/releases/ by scripts/roadmap.py -->"
END = "<!-- roadmap:end -->"
# The milestones whose releases are shown open; the later ones fold, for a page that reads.
OPEN = 2


def releases() -> list[tuple[str, str, str, str, int]]:
    """Each planned release: version, milestone, title, why, tickets."""
    found = []
    for release in tracker.releases(ROOT):
        if not release.version:
            continue
        major, minor, _ = release.version.split(".")
        milestone = f"v{major}.{minor}"
        found.append(
            (f"v{release.version}", milestone, release.title, release.why, len(release.tickets))
        )
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
