#!/usr/bin/env python3
"""One status line for every folder, in ion-repo's colors (stone and fire).

The style is chosen per machine (`ion repo set statusline=…`, read in `~/.config/kiln/config.toml`):
- `plain` (default): three lines, repo, session (model, gauges, duration), then the tasks
  and the other signals sorted by importance (environment, the machine's RAM and CPU);
- `band`: the same on a soot band, important signals as solid pills;
- `classic`: one line per labeled domain (REPO, SESSION, TASKS, ENV, the last one with RAM and
  CPU);
- `classic-band`: the same on a band;
- `none` and `custom`: nothing here (`ion repo set` removes or leaves Claude Code's `statusLine`).
The names of before kiln 0.4.0 (`sobre`, `bandeau`, `classique`, `classique-fond`, `aucune`,
`perso`) are still read. `--style <name>` forces a style; `--preview` draws it for a sample
session, without colors, `--width` columns wide (64 by default): what a choice shows.

The palette, stone and fire by default, is chosen the same way (`ion repo set
statusline_palette=…`, twenty-eight palettes: one of a single hue each, `red`, `blue`…, the
terminal themes, and `chat`: the colors of the person and of Claude in the chat, after the theme;
`rose` of before ion-repo 0.4.14 is read as `pink`); `--palette <name>` forces one. Each
comes dark or light after Claude Code's theme (`/theme`), with color-blind safe levels under its
`-daltonized` themes; `--theme dark|light|dark-daltonized|light-daltonized` forces it.
`--levels` prints each palette's four levels (all well, to watch, to handle, urgent) as JSON, to
offer a palette by its colors rather than its name. `--help` lists the options.

Colors tell importance: gray when all is well, then glow (to watch), fire (to handle), ember
(urgent). In a repo: branch, git state, CI, prod, tasks, containers, each shown only when the
repo uses it; outside a repo (~/code): an overview of the repos below. Slow sources are read
from a cache and refreshed in the background.
"""

import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import math
import os
import re
import shlex
import struct
import subprocess
import sys
import termios
import time
import tomllib
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass, field

CACHE = os.path.expanduser("~/.cache/claude-statusline")
STYLES = ("plain", "band", "classic", "classic-band")
SILENT_STYLES = ("none", "custom")
DEFAULT_STYLE = "plain"
# names of before kiln 0.4.0, still found in the machine settings
LEGACY_STYLES = {
    "sobre": "plain",
    "bandeau": "band",
    "classique": "classic",
    "classique-fond": "classic-band",
    "aucune": "none",
    "perso": "custom",
}
TIMES = "\u00d7"  # multiplication sign, between a name and a count (wt, br)
INTEGRATION = ("main", "master", "develop")
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
FALLBACK_COLUMNS = 160  # width assumed when the terminal's is unknown
CLAUDE_MARGIN = 4  # columns Claude Code keeps around the status line

# Palettes (`ion repo set statusline_palette=…`), each in the roles of ion-repo's stone and fire
# (src/ion_repo/ui.py, copied: the script runs without ion-repo), for a dark terminal then a light
# one: strong, mid and faint grays, the repo's pill, then the levels to watch (glow), to handle
# (fire) and urgent (ember), the main text, the band.
Palette = tuple[tuple[int, int, int], ...]
PALETTES: dict[str, dict[str, Palette]] = {
    "stone-fire": {
        "dark": (
            (185, 185, 180),
            (140, 140, 135),
            (95, 95, 92),
            (180, 75, 35),
            (255, 225, 120),
            (247, 150, 40),
            (205, 50, 35),
            (255, 255, 255),
            (25, 25, 25),
        ),
        "light": (
            (70, 70, 66),
            (105, 105, 100),
            (150, 150, 145),
            (170, 65, 30),
            (175, 120, 0),
            (215, 110, 10),
            (190, 35, 25),
            (20, 20, 20),
            (238, 236, 230),
        ),
    },
    "solarized": {
        "dark": (
            (147, 161, 161),
            (131, 148, 150),
            (88, 110, 117),
            (38, 139, 210),
            (181, 137, 0),
            (203, 75, 22),
            (220, 50, 47),
            (253, 246, 227),
            (0, 43, 54),
        ),
        "light": (
            (88, 110, 117),
            (101, 123, 131),
            (147, 161, 161),
            (38, 139, 210),
            (181, 137, 0),
            (203, 75, 22),
            (220, 50, 47),
            (0, 43, 54),
            (238, 232, 213),
        ),
    },
    "nord": {
        "dark": (
            (216, 222, 233),
            (150, 160, 178),
            (76, 86, 106),
            (94, 129, 172),
            (235, 203, 139),
            (208, 135, 112),
            (191, 97, 106),
            (236, 239, 244),
            (46, 52, 64),
        ),
        "light": (
            (59, 66, 82),
            (76, 86, 106),
            (150, 160, 178),
            (94, 129, 172),
            (180, 140, 50),
            (200, 110, 80),
            (191, 97, 106),
            (46, 52, 64),
            (229, 233, 240),
        ),
    },
    "dracula": {
        "dark": (
            (248, 248, 242),
            (160, 165, 195),
            (98, 114, 164),
            (189, 147, 249),
            (241, 250, 140),
            (255, 184, 108),
            (255, 85, 85),
            (248, 248, 242),
            (40, 42, 54),
        ),
        "light": (
            (40, 42, 54),
            (85, 90, 120),
            (150, 155, 185),
            (130, 80, 220),
            (160, 140, 0),
            (215, 120, 30),
            (215, 40, 40),
            (30, 30, 40),
            (245, 245, 250),
        ),
    },
    "gruvbox": {
        "dark": (
            (235, 219, 178),
            (168, 153, 132),
            (102, 92, 84),
            (69, 133, 136),
            (250, 189, 47),
            (254, 128, 25),
            (251, 73, 52),
            (251, 241, 199),
            (40, 40, 40),
        ),
        "light": (
            (60, 56, 54),
            (124, 111, 100),
            (168, 153, 132),
            (69, 133, 136),
            (181, 118, 20),
            (175, 58, 3),
            (157, 0, 6),
            (40, 40, 40),
            (251, 241, 199),
        ),
    },
    "catppuccin": {
        "dark": (
            (205, 214, 244),
            (166, 173, 200),
            (108, 112, 134),
            (203, 166, 247),
            (249, 226, 175),
            (250, 179, 135),
            (243, 139, 168),
            (205, 214, 244),
            (30, 30, 46),
        ),
        "light": (
            (76, 79, 105),
            (108, 111, 133),
            (156, 160, 176),
            (136, 57, 239),
            (223, 142, 29),
            (254, 100, 11),
            (210, 15, 57),
            (76, 79, 105),
            (239, 241, 245),
        ),
    },
    "tokyo-night": {
        "dark": (
            (192, 202, 245),
            (154, 165, 206),
            (86, 95, 137),
            (122, 162, 247),
            (224, 175, 104),
            (255, 158, 100),
            (247, 118, 142),
            (220, 225, 252),
            (26, 27, 38),
        ),
        "light": (
            (52, 59, 88),
            (90, 98, 130),
            (150, 155, 180),
            (52, 84, 138),
            (143, 94, 21),
            (150, 80, 40),
            (140, 67, 81),
            (52, 59, 88),
            (225, 226, 231),
        ),
    },
    "forest": {
        "dark": (
            (200, 215, 190),
            (145, 165, 135),
            (90, 105, 85),
            (60, 130, 75),
            (230, 215, 110),
            (225, 145, 60),
            (210, 70, 50),
            (240, 248, 235),
            (20, 30, 22),
        ),
        "light": (
            (40, 60, 40),
            (80, 100, 75),
            (140, 160, 130),
            (45, 115, 60),
            (160, 130, 0),
            (195, 105, 20),
            (185, 45, 30),
            (25, 40, 25),
            (235, 242, 230),
        ),
    },
    "mono": {
        "dark": (
            (200, 200, 200),
            (145, 145, 145),
            (95, 95, 95),
            (80, 80, 80),
            (215, 215, 215),
            (255, 255, 255),
            (220, 50, 47),
            (255, 255, 255),
            (20, 20, 20),
        ),
        "light": (
            (50, 50, 50),
            (100, 100, 100),
            (160, 160, 160),
            (90, 90, 90),
            (70, 70, 70),
            (0, 0, 0),
            (200, 30, 30),
            (0, 0, 0),
            (240, 240, 240),
        ),
    },
    "one-dark": {
        "dark": (
            (215, 218, 224),
            (171, 178, 191),
            (92, 99, 112),
            (97, 175, 239),
            (229, 192, 123),
            (209, 154, 102),
            (224, 108, 117),
            (255, 255, 255),
            (40, 44, 52),
        ),
        "light": (
            (56, 58, 66),
            (105, 108, 119),
            (160, 161, 167),
            (64, 120, 242),
            (193, 132, 1),
            (215, 95, 0),
            (228, 86, 73),
            (40, 44, 52),
            (250, 250, 250),
        ),
    },
    "monokai": {
        "dark": (
            (248, 248, 242),
            (166, 162, 140),
            (117, 113, 94),
            (102, 217, 239),
            (230, 219, 116),
            (253, 151, 31),
            (249, 38, 114),
            (248, 248, 242),
            (39, 40, 34),
        ),
        "light": (
            (73, 72, 62),
            (117, 113, 94),
            (166, 162, 140),
            (0, 137, 179),
            (177, 156, 0),
            (217, 119, 6),
            (212, 0, 79),
            (39, 40, 34),
            (250, 250, 248),
        ),
    },
    "everforest": {
        "dark": (
            (211, 198, 170),
            (157, 169, 160),
            (122, 132, 120),
            (167, 192, 128),
            (219, 188, 127),
            (230, 152, 117),
            (230, 126, 128),
            (211, 198, 170),
            (45, 53, 59),
        ),
        "light": (
            (92, 106, 114),
            (130, 145, 129),
            (166, 176, 160),
            (141, 161, 1),
            (223, 160, 0),
            (245, 125, 38),
            (248, 85, 82),
            (92, 106, 114),
            (253, 246, 227),
        ),
    },
    "kanagawa": {
        "dark": (
            (220, 215, 186),
            (166, 166, 156),
            (114, 113, 105),
            (126, 156, 216),
            (230, 195, 132),
            (255, 160, 102),
            (232, 36, 36),
            (220, 215, 186),
            (31, 31, 40),
        ),
        "light": (
            (84, 84, 100),
            (113, 110, 97),
            (160, 156, 172),
            (77, 105, 155),
            (176, 135, 15),
            (204, 109, 0),
            (200, 64, 83),
            (67, 67, 108),
            (242, 236, 188),
        ),
    },
    "rose-pine": {
        "dark": (
            (224, 222, 244),
            (144, 140, 170),
            (110, 106, 134),
            (196, 167, 231),
            (246, 193, 119),
            (234, 154, 151),
            (235, 111, 146),
            (224, 222, 244),
            (25, 23, 36),
        ),
        "light": (
            (87, 82, 121),
            (121, 117, 147),
            (152, 147, 165),
            (144, 122, 169),
            (234, 157, 52),
            (215, 130, 126),
            (180, 99, 122),
            (87, 82, 121),
            (250, 244, 237),
        ),
    },
    "github-dark": {
        "dark": (
            (201, 209, 217),
            (139, 148, 158),
            (110, 118, 129),
            (88, 166, 255),
            (210, 153, 34),
            (219, 109, 40),
            (248, 81, 73),
            (240, 246, 252),
            (13, 17, 23),
        ),
        "light": (
            (31, 35, 40),
            (89, 99, 110),
            (140, 149, 159),
            (9, 105, 218),
            (154, 103, 0),
            (188, 76, 0),
            (207, 34, 46),
            (31, 35, 40),
            (255, 255, 255),
        ),
    },
    "ayu": {
        "dark": (
            (191, 189, 182),
            (172, 182, 191),
            (86, 91, 102),
            (89, 194, 255),
            (230, 180, 80),
            (255, 143, 64),
            (240, 113, 120),
            (230, 225, 207),
            (11, 14, 20),
        ),
        "light": (
            (92, 97, 102),
            (120, 123, 128),
            (171, 176, 182),
            (57, 158, 230),
            (235, 164, 0),
            (250, 141, 62),
            (240, 113, 113),
            (92, 97, 102),
            (252, 252, 252),
        ),
    },
    "material": {
        "dark": (
            (238, 255, 255),
            (176, 190, 197),
            (84, 110, 122),
            (130, 170, 255),
            (255, 203, 107),
            (247, 140, 108),
            (255, 83, 112),
            (238, 255, 255),
            (38, 50, 56),
        ),
        "light": (
            (84, 110, 122),
            (144, 164, 174),
            (176, 190, 197),
            (97, 130, 184),
            (246, 164, 52),
            (247, 109, 71),
            (229, 57, 53),
            (38, 50, 56),
            (250, 250, 250),
        ),
    },
    "slate": {
        "dark": (
            (226, 232, 240),
            (148, 163, 184),
            (71, 85, 105),
            (56, 189, 248),
            (251, 191, 36),
            (251, 146, 60),
            (248, 113, 113),
            (248, 250, 252),
            (15, 23, 42),
        ),
        "light": (
            (51, 65, 85),
            (100, 116, 139),
            (148, 163, 184),
            (2, 132, 199),
            (217, 119, 6),
            (234, 88, 12),
            (220, 38, 38),
            (15, 23, 42),
            (241, 245, 249),
        ),
    },
    "zenburn": {
        "dark": (
            (220, 220, 204),
            (159, 175, 175),
            (112, 144, 128),
            (140, 208, 211),
            (240, 223, 175),
            (223, 175, 143),
            (204, 147, 147),
            (255, 255, 239),
            (63, 63, 63),
        ),
        "light": (
            (63, 63, 63),
            (95, 95, 95),
            (159, 159, 159),
            (54, 96, 96),
            (154, 125, 0),
            (176, 95, 47),
            (160, 60, 60),
            (47, 47, 47),
            (240, 239, 229),
        ),
    },
}
DEFAULT_PALETTE = "stone-fire"
LEGACY_PALETTES = {"rose": "pink"}  # before ion-repo 0.4.14


def oklch(lightness: float, chroma: float, hue: float) -> tuple[int, int, int]:
    """An OKLCH color (Björn Ottosson's OKLab, in polar form) in sRGB; its chroma lowered until
    it fits, so a hue keeps its lightness, the one thing that tells two levels apart."""
    angle = math.radians(hue)
    for step in range(101):
        c = chroma * (1 - step / 100)
        a, b = c * math.cos(angle), c * math.sin(angle)
        long_ = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
        medium = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
        short = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
        linear = (
            4.0767416621 * long_ - 3.3077115913 * medium + 0.2309699292 * short,
            -1.2684380046 * long_ + 2.6097574011 * medium - 0.3413193965 * short,
            -0.0041960863 * long_ - 0.7034186147 * medium + 1.7076147010 * short,
        )
        if all(-1e-4 <= part <= 1 + 1e-4 for part in linear):
            break
    return tuple(  # type: ignore[return-value]
        round(255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055))
        for x in (min(max(part, 0.0), 1.0) for part in linear)
    )


# Palettes of one hue (`red`, `blue`…): a gray barely tinted with it for all well, then the hue
# from the least to the most striking: on a dark terminal, dim and muted to watch, then lighter
# and fuller up to urgent, the brightest (as GitHub's dark contribution graph); on a light one,
# deeper up to urgent. The levels apart by their lightness in OKLCH, so they stay told apart though
# they share a hue. Per shade, (lightness, chroma) of strong, mid and faint grays, pill, glow,
# fire, ember, text, band, as in PALETTES.
HUES = {
    "red": 25,
    "orange": 55,
    "yellow": 95,
    "green": 145,
    "teal": 190,
    "blue": 255,
    "violet": 300,
    "pink": 350,
}
HUE_RAMP = {
    "dark": (
        (0.88, 0.012),
        (0.72, 0.012),
        (0.48, 0.012),
        (0.55, 0.14),
        (0.62, 0.09),
        (0.73, 0.16),
        (0.84, 0.30),
        (0.98, 0.005),
        (0.20, 0.02),
    ),
    "light": (
        (0.35, 0.012),
        (0.50, 0.012),
        (0.72, 0.012),
        (0.50, 0.14),
        (0.70, 0.13),
        (0.57, 0.17),
        (0.44, 0.19),
        (0.20, 0.01),
        (0.96, 0.012),
    ),
}
PALETTES.update(
    {
        name: {
            shade: tuple(oklch(lightness, chroma, hue) for lightness, chroma in ramp)
            for shade, ramp in HUE_RAMP.items()
        }
        for name, hue in HUES.items()
    }
)


def machine_settings() -> dict:
    """ion-repo's machine settings (`~/.config/ion-repo/config.toml`, `kiln/` before ion-repo
    0.4.14), empty when unreadable."""
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    path = os.path.join(base, "ion-repo", "config.toml")
    if not os.path.exists(path):
        path = os.path.join(base, "kiln", "config.toml")
    try:
        with open(path, "rb") as file:
            return tomllib.load(file)
    except OSError, tomllib.TOMLDecodeError:
        return {}


def chosen_palette(settings: dict) -> str:
    """`--palette <name>`, else the `statusline_palette` key of the machine settings."""
    name = ARGS.palette or str(settings.get("statusline_palette", DEFAULT_PALETTE))
    name = LEGACY_PALETTES.get(name, name)
    return name if name in PALETTES or name == CHAT_PALETTE else DEFAULT_PALETTE


# Levels for color-blind eyes (Okabe-Ito, safe for every common color blindness): sky blue to
# watch, orange to handle, vermilion urgent, on a blue pill; taken by Claude Code's `-daltonized`
# themes, in place of the palette's glow, fire, ember and brick.
DALTONIZED = {
    "dark": ((0, 114, 178), (86, 180, 233), (230, 159, 0), (213, 94, 0)),
    "light": ((0, 114, 178), (0, 114, 178), (190, 120, 0), (200, 70, 0)),
}


CHAT_PALETTE = "chat"
# Claude Code's own colors for the person (`professionalBlue`) and for Claude (`claude`), by
# theme; a custom theme's overrides (`/repo:color`) replace them.
CHAT_DEFAULTS = {
    "professionalBlue": (106, 155, 204),
    "claude": (215, 119, 87),
}
CHAT_DEFAULTS_DALTONIZED = {"claude": (255, 153, 51)}


def json_file(path: str) -> dict:
    try:
        with open(os.path.expanduser(path), "rb") as file:
            loaded = json.load(file)
    except OSError, ValueError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def theme_setting() -> str:
    """Claude Code's `/theme`: `theme` in `~/.claude/settings.json`, else in `~/.claude.json`."""
    for path in ("~/.claude/settings.json", "~/.claude.json"):
        theme = json_file(path).get("theme")
        if isinstance(theme, str) and theme:
            return theme
    return ""


def custom_theme(theme: str) -> dict:
    """The file of a `custom:<slug>` theme (`~/.claude/themes/<slug>.json`), empty otherwise."""
    if not theme.startswith("custom:"):
        return {}
    return json_file(f"~/.claude/themes/{theme.removeprefix('custom:')}.json")


def claude_theme() -> str:
    """`--theme <name>`, else Claude Code's theme (`/theme`: `light`, `light-daltonized`,
    `dark-ansi`…, a custom theme by its `base`), else `COLORFGBG` set by some terminals; dark
    otherwise."""
    if ARGS.theme:
        return ARGS.theme
    theme = theme_setting()
    if theme.startswith("custom:"):
        theme = str(custom_theme(theme).get("base") or "")
    if theme.startswith(("light", "dark")):
        return theme
    background = os.environ.get("COLORFGBG", "").rpartition(";")[2]
    return "light" if background in ("7", "15") else "dark"


def rgb(value: object) -> tuple[int, int, int] | None:
    """A theme color written `#rrggbb` or `rgb(r,g,b)`; None for any other form (`ansi:…`)."""
    text = str(value).strip().lower()
    if re.fullmatch(r"#[0-9a-f]{6}", text):
        return (int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16))
    found = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", text)
    if found:
        red, green, blue = (min(int(part), 255) for part in found.groups())
        return (red, green, blue)
    return None


def chat_palette(theme: str, overrides: dict) -> dict[str, Palette]:
    """The `chat` palette: the chat's colors in the roles of stone and fire, the person's color
    on the repo's pill and to watch, Claude's to handle; grays, red, text and band kept."""
    colors = dict(CHAT_DEFAULTS)
    if "daltonized" in theme:
        colors.update(CHAT_DEFAULTS_DALTONIZED)
    for key in colors:
        chosen = rgb(overrides.get(key))
        if chosen is not None:
            colors[key] = chosen
    person, claude = colors["professionalBlue"], colors["claude"]
    palettes = {}
    for shade, base in PALETTES[DEFAULT_PALETTE].items():
        light, mid, faint, _, _, _, red, text, band = base
        palettes[shade] = (light, mid, faint, person, person, claude, red, text, band)
    return palettes


PREVIEW_COLUMNS = 64  # width of a `--preview`: a choice's box, beside the list of options


def options_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ion-repo's status line: reads Claude Code's session on stdin, prints the "
        "line. Without an option, the style and palette of `ion repo set`.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--style",
        choices=(*STYLES, *SILENT_STYLES, *LEGACY_STYLES),
        help="this style rather than the machine's",
    )
    parser.add_argument(
        "--palette",
        choices=(*PALETTES, CHAT_PALETTE),
        metavar="PALETTE",
        help="this palette rather than the machine's (one of `--levels`)",
    )
    parser.add_argument(
        "--theme",
        metavar="THEME",
        help="this Claude Code theme rather than `/theme`'s (dark, light, dark-daltonized…)",
    )
    parser.add_argument(
        "--levels",
        action="store_true",
        help="print each palette's four levels (all well, to watch, to handle, urgent) as JSON",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="the line of a sample session, without colors nor stdin, "
        f"{PREVIEW_COLUMNS} columns wide: what a choice shows",
    )
    parser.add_argument(
        "--width", type=int, metavar="COLUMNS", help="this width rather than the terminal's"
    )
    parser.add_argument("--scan", metavar="ROOT", help=argparse.SUPPRESS)  # background refresh
    return parser


# Read here, as the theme and the palette are; an import (the tests) takes no option.
ARGS = options_parser().parse_args(None if __name__ == "__main__" else [])
SETTINGS = machine_settings()
THEME = claude_theme()
SHADE = "light" if THEME.startswith("light") else "dark"
PALETTE = chosen_palette(SETTINGS)
(
    STONE_LIGHT,
    STONE,
    STONE_DARK,
    BRICK,
    GLOW,
    FIRE,
    EMBER,
    TEXT,
    SOOT,
) = (
    chat_palette(THEME, custom_theme(theme_setting()).get("overrides") or {})
    if PALETTE == CHAT_PALETTE
    else PALETTES[PALETTE]
)[SHADE]
if "daltonized" in THEME and PALETTE != CHAT_PALETTE:
    BRICK, GLOW, FIRE, EMBER = DALTONIZED[SHADE]
# on a pill: the lighter of the text and the band on dark colors, the darker on bright ones
WHITE, INK = sorted((TEXT, SOOT), key=sum, reverse=True)

# states of a backlog ticket, in English (docs/backlog) or French (former docs/a-faire)
STATES = (
    ("in progress", "doing"),
    ("en cours", "doing"),
    ("blocked", "blocked"),
    ("bloqué", "blocked"),
    ("to verify", "review"),
    ("à vérifier", "review"),
)

# all well, to watch, to handle, urgent
LEVEL_COLORS = {0: STONE, 1: GLOW, 2: FIRE, 3: EMBER}
LEVEL_NAMES = ("all well", "to watch", "to handle", "urgent")


def palette_levels(name: str) -> dict[str, str]:
    """A palette's four levels, `#rrggbb`, in Claude Code's theme: what a person choosing it
    needs to see, rather than its name."""
    palettes = (
        chat_palette(THEME, custom_theme(theme_setting()).get("overrides") or {})
        if name == CHAT_PALETTE
        else PALETTES[name]
    )
    _, stone, _, _, glow, fire, ember, _, _ = palettes[SHADE]
    if "daltonized" in THEME and name != CHAT_PALETTE:
        _, glow, fire, ember = DALTONIZED[SHADE]
    return {
        level: "#{:02x}{:02x}{:02x}".format(*color)
        for level, color in zip(LEVEL_NAMES, (stone, glow, fire, ember), strict=True)
    }


BOLD, ITALIC, RESET, NORMAL = "\033[1m", "\033[3m", "\033[0m", "\033[22;23m"


def read(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()


def sh(*cmd: str, cwd: str | None = None, timeout: float = 2) -> str:
    try:
        # never a lock on the index: an interrupted git would leave it behind
        if cmd[:1] == ("git",):
            cmd = ("git", "--no-optional-locks", *cmd[1:])
        return subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        ).stdout.strip()
    except Exception:
        return ""


def cached(name: str, ttl: float, cmd: str, cwd: str) -> str:
    """The last known value; reruns `cmd` (in `cwd`) in the background when older than `ttl` s.

    A failing command does not replace the last known value.
    """
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    try:
        age, val = time.time() - os.path.getmtime(path), read(path).strip()
    except OSError:
        age, val = 1e9, ""
    lock = path + ".lock"
    if age > ttl and not (os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 60):
        with open(lock, "w"):
            pass
        q = shlex.quote
        tmp = q(path + ".tmp")
        script = (
            f"cd {q(cwd)} && ({cmd}) > {tmp} 2>/dev/null && mv {tmp} {q(path)};"
            f" rm -f {tmp} {q(lock)}; touch {q(path)}"
        )
        subprocess.Popen(
            ["bash", "-c", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    return val


def git_state(path: str) -> dict[str, str | int]:
    ab = sh("git", "-C", path, "rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    return {
        "name": os.path.basename(path).lstrip("."),
        "branch": sh("git", "-C", path, "branch", "--show-current"),
        "dirty": len(sh("git", "-C", path, "status", "--porcelain").splitlines()),
        "ahead": int(ab[0]) if len(ab) == 2 else 0,
        "behind": int(ab[1]) if len(ab) == 2 else 0,
        "wt": sh("git", "-C", path, "worktree", "list").count("\n"),
    }


def scan(root: str) -> None:
    """Prints the git state of each repo under `root`, down to three folders (a family folder with
    one folder per tool), except `_*` folders and node_modules."""
    found = []
    for dirpath, dirs, files in os.walk(root):
        if (".git" in dirs or ".git" in files) and dirpath != root:
            found.append(dirpath)
            dirs.clear()
            continue
        depth = dirpath[len(root) :].count(os.sep)
        dirs[:] = [x for x in dirs if not x.startswith("_") and x != "node_modules" and depth < 3]
    found.sort(key=lambda p: os.path.basename(p).lstrip(".").lower())
    print(json.dumps([git_state(p) for p in found]))


# ---------------------------------------------------------------------------- display model


@dataclass
class Item:
    """A displayed item. `short`: its compact form when room runs out (None: none, "": it
    disappears). `role`: `title` (repo name), `strong` (model), `muted` (commit)."""

    text: str
    level: int = 0
    short: str | None = None
    role: str = ""
    gauge: float | None = None  # percentage: the item is drawn as a gauge
    amount: str = ""  # shown instead of the gauge's percentage (the context, in tokens)
    reset: str = ""  # a quota's reset, shown when it gets tight
    compact: bool = False

    @property
    def shown(self) -> str:
        return self.short if self.compact and self.short is not None else self.text

    def can_compact(self) -> bool:
        return not self.compact and (self.short is not None or self.gauge is not None)


Group = list[Item]


@dataclass
class Status:
    repo: list[Group] = field(default_factory=list)
    commit: str = ""
    session: list[Group] = field(default_factory=list)  # model, gauges
    usage: list[Group] = field(default_factory=list)  # cache, duration, lines
    tasks: list[Group] = field(default_factory=list)
    env: list[Group] = field(default_factory=list)
    machine: list[Group] = field(default_factory=list)  # the machine's RAM, CPU


def level_of(group: Group) -> int:
    return max((item.level for item in group), default=0)


def quota_level(pct: float) -> int:
    return 3 if pct >= 90 else 2 if pct >= 80 else 1 if pct >= 60 else 0


# Every message re-reads the whole context: past these sizes, a message costs about two, four and
# six times a fresh session's (some 50k tokens of instructions and tools).
CONTEXT_LEVELS = (100_000, 200_000, 300_000)


def context_level(tokens: int) -> int:
    return sum(tokens >= limit for limit in CONTEXT_LEVELS)


def window_tokens(raw: object) -> int:
    """A window as Claude Code writes it (`400000`, `400k`, `1M`); 0 for anything else (`auto`)."""
    text = str(raw or "").strip().lower()
    scale = {"k": 1_000, "m": 1_000_000}.get(text[-1:], 1)
    try:
        return int(float(text.rstrip("km")) * scale)
    except ValueError:
        return 0


def compaction_point(window: int, project: str, model: str) -> int:
    """Where Claude Code compacts: `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, otherwise `autoCompactWindow`
    (ion-repo's `compact_window`), the local settings over the project's over the user's, in each
    the model's own (saved by `/autocompact`) first; otherwise the whole window. A launch's
    `--autocompact` is not seen."""
    point = window_tokens(os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW"))
    names = ("settings.local.json", "settings.json") if project else ()
    files = [os.path.join(project, ".claude", name) for name in names]
    for path in [*files, os.path.expanduser("~/.claude/settings.json")]:
        if point:
            break
        try:
            settings = json.loads(read(path))
        except OSError, ValueError:
            continue
        if isinstance(settings, dict):
            own = ((settings.get("modelSettings") or {}).get(model) or {}).get("autoCompactWindow")
            point = window_tokens(own or settings.get("autoCompactWindow"))
    return min(point, window) if point and window else point or window


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'s' if n > 1 else ''}"


# ---------------------------------------------------------------------------- collection


def opt(main: str, key: str) -> str:
    """A repo setting, set by `git config statusline.<key> …` (`ci false`, `prod-url …`)."""
    return sh("git", "-C", main, "config", "--get", f"statusline.{key}")


def tracked_secrets(top: str) -> list[str]:
    """Secrets tracked by git: .env (except examples, even rendered by a template:
    `.example.jinja`), tokens, private keys."""
    return [
        f
        for f in sh("git", "-C", top, "ls-files").splitlines()
        if (
            re.search(r"(^|/)\.env(\.[^/]+)*$", f)
            and not re.search(r"\.(example|sample|template|dist)(\.|$)", f)
        )
        or re.search(r"(^|/)\.[\w-]+/token$|\.(pem|key|p12)$|(^|/)id_(rsa|ed25519)$", f)
    ]


def unmerged_branches(cwd: str, integ: str) -> int:
    """Local branches not yet in origin/<integration>, the integration branch itself excluded
    (a `develop` ahead of origin is not a branch to merge)."""
    names = sh(
        "git", "-C", cwd, "branch", "--no-merged", f"origin/{integ}", "--format=%(refname:short)"
    ).splitlines()
    return sum(1 for n in names if n and n != integ)


def backlog_items(top: str) -> Group:
    """Tickets of docs/backlog/backlog.md (`### <repo>#T-NN ·`, or `### T-NN ·` not yet converted),
    or else of the former
    docs/a-faire/a-faire.md (`### AF-NN ·`, French fields): those before the "Done" ("Fait")
    section, critical ones included (🔴 section); or else the former `N. **Title**` format;
    then the boxes of urgent.md, what only the user can do."""
    tasks: Group = []
    folder = "docs/backlog" if os.path.isdir(os.path.join(top, "docs/backlog")) else "docs/a-faire"
    tracker = "backlog.md" if folder == "docs/backlog" else "a-faire.md"
    try:
        lines = read(os.path.join(top, folder, tracker)).splitlines()
        entries, critical, section, states = 0, 0, "", {}
        for line in lines:
            if line.startswith("## "):
                section = line
                if "Done" in line or "Fait" in line:
                    break
            elif re.match(r"### (?:[a-z][a-z0-9-]*#)?[A-Z]+-\d+ ·", line):
                entries += 1
                critical += "🔴" in section
            elif match := re.match(r"- \*\*(?:Status\*\*:|État\*\* :) (.*)", line):
                for prefix, state in STATES:
                    if match[1].startswith(prefix):
                        states[state] = states.get(state, 0) + 1
        if not entries:
            entries = sum(
                1
                for line in lines
                if re.match(r"\s*\d+\.\s+\*\*", line)
                and "Fait" not in line
                and "fait le" not in line.lower()
            )
        tasks.append(Item(f"{entries} tasks"))
        if critical:
            tasks.append(Item(f"crit{TIMES}{critical}", 2))
        for state in ("doing", "blocked", "review"):
            if states.get(state):
                tasks.append(Item(f"{state}{TIMES}{states[state]}", short=""))
    except OSError:
        pass
    try:
        urgent = sum(
            1
            for line in read(os.path.join(top, folder, "urgent.md")).splitlines()
            if line.lstrip().startswith("- [ ]")
        )
        if urgent:
            tasks.insert(1 if tasks else 0, Item(f"urgent{TIMES}{urgent}", 3))
    except OSError:
        pass
    return tasks


def collect_repo(status: Status, cwd: str, top: str) -> str:
    main = (
        sh("git", "-C", cwd, "worktree", "list", "--porcelain")
        .split("\n", 1)[0]
        .removeprefix("worktree ")
    )
    key = hashlib.sha1(main.encode()).hexdigest()[:12]
    name = os.path.basename(main).lstrip(".")
    integ = (
        "develop"
        if sh("git", "-C", cwd, "rev-parse", "-q", "--verify", "origin/develop")
        else sh(
            "git", "-C", cwd, "symbolic-ref", "--short", "refs/remotes/origin/HEAD"
        ).removeprefix("origin/")
        or "main"
    )

    # repo: name, worktree, branch, files, ahead/behind, operation in progress, stashes
    st = sh("git", "-C", cwd, "status", "--porcelain=v2", "--branch").splitlines()
    branch = next((line.split()[2] for line in st if line.startswith("# branch.head ")), "")
    branch = "" if branch == "(detached)" else branch
    files = [line for line in st if not line.startswith("#")]
    add = sum(1 for line in files if line[:1] in "12" and line[2:3] != ".")
    mod = sum(1 for line in files if line[:1] in "12u" and line[3:4] != ".")
    unt = sum(1 for line in files if line.startswith("?"))
    # on the integration branch with changes: risk of a direct commit
    branch_level = 1 if not branch else 2 if branch == integ and (add or mod or unt) else 0
    head = [Item(name, role="title")]
    if top != main:
        head.append(Item(f"wt:{os.path.basename(top)}"))
    head.append(Item(f"⎇ {branch or 'detached'}", branch_level))
    status.repo.append(head)
    changes = [Item(f"{s}{n}", 1) for s, n in (("+", add), ("~", mod), ("?", unt)) if n]
    if changes:
        status.repo.append(changes)
    gitdir = sh("git", "-C", cwd, "rev-parse", "--absolute-git-dir")
    for marker, label in (
        ("rebase-merge", "REBASE"),
        ("rebase-apply", "REBASE"),
        ("MERGE_HEAD", "MERGE"),
        ("CHERRY_PICK_HEAD", "CHERRY-PICK"),
        ("REVERT_HEAD", "REVERT"),
        ("BISECT_LOG", "BISECT"),
    ):
        if os.path.exists(os.path.join(gitdir, marker)):
            status.repo.append([Item(label, 3)])
            break
    sync = []
    ab = sh(
        "git", "-C", cwd, "rev-list", "--left-right", "--count", f"HEAD...origin/{integ}"
    ).split()
    if len(ab) == 2 and ab != ["0", "0"]:
        sync.append(Item(f"↑{ab[0]}↓{ab[1]}", 1 if branch == integ and ab[0] != "0" else 0))
    if branch and branch != integ:
        if not any(line.startswith("# branch.upstream ") for line in st):
            sync.append(Item("unpushed", short=""))
        else:
            up_ab = next(
                (line.split()[2:4] for line in st if line.startswith("# branch.ab ")),
                ["+0", "-0"],
            )
            if up_ab[0] != "+0":
                sync.append(Item(f"⇡{up_ab[0][1:]}"))
    if sync:
        status.repo.append(sync)
    trees = []
    wt = sh("git", "-C", cwd, "worktree", "list").count("\n")
    if wt:
        trees.append(Item(f"wt{TIMES}{wt}"))
    unmerged = unmerged_branches(cwd, integ)
    if unmerged:
        trees.append(Item(f"br{TIMES}{unmerged}"))
    stash = len(sh("git", "-C", cwd, "stash", "list").splitlines())
    if stash:
        trees.append(Item(f"stash{TIMES}{stash}"))
    if trees:
        status.repo.append(trees)
    status.commit = sh("git", "-C", cwd, "log", "-1", "--no-merges", "--format=%s")

    tasks = backlog_items(top)
    if tasks:
        status.tasks.append(tasks)

    secrets = tracked_secrets(top)
    if secrets:
        more = f" +{len(secrets) - 1}" if len(secrets) > 1 else ""
        status.env.append(
            [Item(f"secret tracked: {secrets[0]}{more}", 3, f"secret{TIMES}{len(secrets)}")]
        )

    # prod: back and front, each with the commits that touch it and are not deployed yet (a
    # docs change does not count). Back: the health probe (`statusline.prod-url`) gives the
    # deployed commit; front: the latest Vercel deployment.
    def deployed(name: str, sha: str, paths: Iterable[str]) -> Item:
        late = ""
        if sha:
            late = sh(
                "git",
                "-C",
                main,
                "rev-list",
                "--count",
                f"{sha}..origin/{integ}",
                "--",
                *[p for p in paths if os.path.exists(os.path.join(main, p))],
            )
        if not late:
            return Item(f"{name} ?", 1)
        if late == "0":
            return Item(f"{name} ✓")
        return Item(f"{name} ↓{late}", 2 if int(late) > 50 else 1, f"↓{late}")

    def framework(folder: str, markers: Iterable[tuple[str, str]], fallback: str) -> str:
        """A folder's framework, recognized by a file of its own."""
        return next(
            (n for f, n in markers if os.path.exists(os.path.join(main, folder, f))), fallback
        )

    prod: Group = []
    prod_url = opt(main, "prod-url")
    if prod_url:
        try:
            health = json.loads(
                cached(f"{key}-health", 120, f"curl -s4 -m 5 {shlex.quote(prod_url)}", main) or "{}"
            )
        except ValueError:
            health = {}
        back = framework("backend", (("manage.py", "django"), ("main.py", "fastapi")), "back")
        prod.append(deployed(back, health.get("version", ""), ("backend", "config")))
        if health and health.get("status") != "ok":
            down = [k for k, ok in (health.get("checks") or {}).items() if not ok]
            prod.append(Item(" ".join([str(health.get("status", "?")), *down]), 3))
    try:
        vp = json.loads(read(os.path.join(main, ".vercel", "project.json")))
        scope = f"--scope {vp['orgId']}"
        paused = cached(
            f"{key}-vercel",
            300,
            f"vercel api /v9/projects/{vp['projectId']} {scope}"
            " | python3 -c 'import json,sys; print(json.load(sys.stdin).get(\"paused\", False))'",
            main,
        )
        front_sha = cached(
            f"{key}-front",
            300,
            f"vercel api '/v6/deployments?projectId={vp['projectId']}"
            f"&target=production&state=READY&limit=1' {scope} | python3 -c 'import json,sys;"
            ' m = json.load(sys.stdin)["deployments"][0]["meta"];'
            # Git integration: githubCommitSha; `vercel deploy` from the CLI: gitCommitSha.
            ' print(m.get("githubCommitSha") or m.get("gitCommitSha", ""))\'',
            main,
        )
        front = framework(
            "frontend",
            (
                ("nuxt.config.ts", "nuxt"),
                ("next.config.js", "next"),
                ("next.config.ts", "next"),
                ("svelte.config.js", "svelte"),
                ("vite.config.ts", "vue"),
            ),
            "front",
        )
        prod.append(deployed(front, front_sha, ("frontend",)))
        if paused == "True":
            prod.append(Item("paused", 2))
    except OSError, ValueError, KeyError:
        pass
    if prod:
        status.env.append([Item("prod"), *prod])

    # CI of the integration branch: replayed on the machine by `ion repo ci` (`statusline.ci
    # locale`, verdict in the git note refs/notes/ci, ⏳ while its worktree exists), else GitHub
    # (unless `statusline.ci false`)
    if opt(main, "ci") == "locale":
        sha = sh("git", "-C", main, "rev-parse", "-q", "--verify", f"origin/{integ}")
        note = (
            sh("git", "-C", main, "notes", "--ref=ci", "show", sha).split("\n", 1)[0] if sha else ""
        )
        running = sha and os.path.isdir(
            os.path.expanduser(f"~/.cache/kiln/ci/{os.path.basename(main)}-{sha[:12]}")
        )
        if running:
            status.env.append([Item("CI ⏳")])
        else:
            status.env.append(
                [
                    {
                        "kiln ci: success": Item("CI ✓"),
                        "kiln ci: failure": Item("CI ✗", 3),
                        # Notes written by kiln 0.3.
                        "kiln ci : succès": Item("CI ✓"),
                        "kiln ci : échec": Item("CI ✗", 3),
                    }.get(note, Item("CI rerun needed", 1, "CI rerun"))
                ]
            )
    elif os.path.isdir(os.path.join(main, ".github", "workflows")) and opt(main, "ci") != "false":
        ci = cached(
            f"{key}-ci",
            60,
            f"gh run list -b {integ} -L 1 --json status,conclusion"
            " -q '.[0] | .conclusion // .status'",
            main,
        )
        status.env.append(
            [
                {
                    "success": Item("CI ✓"),
                    "failure": Item("CI ✗", 3),
                    "cancelled": Item("CI ⊘", 1),
                }.get(ci, Item("CI ⏳" if ci else "CI ?"))
            ]
        )

    # TODO/FIXME/XXX markers in comments
    todos = cached(
        f"{key}-todo2",
        300,
        "git grep -I -c -E '(#|//|/\\*|<!--)\\s*(TODO|FIXME|XXX)\\b' -- . ':!docs/_archive'"
        " | awk -F: '{s+=$NF} END{print s+0}'",
        main,
    )
    if todos and todos != "0":
        status.env.append([Item(f"TODO{TIMES}{todos}")])

    # dependencies to update (uv, pnpm), checked once a day in the background
    deps = []
    for folder in ("", "backend", "frontend"):
        path = os.path.join(main, folder)
        tag = hashlib.sha1(path.encode()).hexdigest()[:8]
        if os.path.exists(os.path.join(path, "uv.lock")):
            n = cached(
                f"{key}-{tag}-uv",
                86400,
                "uv tree --outdated --depth 1 --frozen | grep -c 'latest:'",
                path,
            )
            if n and n != "0":
                deps.append(Item(f"uv{TIMES}{n}"))
        if os.path.exists(os.path.join(path, "pnpm-lock.yaml")):
            n = cached(
                f"{key}-{tag}-pnpm",
                86400,
                "pnpm outdated --format json"
                " | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'",
                path,
            )
            if n and n != "0":
                deps.append(Item(f"pnpm{TIMES}{n}"))
    if deps:
        status.env.append(deps)

    # dev servers: listening ports opened by a process started from this repo
    ports = set()
    for line in sh("ss", "-ltnpH").splitlines():
        m = re.search(r":(\d+)\s.*pid=(\d+)", line)
        if not m:
            continue
        try:
            here = os.readlink(f"/proc/{m.group(2)}/cwd")
        except OSError:
            continue
        if here == main or here.startswith(main + "/"):
            ports.add(int(m.group(1)))
    if ports:
        status.env.append([Item(" ".join(f":{p}" for p in sorted(ports)))])

    # podman containers named <repo>-…: running out of total
    pods = cached("podman", 30, "podman ps -a --format '{{.Names}} {{.State}}'", main)
    mine = [
        line.split()
        for line in pods.splitlines()
        if line.startswith(name.lower() + "-") and len(line.split()) == 2
    ]
    if mine:
        up = sum(1 for _, s in mine if s == "running")
        status.env.append([Item(f"podman {up}/{len(mine)}")])
    return main


def collect_overview(status: Status, cwd: str) -> None:
    """Outside a repo: one word per repo below, colored when it has changes or differs from its
    upstream; its branch, when the main tree has left the integration branch."""
    key = hashlib.sha1(cwd.encode()).hexdigest()[:12]
    try:
        repos = json.loads(
            cached(
                f"{key}-repos",
                20,
                f"python3 {shlex.quote(__file__)} --scan {shlex.quote(cwd)}",
                cwd,
            )
            or "[]"
        )
    except ValueError:
        repos = []
    wts = 0
    for r in repos:
        group = [Item(r["name"], 1 if r["dirty"] or r["ahead"] or r["behind"] else 0)]
        if r["branch"] not in INTEGRATION:
            group.append(Item(f"⎇ {r['branch'] or 'detached'}", 2))
        if r["dirty"]:
            group.append(Item(f"~{r['dirty']}", 1))
        if r["ahead"] or r["behind"]:
            group.append(Item(f"↑{r['ahead']}↓{r['behind']}", 1))
        status.repo.append(group)
        wts += int(r["wt"])
    if wts:
        status.env.append([Item(f"wt{TIMES}{wts}")])


def sweep_hint() -> str:
    """With the memory alert, the verdict of `sweep --json` (run in the background, cached):
    what `sweep --kill` would stop, or nothing to kill."""
    sweep = os.path.expanduser("~/.local/bin/sweep")
    if not os.path.exists(sweep):
        return ""
    try:
        report = json.loads(
            cached("sweep", 30, f"{shlex.quote(sweep)} --json", os.path.expanduser("~")) or "null"
        )
        candidates = report["candidates"]
    except ValueError, TypeError, KeyError:
        return " → sweep"  # no verdict yet: the first run is in the background
    certain = [c for c in candidates if c.get("is_certain")]
    if certain:
        size = sum(c.get("rss_bytes", 0) for c in certain) / 2**20
        size_text = f"{size / 1024:.1f} GB" if size >= 1024 else f"{size:.0f} MB"
        return f" → sweep --kill: {len(certain)} safe, {size_text}"
    if candidates:
        return f" → sweep: {len(candidates)} to check"
    return " · nothing to kill"


def collect_session(status: Status, d: dict, main: str) -> None:
    model = d.get("model", {}).get("display_name", "?")
    effort = d.get("effort") or d.get("effort_level") or (d.get("model", {}) or {}).get("effort")
    if isinstance(effort, dict):
        effort = effort.get("level")
    head = [Item(model, role="strong")]
    if effort:
        head.append(Item(str(effort), short=""))
    if d.get("fast_mode"):
        head.append(Item("fast", 1))
    style = (d.get("output_style") or {}).get("name")
    if style and style != "default":
        head.append(Item(f"style {style}", short=""))
    status.session.append(head)

    # the context in tokens, coloured by what a message costs, its gauge full at the compaction;
    # red once the cache has gone cold, the next message writing it all again (Claude Code
    # redraws the line when the cache expires, an hour after the last message with a subscription)
    cw = d.get("context_window") or {}
    context_tokens = sum(
        (cw.get("current_usage") or {}).get(k, 0) or 0
        for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    )
    project = str((d.get("workspace") or {}).get("project_dir") or "")
    model_id = str((d.get("model") or {}).get("id") or "")
    point = compaction_point(int(cw.get("context_window_size") or 0), project, model_id)
    if context_tokens and point:
        fill = min(100.0, 100 * context_tokens / point)
        cold = (d.get("prompt_cache") or {}).get("warm") is False
        level = 3 if cold else context_level(context_tokens)
        amount = f"{context_tokens / 1000:.0f}k"
        status.session.append([Item("ctx", level, gauge=fill, amount=amount)])
    elif cw.get("used_percentage") is not None:
        pct = float(cw["used_percentage"])
        status.session.append([Item("ctx", quota_level(pct), gauge=pct)])

    # subscription limits (5 h window, week), when Claude Code or agy provides them
    has_limits = False
    for k, label in (("five_hour", "5h"), ("seven_day", "wk")):
        limit = (d.get("rate_limits") or {}).get(k) or {}
        if limit.get("used_percentage") is None:
            continue
        has_limits = True
        used = float(limit["used_percentage"])
        when = ""
        if limit.get("resets_at"):
            at = datetime.datetime.fromtimestamp(limit["resets_at"])
            when = f"{at:%H:%M}" if k == "five_hour" else DAYS[at.weekday()]
        status.session.append([Item(label, quota_level(used), gauge=used, reset=when)])

    # machine (Linux, WSL): RAM, always; an alert when it runs short, or when swap is full while
    # RAM fills up (a full swap over free RAM no longer hurts), with sweep's verdict; and the busy
    # cores (one-minute load) out of total
    machine: Group = []
    try:
        meminfo = {
            k: int(v.split()[0])
            for k, v in (line.split(":", 1) for line in read("/proc/meminfo").splitlines())
        }
        ram = 100 * (1 - meminfo["MemAvailable"] / meminfo["MemTotal"])
        swap = (
            100 * (1 - meminfo["SwapFree"] / meminfo["SwapTotal"])
            if meminfo.get("SwapTotal")
            else 0
        )
        if ram >= 90 or (swap >= 80 and ram >= 70):
            text = f"RAM {ram:.0f}% swap {swap:.0f}%{sweep_hint()}"
            machine.append(Item(text, 3, f"RAM {ram:.0f}%"))
        else:
            machine.append(Item(f"RAM {ram:.0f}%", 1 if ram >= 75 else 0))
    except OSError, KeyError, ValueError, ZeroDivisionError:
        pass
    cores = os.cpu_count() or 0
    if cores:
        load = os.getloadavg()[0]
        level = 2 if load >= cores else 1 if load >= 0.8 * cores else 0
        machine.append(Item(f"CPU {load:.1f}/{cores}", level))
    if machine:
        status.machine.append(machine)

    # other Claude sessions (rule: one at a time per project): in a repo, those running in this
    # repo or its worktrees; elsewhere, all of them; and the suspended sessions
    active, stopped = 0, 0
    for pid in sh("pgrep", "-x", "claude").split():
        try:
            here = os.readlink(f"/proc/{pid}/cwd")
            state_letter = read(f"/proc/{pid}/stat").rsplit(")", 1)[1].split()[0]
        except OSError:
            continue
        if main and not (here == main or here.startswith(main + "/")):
            continue
        if state_letter == "T":
            stopped += 1
        else:
            active += 1
    sessions = []
    if active > 1:
        sessions.append(Item(f"+{plural(active - 1, 'session')}", 1, f"+{active - 1}"))
    if stopped:
        sessions.append(Item(f"⏸ {stopped} suspended", short=f"⏸ {stopped}"))
    if sessions:
        status.repo.append(sessions)

    # prompt cache, duration and lines of the session (the cost, only without a subscription)
    pc = d.get("prompt_cache") or {}
    if pc.get("hit_ratio") is not None:
        ratio = 100 * float(pc["hit_ratio"])
        warm = pc.get("warm", True)
        if not warm:  # cold: the context's figure turns red
            status.usage.append([Item("cache cold")])
        elif ratio < 70:  # a healthy cache is not shown
            status.usage.append([Item(f"cache {ratio:.0f}%", 1)])
    c = d.get("cost") or {}
    if c:
        mins = int((c.get("total_duration_ms") or 0) / 60000)
        usage = [Item(f"{mins // 60}h{mins % 60:02d}m" if mins >= 60 else f"{mins}m")]
        if not has_limits:
            usage.append(Item(f"${c.get('total_cost_usd', 0):.2f}"))
        usage.append(
            Item(f"+{c.get('total_lines_added', 0)}/-{c.get('total_lines_removed', 0)}", short="")
        )
        status.usage.append(usage)


# ---------------------------------------------------------------------------- rendering


def fg(color: tuple[int, int, int]) -> str:
    return "\033[38;2;{};{};{}m".format(*color)


def bg(color: tuple[int, int, int]) -> str:
    return "\033[48;2;{};{};{}m".format(*color)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    r, g, bl = (round(x + (y - x) * t) for x, y in zip(a, b, strict=True))
    return r, g, bl


def visible_width(text: str) -> int:
    plain = re.sub(r"\033\[[0-9;]*m", "", text)
    return sum(
        2 if unicodedata.east_asian_width(ch) in "WF" else 0 if unicodedata.combining(ch) else 1
        for ch in plain
    )


# band pills, per level: (background, text)
PILLS = {1: (mix(GLOW, SOOT, 0.78), GLOW), 2: (FIRE, INK), 3: (EMBER, WHITE)}


class Painter:
    """Draws the items: colored text on the terminal's background, or (`band`) on a soot band,
    colored items as solid pills."""

    def __init__(self, band: bool) -> None:
        self.band = band
        self.base = bg(SOOT) if band else ""
        self.sep = self.text(" │ ", STONE_DARK)

    def text(self, t: str, color: tuple[int, int, int], style: str = "") -> str:
        return self.base + fg(color) + style + t + (NORMAL if style else "")

    def pill(self, t: str, back: tuple[int, int, int], front: tuple[int, int, int]) -> str:
        if front in (WHITE, INK):  # pastel palettes: dark letters on a bright pill
            r, g, bl = back
            front = INK if 0.299 * r + 0.587 * g + 0.114 * bl > 150 else WHITE
        return bg(back) + fg(front) + BOLD + f" {t} " + NORMAL + (self.base or RESET)

    def gauge(self, item: Item) -> str:
        pct = item.gauge or 0.0
        out = self.text(item.text + " ", STONE)
        if not item.compact:
            filled = round(pct / 100 * 6)
            out += self.text("▰" * filled, LEVEL_COLORS[item.level] if item.level else STONE_LIGHT)
            out += self.text("▱" * (6 - filled) + " ", STONE_DARK)
        figure = item.amount or f"{pct:.0f}%"
        out += self.text(figure, LEVEL_COLORS[item.level], BOLD if item.level else "")
        if item.reset and item.level and not item.compact:
            out += self.text(f" ↻ {item.reset}", STONE)
        return out

    def item(self, item: Item) -> str:
        if item.gauge is not None:
            return self.gauge(item)
        if item.role == "title":
            return (
                self.pill(item.shown, BRICK, WHITE)
                if self.band
                else self.text(item.shown, TEXT, BOLD)
            )
        if item.role == "strong":
            return self.text(item.shown, STONE_LIGHT, BOLD)
        if item.role == "muted":
            return self.text(item.shown, STONE_DARK, ITALIC)
        if item.level and self.band:
            return self.pill(item.shown, *PILLS[item.level])
        return self.text(item.shown, LEVEL_COLORS[item.level], BOLD if item.level == 3 else "")

    def line(self, groups: list[Group]) -> str:
        parts = [[self.item(i) for i in g if i.shown] for g in groups]
        return self.sep.join(self.text(" ", STONE).join(p) for p in parts if p)


def fit(groups: list[Group], painter: Painter, room: int) -> str:
    """The line, shrunk until it fits in `room` columns: 1) gray items compact, from the last
    group to the first; 2) all-gray groups drop, from the end; 3) colored items compact."""

    def compact(colored: bool) -> bool:
        for g in reversed(groups):
            for item in reversed(g):
                if bool(item.level) == colored and item.can_compact():
                    item.compact = True
                    return True
        return False

    while visible_width(painter.line(groups)) > room:
        if compact(False):
            continue
        if len(groups) > 1 and not level_of(groups[-1]) and groups[-1][0].role != "title":
            groups.pop()
            continue
        if not compact(True):
            break
    return clip(painter.line(groups), room)


def clip(text: str, room: int) -> str:
    """`text` cut to `room` columns, an ellipsis in place of the rest; its color codes all kept,
    so the colors after the cut still end where they did."""
    if visible_width(text) <= room:
        return text
    kept, width, cut = [], 0, False
    for part in re.split(r"(\033\[[0-9;]*m)", text):
        if part.startswith("\033"):
            kept.append(part)
            continue
        for ch in part:
            if cut:
                break
            if width + visible_width(ch) > room - 1:
                kept.append("…")
                cut = True
                break
            kept.append(ch)
            width += visible_width(ch)
    return "".join(kept)


def by_importance(groups: list[Group]) -> list[Group]:
    """Groups from most to least important; the inner order stays (the task total stays ahead
    of its sub-counts)."""
    return sorted(groups, key=lambda g: -level_of(g))


def terminal_columns() -> int:
    """Width of the session's terminal: that of the parent `claude` process (the script has no
    terminal of its own)."""
    pid = os.getppid()
    for _ in range(6):
        try:
            if read(f"/proc/{pid}/comm").strip() == "claude":
                with open(f"/proc/{pid}/fd/0", "rb") as tty:
                    size = fcntl.ioctl(tty, termios.TIOCGWINSZ, b"\0" * 8)
                    return int(struct.unpack("hhhh", size)[1])
            pid = int(read(f"/proc/{pid}/stat").rsplit(")", 1)[1].split()[1])
        except OSError, ValueError, IndexError:
            return 0
    return 0


EMPTY: list[Group] = [[Item("—")]]  # constant height: an empty line keeps its place


def render(status: Status, style: str, columns: int) -> list[str]:
    band = style in ("band", "classic-band")
    painter = Painter(band)
    inner = columns - (2 if band else 0)  # the band keeps one column of margin on each side

    def finish(text: str) -> str:
        if not band:
            return text
        pad = max(0, columns - 1 - visible_width(text))
        return bg(SOOT) + " " + text + bg(SOOT) + " " * pad + RESET

    if style in ("plain", "band"):
        # The tasks keep the head of the line, in every repo; the rest by importance.
        signals = status.tasks + by_importance(status.env + status.machine)
        rows = (status.repo, status.session + status.usage, signals or EMPTY)
        return [finish(fit(row, painter, inner)) for row in rows]

    commit = [[Item(status.commit[:48], role="muted", short="")]] if status.commit else []
    rows = (
        ("REPO", status.repo + commit),
        ("SESSION", status.session + status.usage),
        ("TASKS", status.tasks or EMPTY),
        ("ENV", status.env + status.machine or EMPTY),
    )
    out = []
    for name, groups in rows:
        label = (
            painter.pill(f"{name:<7}", BRICK, WHITE) + painter.text(" ", STONE)
            if band
            else fg(STONE_DARK) + BOLD + f"{name:<9}" + RESET
        )
        out.append(finish(label + fit(groups, painter, inner - visible_width(label))))
    return out


def chosen_style() -> str:
    """`--style <name>`, else the `statusline` key of ion-repo's machine settings."""
    style = ARGS.style or str(SETTINGS.get("statusline", DEFAULT_STYLE))
    return LEGACY_STYLES.get(style, style)


def sample_session() -> dict:
    """A session midway, for `--preview`: each part of the session's line has something to show."""
    now = time.time()
    return {
        "model": {"id": "claude-opus-5-5", "display_name": "Opus 5.5"},
        "effort": {"level": "high"},
        "cost": {"total_cost_usd": 1.84, "total_duration_ms": 47 * 60 * 1000},
        "context_window": {
            "context_window_size": 1_000_000,
            "used_percentage": 23,
            "remaining_percentage": 77,
        },
        "rate_limits": {
            "five_hour": {"used_percentage": 41, "resets_at": now + 2 * 3600},
            "seven_day": {"used_percentage": 18, "resets_at": now + 4 * 86400},
        },
    }


def main() -> None:
    if ARGS.scan:
        scan(ARGS.scan)
        return
    if ARGS.levels:
        print(json.dumps({name: palette_levels(name) for name in (*PALETTES, CHAT_PALETTE)}))
        return
    style = chosen_style()
    if style in SILENT_STYLES:
        return
    if style not in STYLES:
        style = DEFAULT_STYLE
    if ARGS.preview:
        lines = render_session(sample_session(), style, ARGS.width or PREVIEW_COLUMNS)
        print("\n".join(re.sub(r"\x1b\[[0-9;]*m", "", line).rstrip() for line in lines))
        return
    d = json.load(sys.stdin)
    # Antigravity CLI (agy) sends the same format, except its quotas: remaining fraction per
    # window (gemini-5h, gemini-weekly), mapped here to Claude Code's rate_limits.
    if d.get("quota") and not d.get("rate_limits"):
        d["rate_limits"] = {}
        for src, k in (("gemini-5h", "five_hour"), ("gemini-weekly", "seven_day")):
            q = d["quota"].get(src) or {}
            if q.get("remaining_fraction") is not None:
                d["rate_limits"][k] = {
                    "used_percentage": 100 * (1 - float(q["remaining_fraction"])),
                    "resets_at": time.time() + float(q.get("reset_in_seconds") or 0),
                }
    # last input received, to see the fields Claude Code provides
    with (
        contextlib.suppress(OSError),
        open(os.path.join(CACHE, "input.json"), "w", encoding="utf-8") as last_input,
    ):
        json.dump(d, last_input, indent=1)
    columns = ARGS.width or (terminal_columns() or FALLBACK_COLUMNS) - CLAUDE_MARGIN
    print("\n".join(render_session(d, style, columns)), end="")


def render_session(d: dict, style: str, columns: int) -> list[str]:
    """The lines of a session: its folder's repo (or the repos below it), then the session."""
    cwd = d.get("workspace", {}).get("current_dir") or d.get("cwd") or os.getcwd()
    if re.match(r"[A-Za-z]:[\\/]", cwd):  # called from Claude Code on Windows through wsl.exe
        cwd = sh("wslpath", "-u", cwd) or cwd

    status = Status()
    top = sh("git", "-C", cwd, "rev-parse", "--show-toplevel")
    main_tree = collect_repo(status, cwd, top) if top else ""
    if not top:
        collect_overview(status, cwd)
    collect_session(status, d, main_tree)
    return render(status, style, columns)


if __name__ == "__main__":
    main()
