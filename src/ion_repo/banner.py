"""Banner of the long commands (`new`, `install`, `update`, `status`) and home screen.

The Ion logo, an ion in flight in pixel art, drawn in half blocks (two pixels per character, a
24-bit colour each), next to the version of ion-repo, the command run, the project and its folder.
Outside a terminal, or with `NO_COLOR`, a single line without the drawing: logs and captured
output stay readable.
"""

import shutil
import textwrap
from collections.abc import Sequence
from pathlib import Path

from ion_score import ui

from ion_repo.shell import KilnError
from ion_repo.stack import NO_FRAMEWORK, answers_if_any, load_stack
from ion_repo.versions import installed_version

# The ion in flight: a white-cyan head, its trail from blue to violet fading out. One pixel = six
# hex digits (red, green, blue), `......` an empty one; one character = two stacked pixels.
LOGO_PIXELS = (
    ".........................................................................................."
    "..........................................................................................",
    ".........................................................................................."
    "................................................2c4f8c3366ac407fd53366ac..................",
    ".........................................................................................."
    "......382f7c3a37874548a64f5bc5546bda5d82fa558bfc53a2fe5eb8ff63c0ff5eb8ff509df428518d......",
    "............................................................331d673f24804c2c99633ac76b47dd"
    "7155f26d5cf36a64f5676bf66373f7607af85b82fa529ffe65c4ff79dfff86e6ff79dfff65c4ff4e9af4......",
    "........................1e10412a1759311b6643258a4f2da35d35be6439ca6a3dd77141e37646ee744df1"
    "7155f26d5cf36a64f5676bf66373f7607af85786fb5ab0ff74dbffa6eeffc7f4ffa6eeff74dbff5ab0ff28518d",
    "............1c0e3d261452321b6a402386492898502da55631b15d35be6439ca6a3dd77141e37646ee744df1"
    "7155f26d5cf36a64f5676bf66373f7607af85588fc5cb4ff79dfffb4f1ffe1f9ffb4f1ff79dfff5cb4ff2e5da1",
    "..........................................291754331d6a3f24805330a96238c57141e37646ee744df1"
    "7155f26d5cf36a64f5676bf66373f7607af85984fa56a9ff6dd2ff8fe9ffa6eeff8fe9ff6dd2ff56a9ff......",
    "..............................................................................3c247a452e8f"
    "4c39a35c4dcc5d58d7676bf66373f7607af85d82fa5193fd5cb4ff6acdff70d6ff6acdff5cb4ff3d7acb......",
    ".........................................................................................."
    "..............................3544893e57a8466dc84683df52a2ff56a9ff52a2ff376db6............",
    ".........................................................................................."
    "............................................................244882........................",
)
EMPTY, PIXEL = "......", 6
RGB = tuple[int, int, int]


def _pixels(row: str) -> tuple[RGB | None, ...]:
    cells = (row[start : start + PIXEL] for start in range(0, len(row), PIXEL))
    return tuple(None if cell == EMPTY else _rgb(bytes.fromhex(cell)) for cell in cells)


def _rgb(channels: bytes) -> RGB:
    red, green, blue = channels
    return red, green, blue


LOGO = tuple(_pixels(row) for row in LOGO_PIXELS)
# The text beside it: the cyan of the head.
ACCENT = ui.Color("121;223;255", "117")
# Steps of the 256-colour cube, for the terminals without 24-bit colour.
CUBE_STEPS = (0, 95, 135, 175, 215, 255)
UPPER_HALF, LOWER_HALF, FULL_BLOCK = "▀", "▄", "█"
LOGO_MARGIN, TEXT_GAP, INDENT = "  ", "   ", "  "
REPO_URL = "github.com/antoine-tena/ion-repo"

# Home screen: command sections (name, role) and examples.
CommandGroup = tuple[str, Sequence[tuple[str, str]]]
# `ion-repo <command> --help`: sections of (flags, role).
OptionGroup = tuple[str, Sequence[tuple[str, str]]]


def show_banner(action: str, root: Path | None = None) -> None:
    """Shows the banner; `root`: the repo concerned, otherwise the current folder, no project."""
    kiln_version = installed_version()
    details = [action, *([_project_summary(root)] if root is not None else [])]
    location = _home_relative(root or Path.cwd())
    if not ui.is_styled():
        print(" · ".join([f"ion-repo {kiln_version}", *details, location]), flush=True)
        return
    # Five lines beside the logo's five: the text faces the head.
    text_lines = [
        "",
        f"{ui.paint('ion-repo', bold=True)} {ui.paint(kiln_version, ui.STONE)}",
        ui.paint(" · ".join(details), ACCENT),
        ui.paint(location, ui.STONE),
        "",
    ]
    print()
    for logo_line, text_line in zip(render_logo(), text_lines, strict=True):
        print(f"{LOGO_MARGIN}{logo_line}{TEXT_GAP}{text_line}".rstrip())
    print(flush=True)


def show_home(groups: Sequence[CommandGroup], examples: Sequence[str]) -> None:
    """`ion-repo` alone or `ion-repo --help`: banner, commands by section, examples."""
    show_banner("Claude Code's workshop")
    width = max(len(name) for _, commands in groups for name, _ in commands) + 3
    usage = ui.paint("<command> [options]", ui.STONE)
    print(f"{INDENT}{ui.paint('Usage', bold=True)}  ion-repo {usage}")
    for title, commands in groups:
        print(f"\n{INDENT}{ui.paint(title.upper(), ACCENT, bold=True)}")
        for name, role in commands:
            print(f"{INDENT}  {ui.paint(f'{name:<{width}}', ui.STONE_LIGHT, bold=True)}{role}")
    print(f"\n{INDENT}{ui.paint('EXAMPLES', ACCENT, bold=True)}")
    for example in examples:
        print(f"{INDENT}  {ui.paint('$', ui.STONE_DARK)} {example}")
    print(
        f"\n{INDENT}{ui.paint('ion-repo <command> --help', bold=True)}"
        f"{ui.paint(' for the options · ', ui.STONE)}"
        f"{ui.paint('ion-repo -V', bold=True)}{ui.paint(f' the version · {REPO_URL}', ui.STONE)}\n"
    )


def show_command_help(role: str, usage: str, groups: Sequence[OptionGroup]) -> None:
    """`ion-repo <command> --help`: the home screen's banner and layout, the command's options."""
    show_banner(role)
    columns = shutil.get_terminal_size((100, 24)).columns
    margin = " " * len(f"{INDENT}Usage  ")
    usage_lines = textwrap.wrap(usage, max(columns - len(margin), 30))
    print(f"{INDENT}{ui.paint('Usage', bold=True)}  {usage_lines[0]}")
    for line in usage_lines[1:]:
        print(f"{margin}{line}")
    width = max((len(flags) for _, options in groups for flags, _ in options), default=0) + 3
    for title, options in groups:
        print(f"\n{INDENT}{ui.paint(title.upper(), ACCENT, bold=True)}")
        for flags, text in options:
            lines = textwrap.wrap(text, max(columns - len(INDENT) - 2 - width, 30)) or [""]
            print(f"{INDENT}  {ui.paint(f'{flags:<{width}}', ui.STONE_LIGHT, bold=True)}{lines[0]}")
            for line in lines[1:]:
                print(f"{INDENT}  {' ' * width}{line}")
    print()


def render_logo() -> list[str]:
    return [
        "".join(_cell(top, bottom) for top, bottom in zip(top_row, bottom_row, strict=True))
        for top_row, bottom_row in zip(LOGO[0::2], LOGO[1::2], strict=True)
    ]


def _cell(top: RGB | None, bottom: RGB | None) -> str:
    if top is None:
        if bottom is None:
            return " "
        return f"{ui.foreground(_color(bottom))}{LOWER_HALF}{ui.RESET}"
    if bottom is None:
        return f"{ui.foreground(_color(top))}{UPPER_HALF}{ui.RESET}"
    if top == bottom:
        return f"{ui.foreground(_color(top))}{FULL_BLOCK}{ui.RESET}"
    return f"{ui.foreground(_color(top))}{ui.background(_color(bottom))}{UPPER_HALF}{ui.RESET}"


def _color(pixel: RGB) -> ui.Color:
    return ui.Color(";".join(map(str, pixel)), _ansi256(pixel))


def _ansi256(pixel: RGB) -> str:
    """The closest colour of the 256-colour palette: its cube of 216 or its grey ramp."""
    levels = [
        min(range(len(CUBE_STEPS)), key=lambda level: abs(CUBE_STEPS[level] - channel))
        for channel in pixel
    ]
    cube = tuple(CUBE_STEPS[level] for level in levels)
    grey_level = min(23, max(0, round((sum(pixel) / 3 - 8) / 10)))
    grey = (8 + 10 * grey_level,) * 3

    def distance(color: tuple[int, ...]) -> int:
        return sum((a - b) ** 2 for a, b in zip(color, pixel, strict=True))

    if distance(grey) < distance(cube):
        return str(232 + grey_level)
    red, green, blue = levels
    return str(16 + 36 * red + 6 * green + blue)


def _project_summary(root: Path) -> str:
    """Project name, size and frameworks: `demo · medium · django + nuxt, podman`."""
    try:
        answers = answers_if_any(root)
        stack = load_stack(root)
    except KilnError, OSError, ValueError:
        return root.name
    frameworks = [name for name in (stack.backend, stack.frontend) if name != NO_FRAMEWORK]
    pile = " + ".join(frameworks) + (", podman" if stack.has_podman else "")
    parts = [str(answers.get("name", root.name)), str(answers.get("size", "")), pile]
    return " · ".join(part for part in parts if part)


def _home_relative(path: Path) -> str:
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)
