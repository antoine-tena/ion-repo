"""Terminal styles: stone and fire palette (the one of the banner's ion-repo) and messages.

Colors only go to a terminal, without `NO_COLOR` or `TERM=dumb`: outside a terminal the text
stays bare, for logs and captured output. 24-bit when the terminal says so (`COLORTERM`),
otherwise the 256-color palette.
"""

import os
import shutil
import sys
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TextIO


@dataclass(frozen=True)
class Color:
    true_color: str  # "r;g;b"
    palette: str  # index in the 256 colors


STONE_LIGHT = Color("185;185;180", "250")
STONE = Color("140;140;135", "245")
STONE_DARK = Color("95;95;92", "240")
BRICK = Color("180;75;35", "130")
FIRE = Color("247;150;40", "208")
EMBER = Color("205;50;35", "160")
GLOW = Color("255;225;120", "222")
MOSS = Color("130;190;110", "107")
WHITE = Color("255;255;255", "231")
SOOT = Color("25;25;25", "234")
CHEEK = Color("230;130;120", "174")

BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"


def is_styled(stream: TextIO | None = None) -> bool:
    """`stream`: sys.stdout by default, read at call time (pytest replaces it)."""
    return (
        (stream or sys.stdout).isatty()
        and "NO_COLOR" not in os.environ
        and os.environ.get("TERM", "") != "dumb"
    )


def foreground(color: Color) -> str:
    return _escape(38, color)


def background(color: Color) -> str:
    return _escape(48, color)


def _escape(layer: int, color: Color) -> str:
    if os.environ.get("COLORTERM", "") in ("truecolor", "24bit"):
        return f"\033[{layer};2;{color.true_color}m"
    return f"\033[{layer};5;{color.palette}m"


def paint(
    text: str,
    color: Color | None = None,
    *,
    bold: bool = False,
    dim: bool = False,
    stream: TextIO | None = None,
) -> str:
    """The text in color for this stream, or as is if it takes no colors."""
    if not is_styled(stream):
        return text
    codes = (BOLD if bold else "") + (DIM if dim else "") + (foreground(color) if color else "")
    return f"{codes}{text}{RESET}" if codes else text


@dataclass
class StepRecord:
    title: str
    started: float = field(default_factory=time.monotonic)
    ended: float | None = None
    failed: bool = False

    @property
    def duration(self) -> float:
        return (self.ended or time.monotonic()) - self.started


# Steps of the running command, for the final recap.
_steps: list[StepRecord] = []
# Spinner told of each step meanwhile, for work whose output goes elsewhere (`update --all`).
_step_watchers: list[Spinner] = []


def step(title: str) -> None:
    """Start of a step: a fire diamond and the title in bold; the previous step closes."""
    _close_last_step()
    _steps.append(StepRecord(title))
    for watcher in _step_watchers:
        watcher.show(title)
    if is_styled():
        print(f"\n{paint('◆', FIRE)} {paint(title, bold=True)}", flush=True)
    else:
        print(f"\n==> {title}", flush=True)


@contextmanager
def steps_elsewhere(spinner: Spinner | None) -> Iterator[None]:
    """Steps whose output goes to a log: their title shown by `spinner`, if any, and left out of
    the final recap."""
    kept = len(_steps)
    if spinner is not None:
        _step_watchers.append(spinner)
    try:
        yield
    finally:
        _step_watchers.clear()
        del _steps[kept:]


def success(message: str) -> None:
    print(f"\n{paint('✓', MOSS, bold=True)} {paint(message, bold=True)}", flush=True)


def note(message: str) -> None:
    print(paint(message, dim=True), flush=True)


def error(message: str) -> None:
    mark = paint("✗", EMBER, bold=True, stream=sys.stderr)
    print(f"{mark} {paint('ion-repo', bold=True, stream=sys.stderr)}: {message}", file=sys.stderr)


def _close_last_step() -> None:
    if _steps and _steps[-1].ended is None:
        _steps[-1].ended = time.monotonic()


def format_duration(seconds: float) -> str:
    """`0.4 s`, `12 s`, `1 min 05 s`."""
    if seconds < 10:
        return f"{seconds:.1f} s"
    if seconds < 60:
        return f"{seconds:.0f} s"
    minutes, rest = divmod(round(seconds), 60)
    return f"{minutes} min {rest:02d} s"


def _columns() -> int:
    return shutil.get_terminal_size((100, 24)).columns


def _fit(text: str, width: int) -> str:
    return text if len(text) <= width else text[: max(width - 1, 0)] + "…"


SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
SPINNER_DELAY = 0.08


class Spinner:
    """Animated line during an external command: fire wheel, command, time elapsed, last line
    of its output in grey. At the end, a fixed line: ✓ or ✗, the command and its duration."""

    def __init__(self, label: str, stream: TextIO | None = None) -> None:
        self.label = label
        # sys.stdout by default, read at call time; the terminal while stdout goes to a log.
        self._stream = stream
        self.detail = ""
        self.started = time.monotonic()
        self._stopped = threading.Event()
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    @property
    def stream(self) -> TextIO:
        return self._stream or sys.stdout

    def start(self) -> None:
        self.stream.write("\033[?25l")  # cursor hidden during the animation
        self._thread.start()

    def stop(self) -> None:
        """Clears the animated line and restores the cursor; no effect the second time."""
        if self._stopped.is_set():
            return
        self._stopped.set()
        self._thread.join()
        self.stream.write("\r\033[2K\033[?25h")
        self.stream.flush()

    def show(self, line: str) -> None:
        if line.strip():
            with self._lock:
                self.detail = line.strip()

    def finish(self, *, succeeded: bool, output: str = "") -> None:
        """Final line; on failure, the step is marked and the output shown in a margin."""
        self.stop()
        if not succeeded and _steps:
            _steps[-1].failed = True
        stream = self.stream
        mark = (
            paint("✓", MOSS, stream=stream)
            if succeeded
            else paint("✗", EMBER, bold=True, stream=stream)
        )
        elapsed = paint(format_duration(time.monotonic() - self.started), STONE_DARK, stream=stream)
        label = _fit(self.label, _columns() - 16)
        print(f"  {mark} {paint(label, STONE, stream=stream)}  {elapsed}", file=stream, flush=True)
        if not succeeded:
            margin = paint("│", EMBER, stream=stream)
            for line in output.rstrip().splitlines():
                print(f"    {margin} {line}", file=stream)
            stream.flush()

    def _spin(self) -> None:
        frame = 0
        while not self._stopped.wait(SPINNER_DELAY):
            with self._lock:
                detail = self.detail
            label = _fit(self.label, _columns() // 2)
            elapsed = format_duration(time.monotonic() - self.started)
            room = _columns() - len(label) - len(elapsed) - 10
            stream = self.stream
            wheel = paint(SPINNER_FRAMES[frame % len(SPINNER_FRAMES)], FIRE, stream=stream)
            text = paint(label, STONE_LIGHT, stream=stream)
            text += paint(f"  {elapsed}", STONE_DARK, stream=stream)
            if detail and room > 10:
                text += paint(f"  {_fit(detail, room)}", STONE_DARK, stream=stream)
            stream.write(f"\r\033[2K  {wheel} {text}")
            stream.flush()
            frame += 1


RECAP_TITLES = {
    "new": "Project created",
    "install": "Install done",
    "update": "Update done",
    "check": "Checks done",
    "set": "Settings applied",
    "contract": "Contract regenerated",
    "publish": "Repo published",
}


def recap(command: str, started: float, *, succeeded: bool) -> None:
    """Framed recap of the command: verdict, total duration, duration of each step."""
    _close_last_step()
    if not _steps:
        return
    total = format_duration(time.monotonic() - started)
    if succeeded:
        verdict = f"{RECAP_TITLES.get(command, 'Done')} in {total}"
    else:
        verdict = f"Interrupted after {total}"
    if not is_styled():
        count = len(_steps)
        print(f"\n{verdict} ({count} step{'s' if count > 1 else ''})", flush=True)
        return
    durations = [format_duration(record.duration) for record in _steps]
    inner = min(
        max(
            len(verdict) + 2,
            *(len(r.title) + len(d) + 6 for r, d in zip(_steps, durations, strict=True)),
        ),
        _columns() - 6,
    )
    edge = foreground(STONE_DARK)
    bar = f"{edge}│{RESET}"
    mark = paint("✓", MOSS, bold=True) if succeeded else paint("✗", EMBER, bold=True)
    print(f"\n  {edge}╭{'─' * (inner + 2)}╮{RESET}")
    head = paint(_fit(verdict, inner - 2), bold=True)
    print(f"  {bar} {mark} {head}{' ' * (inner - 2 - len(_fit(verdict, inner - 2)))} {bar}")
    print(f"  {edge}├{'─' * (inner + 2)}┤{RESET}")
    for index, (record, duration) in enumerate(zip(_steps, durations, strict=True)):
        is_failure = record.failed or (not succeeded and index == len(_steps) - 1)
        title = _fit(record.title, inner - len(duration) - 4)
        gap = " " * (inner - 2 - len(title) - len(duration))
        dot = paint("✗", EMBER) if is_failure else paint("·", STONE_DARK)
        shown = paint(title, EMBER) if is_failure else title
        print(f"  {bar} {dot} {shown}{gap}{paint(duration, STONE)} {bar}")
    print(f"  {edge}╰{'─' * (inner + 2)}╯{RESET}", flush=True)


def panel(title: str, lines: list[str]) -> None:
    """Frame: a title in fire, then lines (a `vN …` line in bold, `- …` as a bullet). A long
    line wraps under its own text, never cut; `code` spans of the changelog show in colour,
    without their backticks."""
    if not is_styled():
        print(f"\n{title}", *(f"  {line}" for line in lines), sep="\n", flush=True)
        return
    widest = max(len(title), *(len(line.replace("`", "")) for line in lines))
    inner = min(widest + 2, _columns() - 6)
    edge = foreground(STONE_DARK)
    bar = f"{edge}│{RESET}"
    print(f"\n  {edge}╭{'─' * (inner + 2)}╮{RESET}")
    shown_title = _fit(title, inner)
    print(f"  {bar} {paint(shown_title, FIRE, bold=True)}{' ' * (inner - len(shown_title))} {bar}")
    print(f"  {edge}├{'─' * (inner + 2)}┤{RESET}")
    for line in lines:
        is_bullet = line.startswith("- ")
        is_heading = line[:1] == "v" and line[1:2].isdigit()
        body = line[2:] if is_bullet else line
        indent = 2 if is_bullet else 0
        for index, words in enumerate(_wrap_words(_code_words(body), inner - indent)):
            visible = " ".join(_visible(word) for word in words)
            styled = " ".join(
                "".join(paint(piece, GLOW) if is_code else piece for piece, is_code in word)
                for word in words
            )
            if is_heading:
                styled = paint(visible, bold=True)
            elif not is_bullet:
                styled = paint(visible, STONE)
            lead = (paint("·", FIRE) + " " if index == 0 else "  ") if is_bullet else ""
            gap = " " * (inner - indent - len(visible))
            print(f"  {bar} {lead}{styled}{gap} {bar}")
    print(f"  {edge}╰{'─' * (inner + 2)}╯{RESET}", flush=True)


# A word of a changelog line: its pieces, each in a `code` span or not ("(`ci_runner`)" is three).
Word = list[tuple[str, bool]]


def _code_words(text: str) -> list[Word]:
    """The words of a line, backticks gone, each piece marked when it sat between them."""
    words: list[Word] = [[]]
    for index, part in enumerate(text.split("`")):
        is_code = index % 2 == 1
        chunks = part.split(" ")
        for position, chunk in enumerate(chunks):
            if position > 0:
                words.append([])  # a space ends the word
            if chunk:
                words[-1].append((chunk, is_code))
    return [word for word in words if word]


def _visible(word: Word) -> str:
    return "".join(piece for piece, _ in word)


def _wrap_words(words: list[Word], width: int) -> list[list[Word]]:
    """Greedy wrapping on the visible length; a word longer than the width gets its own line."""
    lines: list[list[Word]] = [[]]
    length = 0
    for word in words:
        size = len(_visible(word))
        needed = size + (1 if lines[-1] else 0)
        if lines[-1] and length + needed > width:
            lines.append([])
            length, needed = 0, size
        lines[-1].append(word)
        length += needed
    return lines
