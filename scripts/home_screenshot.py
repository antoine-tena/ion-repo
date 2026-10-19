"""Draw kiln's home screen (`kiln` alone) as the SVG shown at the top of the README.

    uv run python scripts/home_screenshot.py

The screen is the real one, rendered in colour for a demo project and without a version number
(the image would be out of date at each release); `tests/test_docs.py` fails when the committed
image no longer matches it.
"""

import io
import os
import re
from contextlib import redirect_stdout
from html import escape
from pathlib import Path
from unittest import mock

from kiln import banner, cli, ui

ROOT = Path(__file__).resolve().parent.parent
SVG_PATH = ROOT / "docs/assets/kiln-home.svg"
LOCATION = "~/code/atelier"

CELL, LINE, LEFT, TOP, BOTTOM = 8.4, 18, 22, 28, 12
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
TEXT, BACKGROUND = "#e6e3dc", "#1c1b19"
HALVES = {"▀": (0, 9.3), "▄": (9, 9.3), "█": (0, 18.3)}
SGR = re.compile(r"\033\[([\d;]*)m")


def home_screen() -> str:
    """The home screen with its colour codes, as a true-colour terminal shows it."""
    output = io.StringIO()
    with (
        mock.patch.dict(os.environ, {"COLORTERM": "truecolor"}),
        mock.patch.object(ui, "is_styled", lambda stream=None: True),
        mock.patch.object(banner, "installed_version", lambda: ""),
        mock.patch.object(banner, "_home_relative", lambda path: LOCATION),
        redirect_stdout(output),
    ):
        cli.show_home(cli.build_parser())
    return output.getvalue()


def hex_color(codes: list[str]) -> str:
    return "#" + "".join(f"{int(code):02x}" for code in codes)


def svg(screen: str) -> str:
    lines = screen.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    columns = max(len(SGR.sub("", line)) for line in lines)
    width = round(2 * LEFT + CELL * columns)
    height = TOP + LINE * len(lines) + BOTTOM
    shapes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="kiln welcome screen">',
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
            if code == "0":
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


def draw_run(
    text: str, column: int, top: int, foreground: str, background: str, bold: bool
) -> list[str]:
    x = LEFT + CELL * column
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
    stripped = text.lstrip(" ")
    if not stripped.strip():
        return []
    x += CELL * (len(text) - len(stripped))
    stripped = stripped.rstrip(" ")
    attributes = f'x="{round(x, 1)}" y="{top + 13.5}" textLength="{round(CELL * len(stripped), 1)}"'
    if foreground:
        attributes += f' fill="{foreground}"'
    if bold:
        attributes += ' font-weight="bold"'
    return [f"<text {attributes}>{escape(stripped, quote=False)}</text>"]


def main() -> None:
    SVG_PATH.write_text(svg(home_screen()), encoding="utf-8")
    print(f"{SVG_PATH.relative_to(ROOT)} written")


if __name__ == "__main__":
    main()
