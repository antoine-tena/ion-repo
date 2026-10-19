"""Banner of the long commands (`new`, `install`, `update`, `status`) and home screen.

A laughing kiln in pixel art (stone and fire), drawn in half blocks (two pixels per character),
next to the version of kiln, the command run, the project and its folder.
Outside a terminal, or with `NO_COLOR`, a single line without the drawing: logs and captured
output stay readable.
"""

from collections.abc import Sequence
from pathlib import Path

from kiln import ui
from kiln.shell import KilnError
from kiln.stack import NO_FRAMEWORK, answers_if_any, load_stack
from kiln.versions import installed_version

# One character = two stacked pixels. L lit stone, B stone, b stone in shadow, d brick base and
# cap, W/K eyes, P cheeks, R/F/Y flame (edge, body, heart), . empty.
LOGO = (
    "..........dd..",
    "...LLLBBB.bb..",
    "..LWKBBWKBbb..",
    ".LLWKBBWKBBbb.",
    ".LBP.RR..PBbb.",
    ".LBB.RFR..Bbb.",
    ".BBB.FYYF.bbb.",
    "dddddddddddddd",
)
LOGO_COLORS = {
    "L": ui.STONE_LIGHT,
    "B": ui.STONE,
    "b": ui.STONE_DARK,
    "d": ui.BRICK,
    "W": ui.WHITE,
    "K": ui.SOOT,
    "P": ui.CHEEK,
    "R": ui.EMBER,
    "F": ui.FIRE,
    "Y": ui.GLOW,
}
EMPTY = "."
UPPER_HALF, LOWER_HALF, FULL_BLOCK = "▀", "▄", "█"
LOGO_MARGIN, TEXT_GAP, INDENT = "  ", "   ", "  "
REPO_URL = "github.com/antoine-tena/kiln"

# Home screen: command sections (name, role) and examples.
CommandGroup = tuple[str, Sequence[tuple[str, str]]]


def show_banner(action: str, root: Path | None = None) -> None:
    """Shows the banner; `root`: the repo concerned, otherwise the current folder, no project."""
    kiln_version = installed_version()
    details = [action, *([_project_summary(root)] if root is not None else [])]
    location = _home_relative(root or Path.cwd())
    if not ui.is_styled():
        print(" · ".join([f"kiln {kiln_version}", *details, location]), flush=True)
        return
    text_lines = [
        "",
        f"{ui.paint('kiln', bold=True)} {ui.paint(kiln_version, ui.STONE)}",
        ui.paint(" · ".join(details), ui.FIRE),
        ui.paint(location, ui.STONE),
    ]
    print()
    for logo_line, text_line in zip(render_logo(), text_lines, strict=True):
        print(f"{LOGO_MARGIN}{logo_line}{TEXT_GAP}{text_line}".rstrip())
    print(flush=True)


def show_home(groups: Sequence[CommandGroup], examples: Sequence[str]) -> None:
    """`kiln` alone or `kiln --help`: banner, commands by section, examples."""
    show_banner("Claude Code's workshop")
    width = max(len(name) for _, commands in groups for name, _ in commands) + 3
    usage = ui.paint("<command> [options]", ui.STONE)
    print(f"{INDENT}{ui.paint('Usage', bold=True)}  kiln {usage}")
    for title, commands in groups:
        print(f"\n{INDENT}{ui.paint(title.upper(), ui.FIRE, bold=True)}")
        for name, role in commands:
            print(f"{INDENT}  {ui.paint(f'{name:<{width}}', ui.STONE_LIGHT, bold=True)}{role}")
    print(f"\n{INDENT}{ui.paint('EXAMPLES', ui.FIRE, bold=True)}")
    for example in examples:
        print(f"{INDENT}  {ui.paint('$', ui.STONE_DARK)} {example}")
    print(
        f"\n{INDENT}{ui.paint('kiln <command> --help', bold=True)}"
        f"{ui.paint(f' for the options · {REPO_URL}', ui.STONE)}\n"
    )


def render_logo() -> list[str]:
    def cell(top: str, bottom: str) -> str:
        if top == EMPTY and bottom == EMPTY:
            return " "
        if bottom == EMPTY:
            return f"{ui.foreground(LOGO_COLORS[top])}{UPPER_HALF}{ui.RESET}"
        if top == EMPTY:
            return f"{ui.foreground(LOGO_COLORS[bottom])}{LOWER_HALF}{ui.RESET}"
        if top == bottom:
            return f"{ui.foreground(LOGO_COLORS[top])}{FULL_BLOCK}{ui.RESET}"
        colors = ui.foreground(LOGO_COLORS[top]) + ui.background(LOGO_COLORS[bottom])
        return f"{colors}{UPPER_HALF}{ui.RESET}"

    return [
        "".join(cell(top, bottom) for top, bottom in zip(top_row, bottom_row, strict=True))
        for top_row, bottom_row in zip(LOGO[0::2], LOGO[1::2], strict=True)
    ]


def _project_summary(root: Path) -> str:
    """Project name, size and frameworks: `demo · flame · django + nuxt, podman`."""
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
