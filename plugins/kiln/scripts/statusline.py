#!/usr/bin/env python3
"""One status line for every folder, in kiln's colors (stone and fire).

The style is chosen per machine (`kiln set statusline=…`, read in `~/.config/kiln/config.toml`):
- `plain` (default): three lines, repo, session (model, gauges, duration), signals sorted by
  importance (tasks, environment, the machine's RAM and CPU);
- `band`: the same on a soot band, important signals as solid pills;
- `classic`: one line per labeled domain (REPO, SESSION, TASKS, ENV, the last one with RAM and
  CPU);
- `classic-band`: the same on a band;
- `none` and `custom`: nothing here (`kiln set` removes or leaves Claude Code's `statusLine`).
The names of before kiln 0.4.0 (`sobre`, `bandeau`, `classique`, `classique-fond`, `aucune`,
`perso`) are still read. `--style <name>` forces a style, for a preview.

Colors tell importance: gray when all is well, then glow (to watch), fire (to handle), ember
(urgent). In a repo: branch, git state, CI, prod, tasks, containers, each shown only when the
repo uses it; outside a repo (~/code): an overview of the repos below. Slow sources are read
from a cache and refreshed in the background.
"""

import contextlib
import datetime
import fcntl
import hashlib
import json
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

# kiln's stone and fire palette (src/kiln/ui.py), copied: the script runs without kiln.
STONE_LIGHT, STONE, STONE_DARK = (185, 185, 180), (140, 140, 135), (95, 95, 92)
BRICK, FIRE, EMBER = (180, 75, 35), (247, 150, 40), (205, 50, 35)
GLOW, WHITE, SOOT = (255, 225, 120), (255, 255, 255), (25, 25, 25)

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
    """Prints the git state of each repo under `root` (except `_*` folders and node_modules)."""
    found = []
    for dirpath, dirs, files in os.walk(root):
        if (".git" in dirs or ".git" in files) and dirpath != root:
            found.append(dirpath)
            dirs.clear()
            continue
        depth = dirpath[len(root) :].count(os.sep)
        dirs[:] = [x for x in dirs if not x.startswith("_") and x != "node_modules" and depth < 2]
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
    """Tickets of docs/backlog/backlog.md (`### T-NN ·`), or else of the former
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
            elif re.match(r"### [A-Z]+-\d+ ·", line):
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

    # CI of the integration branch: replayed on the machine by `kiln ci` (`statusline.ci locale`,
    # verdict in the git note refs/notes/ci, ⏳ while its worktree exists), else GitHub (unless
    # `statusline.ci false`)
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
    name = str(d.get("session_name") or "")
    if name:
        name = name if len(name) <= 24 else name[:23] + "…"
        head.append(Item(f'"{name}"', role="muted", short=""))
    status.session.append(head)

    cw = d.get("context_window") or {}
    pct = cw.get("used_percentage")
    if pct is None and cw.get("context_window_size"):
        used = sum(
            (cw.get("current_usage") or {}).get(k, 0) or 0
            for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
        )
        pct = 100 * used / cw["context_window_size"]
    if pct is not None:
        status.session.append([Item("ctx", quota_level(float(pct)), gauge=float(pct))])

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
        status.usage.append(
            [Item(f"cache {ratio:.0f}%" if warm else "cache cold", 1 if warm and ratio < 70 else 0)]
        )
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
PILLS = {1: (mix(GLOW, SOOT, 0.78), GLOW), 2: (FIRE, SOOT), 3: (EMBER, WHITE)}


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
        return bg(back) + fg(front) + BOLD + f" {t} " + NORMAL + (self.base or RESET)

    def gauge(self, item: Item) -> str:
        pct = item.gauge or 0.0
        out = self.text(item.text + " ", STONE)
        if not item.compact:
            filled = round(pct / 100 * 6)
            out += self.text("▰" * filled, LEVEL_COLORS[item.level] if item.level else STONE_LIGHT)
            out += self.text("▱" * (6 - filled) + " ", STONE_DARK)
        out += self.text(f"{pct:.0f}%", LEVEL_COLORS[item.level], BOLD if item.level else "")
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
                else self.text(item.shown, WHITE, BOLD)
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
    return painter.line(groups)


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
        signals = by_importance(status.tasks + status.env + status.machine)
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
    """`--style <name>`, else the `statusline` key of kiln's machine settings."""
    if "--style" in sys.argv[1:-1]:
        style = sys.argv[sys.argv.index("--style") + 1]
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
        try:
            with open(os.path.join(base, "kiln", "config.toml"), "rb") as file:
                style = str(tomllib.load(file).get("statusline", DEFAULT_STYLE))
        except OSError, tomllib.TOMLDecodeError:
            style = DEFAULT_STYLE
    return LEGACY_STYLES.get(style, style)


def main() -> None:
    if sys.argv[1:2] == ["--scan"]:
        scan(sys.argv[2])
        return
    style = chosen_style()
    if style in SILENT_STYLES:
        return
    if style not in STYLES:
        style = DEFAULT_STYLE
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
    cwd = d.get("workspace", {}).get("current_dir") or d.get("cwd") or os.getcwd()
    if re.match(r"[A-Za-z]:[\\/]", cwd):  # called from Claude Code on Windows through wsl.exe
        cwd = sh("wslpath", "-u", cwd) or cwd

    status = Status()
    top = sh("git", "-C", cwd, "rev-parse", "--show-toplevel")
    main_tree = collect_repo(status, cwd, top) if top else ""
    if not top:
        collect_overview(status, cwd)
    collect_session(status, d, main_tree)
    columns = (terminal_columns() or FALLBACK_COLUMNS) - CLAUDE_MARGIN
    print("\n".join(render(status, style, columns)), end="")


if __name__ == "__main__":
    main()
