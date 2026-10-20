"""Draw the README's images from kiln's real output, in `docs/assets/`.

    uv run python scripts/screenshots.py

Each terminal image is the screen kiln prints, rendered in colour (true-colour escape codes
turned into SVG), for a demo project and without a version number that would date it. The
diagram is drawn in kiln's palette, in a light and a dark variant; the logo and the social
preview draw the banner's kiln pixel by pixel. `tests/test_docs.py` fails when a committed image
no longer matches what this script draws: the README never shows an old screen. The animated
demo is recorded apart (`docs/assets/kiln-new.tape`).
"""

import io
import os
import re
import tempfile
from collections.abc import Callable
from contextlib import redirect_stdout, suppress
from dataclasses import dataclass
from html import escape
from pathlib import Path
from unittest import mock

from kiln import banner, cli, ui, update, versions

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/assets"
LOCATION = "~/code/atelier"
COLUMNS = 92

CELL, LINE, LEFT, TOP, BOTTOM = 8.4, 18, 22, 28, 12
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
TEXT, BACKGROUND, PROMPT = "#e6e3dc", "#1c1b19", "#8c8c87"
HALVES = {"▀": (0, 9.3), "▄": (9, 9.3), "█": (0, 18.3)}
SGR = re.compile(r"\033\[([\d;]*)m")


# --- Screens: what kiln prints, captured in colour ------------------------------------------


def captured(run: Callable[[], object]) -> str:
    """What `run` prints, with its colour codes, as a true-colour terminal of COLUMNS shows it."""
    output = io.StringIO()
    with (
        mock.patch.dict(os.environ, {"COLORTERM": "truecolor", "NO_COLOR": ""}),
        mock.patch.object(ui, "is_styled", lambda stream=None: True),
        mock.patch.object(ui, "_columns", lambda: COLUMNS),
        mock.patch.object(banner, "installed_version", lambda: ""),
        mock.patch.object(banner, "_home_relative", lambda path: LOCATION),
        redirect_stdout(output),
    ):
        run()
    return output.getvalue()


def home_screen() -> str:
    return captured(lambda: cli.show_home(cli.build_parser()))


def kiln_command(*arguments: str) -> Callable[[], object]:
    def run() -> None:
        with mock.patch("sys.argv", ["kiln", *arguments]), suppress(SystemExit):
            cli.main()

    return run


def grid_screen() -> str:
    return prompt("kiln grid") + captured(kiln_command("grid"))


def rule_screen() -> str:
    return prompt("kiln grid pinned-actions") + captured(kiln_command("grid", "pinned-actions"))


def update_screen() -> str:
    """The box `kiln update` shows when it crosses the latest release (from the changelog)."""
    notes = versions.parse_changelog(versions.read_changelog())
    current, previous = notes[0].tag, notes[1].tag

    def run() -> None:
        with tempfile.TemporaryDirectory() as scratch:
            update.show_release_notes(Path(scratch), previous, current)

    return prompt("kiln update") + captured(run)


def prompt(command: str) -> str:
    return f"\033[38;2;140;140;135m$\033[0m {command}\n"


# --- Terminal SVG ----------------------------------------------------------------------------


def hex_color(codes: list[str]) -> str:
    return "#" + "".join(f"{int(code):02x}" for code in codes)


def svg(screen: str, label: str = "kiln welcome screen") -> str:
    lines = screen.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    columns = max(len(SGR.sub("", line)) for line in lines)
    width = round(2 * LEFT + CELL * columns)
    height = TOP + LINE * len(lines) + BOTTOM
    shapes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">',
        f'<rect width="100%" height="100%" rx="10" fill="{BACKGROUND}"/>',
        '<circle cx="20" cy="18" r="6" fill="#ff5f57"/><circle cx="40" cy="18" r="6" '
        'fill="#febc2e"/><circle cx="60" cy="18" r="6" fill="#28c840"/>',
        f'<g font-family="{FONT}" font-size="14" fill="{TEXT}" xml:space="preserve">',
    ]
    for row, line in enumerate(lines):
        shapes += draw_line(line, TOP + LINE * row)
    shapes += ["</g>", "</svg>", ""]
    return "\n".join(shapes)


def draw_line(line: str, top: int) -> list[str]:
    """One terminal line: half-blocks of the logo as rectangles, runs of text as `<text>`."""
    shapes: list[str] = []
    column, foreground, background, bold = 0, "", "", False
    # `split` alternates the text and the codes of the escape sequence that follows it.
    parts = SGR.split(line)
    for text, sequence in zip(parts[0::2], [*parts[1::2], None], strict=True):
        shapes += draw_run(text, column, top, foreground, background, bold)
        column += len(text)
        codes = (sequence or "0").split(";") if sequence is not None else []
        while codes:
            code = codes.pop(0)
            if code in ("0", ""):
                foreground, background, bold = "", "", False
            elif code == "1":
                bold = True
            elif code in ("38", "48") and codes[:1] == ["2"]:
                color, codes = hex_color(codes[1:4]), codes[4:]
                if code == "38":
                    foreground = color
                else:
                    background = color
    return shapes


# Box drawing as strokes, so a frame's edges join from one line to the next: which edges of
# its cell each character reaches (left, right, up, down), and whether its corner is rounded.
BOX = {
    "─": "lr", "│": "ud", "├": "rud", "┤": "lud", "┬": "lrd", "┴": "lru", "┼": "lrud",
    "╭": "rd", "╮": "ld", "╰": "ru", "╯": "lu",
}  # fmt: skip
ROUNDED = frozenset("╭╮╰╯")


def draw_box(char: str, x: float, top: int, color: str) -> str:
    left, right, middle_x = x, x + CELL, x + CELL / 2
    up, down, middle_y = top, top + LINE, top + LINE / 2
    ends = {
        "l": (left, middle_y),
        "r": (right, middle_y),
        "u": (middle_x, up),
        "d": (middle_x, down),
    }
    stroke = f'stroke="{color}" stroke-width="1.2" fill="none"'
    if char in ROUNDED:
        (x1, y1), (x2, y2) = (ends[edge] for edge in BOX[char])
        curve = f"M{x1:.1f},{y1:.1f} Q{middle_x:.1f},{middle_y:.1f} {x2:.1f},{y2:.1f}"
        return f'<path d="{curve}" {stroke}/>'
    return "".join(
        f'<line x1="{middle_x:.1f}" y1="{middle_y:.1f}" x2="{ends[edge][0]:.1f}" '
        f'y2="{ends[edge][1]:.1f}" {stroke}/>'
        for edge in BOX[char]
    )


def draw_run(
    text: str, column: int, top: int, foreground: str, background: str, bold: bool
) -> list[str]:
    x = LEFT + CELL * column
    if text and all(char in BOX for char in text.strip(" ")) and text.strip(" "):
        offset = len(text) - len(text.lstrip(" "))
        return [
            draw_box(char, x + CELL * (offset + index), top, foreground or TEXT)
            for index, char in enumerate(text.strip(" "))
        ]
    if text and all(char in HALVES for char in text):
        shapes = []
        for index, char in enumerate(text):
            left = round(x + CELL * index, 1)
            if background:
                shapes.append(
                    f'<rect x="{left}" y="{top + 9}" width="8.7" height="9.3" fill="{background}"/>'
                )
            offset, height = HALVES[char]
            shapes.append(
                f'<rect x="{left}" y="{top + offset}" width="8.7" height="{height}" '
                f'fill="{foreground or TEXT}"/>'
            )
        return shapes
    # A browser collapses runs of spaces: each word group is placed at its own column.
    shapes = []
    for found in re.finditer(r"\S+(?: \S+)*", text):
        words = found.group()
        left = round(x + CELL * found.start(), 1)
        attributes = f'x="{left}" y="{top + 13.5}" textLength="{round(CELL * len(words), 1)}"'
        if foreground:
            attributes += f' fill="{foreground}"'
        if bold:
            attributes += ' font-weight="bold"'
        shapes.append(f"<text {attributes}>{escape(words, quote=False)}</text>")
    return shapes


# --- Diagram: one release, every repo current ------------------------------------------------


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    card: str
    border: str
    title: str
    text: str
    muted: str
    accent: str


THEMES = (
    Theme("light", "#ffffff", "#faf8f5", "#e2ddd5", "#1c1b19", "#3d3b37", "#7a776f", "#c2551f"),
    Theme("dark", "#0d1117", "#1c1b19", "#3a3833", "#f2efe8", "#d4d0c7", "#9a968c", "#f79628"),
)
# Each stage of a release, in order: its name, what it is, and what holds before the next one,
# in the words of someone who has never seen kiln.
STAGES = (
    ("kiln", ("template, rules,", "plugins, workflows"), "checked at each merge"),
    ("candidate", ("tried first on", "kiln's own repos"), "green on Linux, macOS"),
    ("release", ("on PyPI and", "GitHub Releases"), "next candidate ready"),
    ("rehearsal", ("your repo updated", "on a throwaway clone"), "green on every clone"),
    ("your repos", ("kiln update merges", "template and deps"), "only if checks pass"),
)


def flow_svg(theme: Theme) -> str:
    width, height, card_width, card_height, gap, top = 930, 232, 154, 116, 30, 62
    left = (width - 5 * card_width - 4 * gap) // 2
    shapes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="One kiln release, from a '
        "change checked to every repo updated: a candidate on a green CI, the release on PyPI, "
        'a rehearsal on a clone of each repo, then kiln update in each repo">',
        f'<rect width="100%" height="100%" rx="12" fill="{theme.background}"/>',
        "<g font-family=\"-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,"
        'sans-serif" text-anchor="middle">',
        f'<text x="{width // 2}" y="36" font-size="19" font-weight="600" fill="{theme.title}">'
        "One release, every repo current</text>",
    ]
    for index, (name, lines, gate) in enumerate(STAGES):
        x = left + index * (card_width + gap)
        center = x + card_width // 2
        shapes += [
            f'<rect x="{x}" y="{top}" width="{card_width}" height="{card_height}" rx="10" '
            f'fill="{theme.card}" stroke="{theme.border}"/>',
            f'<rect x="{x}" y="{top}" width="{card_width}" height="4" rx="2" '
            f'fill="{theme.accent}"/>',
            f'<text x="{center}" y="{top + 38}" font-size="17" font-weight="600" '
            f'fill="{theme.title}">{escape(name)}</text>',
        ]
        shapes += [
            f'<text x="{center}" y="{top + 68 + 20 * row}" font-size="14" fill="{theme.text}">'
            f"{escape(line)}</text>"
            for row, line in enumerate(lines)
        ]
        shapes.append(
            f'<text x="{center}" y="{top + card_height + 28}" font-size="13" '
            f'fill="{theme.muted}">✓ {escape(gate)}</text>'
        )
        if index < len(STAGES) - 1:
            start, end = x + card_width + 5, x + card_width + gap - 5
            middle = top + card_height // 2
            shapes += [
                f'<line x1="{start}" y1="{middle}" x2="{end - 5}" y2="{middle}" '
                f'stroke="{theme.accent}" stroke-width="2"/>',
                f'<path d="M{end - 6},{middle - 5} L{end},{middle} L{end - 6},{middle + 5} Z" '
                f'fill="{theme.accent}"/>',
            ]
    shapes += ["</g>", "</svg>", ""]
    return "\n".join(shapes)


# --- Logo and social preview: the banner's kiln, one square per pixel -----------------------


def rgb(color: ui.Color) -> str:
    return hex_color(color.true_color.split(";"))


def pixels(size: int, left: int = 0, top: int = 0) -> list[str]:
    """The kiln of the banner (`banner.LOGO`), each run of same-coloured pixels one rectangle."""
    return [
        f'<rect x="{left + size * found.start()}" y="{top + size * row}" '
        f'width="{size * len(found.group())}" height="{size}" '
        f'fill="{rgb(banner.LOGO_COLORS[found.group(1)])}"/>'
        for row, line in enumerate(banner.LOGO)
        for found in re.finditer(rf"([^{re.escape(banner.EMPTY)}])\1*", line)
    ]


def logo_svg(size: int = 12) -> str:
    """On a transparent ground, one image for the light and the dark themes."""
    width, height = size * len(banner.LOGO[0]), size * len(banner.LOGO)
    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" shape-rendering="crispEdges" role="img" '
        'aria-label="kiln: a laughing kiln in pixel art">'
    )
    return "\n".join([header, *pixels(size), "</svg>", ""])


# What a shared link shows (X, Bluesky, LinkedIn, Slack, Discord, Reddit): the name, the workshop
# and the promise, readable as a thumbnail. GitHub takes a PNG: `scripts/social_preview.py`.
BRAND = "Claude Code's workshop"
PROMISE = (
    "Start every new project, and",
    "rescue every old one, like a",
    "senior engineer would — even",
    "if you're not one.",
)


def social_preview_svg() -> str:
    width, height, left = 1280, 640, 560
    text = f'font-family="{FONT}"'
    label = escape(f"kiln, {BRAND}: {' '.join(PROMISE)}")
    shapes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">',
        '<defs><radialGradient id="glow" cx="0.25" cy="0.55" r="0.45">'
        '<stop offset="0" stop-color="#f79628" stop-opacity="0.22"/>'
        '<stop offset="1" stop-color="#f79628" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
        f'<rect width="{width}" height="{height}" fill="url(#glow)"/>',
        '<g shape-rendering="crispEdges">',
        *pixels(26, left=96, top=232),
        "</g>",
        f'<text x="{left}" y="196" {text} font-size="112" font-weight="bold" '
        'fill="#f2efe8">kiln</text>',
        f'<text x="{left}" y="258" {text} font-size="40" fill="#f79628">{escape(BRAND)}</text>',
    ]
    shapes += [
        f'<text x="{left}" y="{338 + 46 * row}" {text} font-size="34" fill="#f2efe8">'
        f"{escape(line)}</text>"
        for row, line in enumerate(PROMISE)
    ]
    shapes += [
        f'<text x="{left}" y="574" {text} font-size="24" fill="{PROMPT}">'
        "github.com/antoine-tena/kiln</text>",
        "</svg>",
        "",
    ]
    return "\n".join(shapes)


# --- All images ------------------------------------------------------------------------------


def images() -> dict[Path, str]:
    """Each image of the README, the reference and the social preview, and what it must contain
    today."""
    drawn = {
        ASSETS / "kiln-logo.svg": logo_svg(),
        ASSETS / "kiln-home.svg": svg(home_screen(), "kiln welcome screen: the commands"),
        ASSETS / "kiln-grid.svg": svg(grid_screen(), "kiln grid: the rules kiln stands behind"),
        ASSETS / "kiln-rule.svg": svg(rule_screen(), "kiln grid: one rule, its why and sources"),
        ASSETS / "kiln-update.svg": svg(update_screen(), "kiln update: what is new"),
        ASSETS / "social-preview.svg": social_preview_svg(),
    }
    drawn |= {ASSETS / f"kiln-flow-{theme.name}.svg": flow_svg(theme) for theme in THEMES}
    return drawn


def main() -> None:
    for path, content in images().items():
        path.write_text(content, encoding="utf-8")
        print(f"{path.relative_to(ROOT)} written")


if __name__ == "__main__":
    main()
