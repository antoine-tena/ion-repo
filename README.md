<div align="center">

<img src="docs/assets/kiln-logo.svg" alt="kiln's logo: a laughing kiln in pixel art" width="168">

# kiln

*Claude Code's workshop*

**Start every new project, and rescue every old one, like a senior engineer would — even if you're not one.**

Make Claude Code build production-grade repos, bring yours up to that grade, and keep them that way.

[![PyPI](https://img.shields.io/pypi/v/kiln-cli.svg?color=c2551f)](https://pypi.org/project/kiln-cli/)
[![CI](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml/badge.svg?branch=develop)](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-4c4c4c.svg)](LICENSE)

[**Reference**](docs/reference.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Français](README.fr.md)

<img src="docs/assets/kiln-new.gif" alt="kiln new my-app asks three questions (what you build, how big, the team's language), creates a Django and Nuxt app with its first commit, then kiln check passes ruff, mypy, pytest, ESLint, the type checks and charter, and kiln score gives it 100/100" width="820">

<i>A real run, played at 1.5× with the waits cut: <code>kiln new</code>, then <code>kiln check</code> and <code>kiln score</code> in the new repo.</i>

</div>

Claude Code writes code fast. A repo needs more than that to stay healthy: a current stack, rules
an agent cannot argue its way around, a git workflow that survives a bad afternoon, and someone
to stop it going stale on day ninety. kiln brings all four to a new repo in three questions, and
to the one you already have, however old and messy: it lays down the rules, lists what falls
short, and Claude Code works it off. Then it keeps every repo current, release after release.
kiln itself calls no AI and needs no API key.

## Highlights

- A new repo in three questions (what you build, how big, the team's language): code, tests,
  linters, CI, pre-commit hooks, containers and the instructions Claude reads first.
- A repo you already have, however old: `kiln adopt` brings it to the level of `kiln new` on a
  work branch, laying the CI, hooks, rules and instructions it lacks without overwriting a file.
  The rules are checked after each edit Claude makes, the debt they find is listed for Claude to
  work off, and `kiln update` keeps it current like a repo kiln created.
- `kiln update` replays the template, takes compatible dependency upgrades, converts what a
  release renamed and runs your checks before you commit. `--rehearse` tries it on a throwaway
  clone first, `--all` updates every repo in your code folder.
- `charter`, kiln's rule checker, checks each file Claude edits in about 0.15 s: banned tools,
  names, file sizes, personal data in logs. Counts that may only go down (ratchets) and coverage
  floors hold at each commit and in CI. A waiver needs a reason and an end date.
- `kiln grid` lists the practices kiln stands behind, each with its reason, its sources (checked
  and dated) and how it is detected. `kiln score` measures any repo against them in about a
  second, without a token: a score out of 100, one per pillar, and the gaps to close first. `kiln fix` closes on a
  branch those a script can close, one commit per rule, undone if your checks turn red.
  `kiln score --roadmap` hands the rest to Claude Code as a short list with file and line, and
  `/kiln:modernize` works through it, each gap proven closed by `kiln score --rule`.
- Skills for worktrees, merges, releases and reviews; hooks that keep Claude off `main` and
  `develop`; a status line that shows CI, tickets and production.
- A private repo's CI runs on your machine (`kiln ci`, its verdict kept as a git note) and spends
  no GitHub minutes; a public repo's runs on GitHub, where it is free.

## Rescue an old repo

<p align="center">
  <img src="docs/assets/kiln-rescue.gif" alt="kiln score puts an old Django repo at 23 out of 100; kiln adopt, kiln fix and kiln score --roadmap follow; Claude Code works through the roadmap with /kiln:modernize, one commit per gap; kiln score then gives it 100 out of 100" width="820">
</p>
<p align="center"><i>A real run on <a href="https://github.com/antoine-tena/kiln-demo-legacy">kiln-demo-legacy</a>, a Django app left as it was written around 2020, played at 1.5× with the waits cut; Claude Code's five minutes as a time-lapse.</i></p>

`kiln score` puts it at 23/100. `kiln adopt` lays kiln's rules, checks and instructions without
overwriting a file (39), `kiln fix` closes what a script can, one commit per rule (65), and
`kiln score --roadmap` hands the rest to Claude Code. `/kiln:modernize` pins what the code does
today with tests first, then closes each gap in its own commit, proven by `kiln score --rule`:
100/100. The demo repo's README gives the commands to replay it.

## Install

```sh
uv tool install kiln-cli     # the command is kiln; uv fetches Python 3.14 if needed
kiln install                 # outside a repo: kiln's Claude Code plugin in every session
```

With Homebrew: `brew install antoine-tena/kiln/kiln`. Or try it without installing anything:
`uvx kiln-cli new my-app` for a new repo, `uvx kiln-cli adopt` in one you already have. macOS,
Linux and Windows through WSL;
[pnpm](https://pnpm.io/) for JavaScript fronts, [podman](https://podman.io/) for containers.

## Quick start

A new repo:

```console
$ kiln new my-app            # three questions, then a private GitHub repo (--no-github: local)
$ cd my-app && kiln dev      # dev servers in the background, databases first, logs offered
$ kiln check                 # ruff, mypy, ESLint, type checks, then charter (--tests: the suites)
$ claude                     # Claude Code, with kiln's rules, skills and hooks loaded
```

A repo you already have, on a work branch:

```console
$ git switch -c chore/kiln-adopt
$ kiln adopt                 # what kiln new writes, no file overwritten; then what falls short
$ claude                     # Claude Code works it off, with kiln's rules, skills and hooks
```

## What you get

| You build | Backend | Frontend |
|---|---|---|
| A full app (`app`) | Django + Django Ninja | Nuxt + Vue |
| An API (`api`) | FastAPI | — |
| A content site (`site`) | — | Astro |
| A data dashboard (`dashboard`) | polars, marimo, Plotly | Streamlit |
| A data analysis (`analysis`) | polars, marimo, Plotly | — |
| A command-line tool (`cli`) | Python, installable | — |

Next.js, Vite + React, Dash and Java 25 + Maven are there too, and kiln's tests generate and check every
combination. Django and Nuxt are complete; the other stacks are frozen but maintained: new grid
rules go to Django and Nuxt first.

Every repo also gets uv, pnpm and podman (never pip, npm or docker), CI that calls kiln's
reusable workflows, protected `main` and `develop` branches, a `docs/backlog/` of typed tickets,
and a size (`spark`, `ember`, `flame` or `blaze`) that sets how much process it carries. A
Django app can ship to a hardened VPS (Caddy, read-only containers, automatic rollback, tested
backups), a Nuxt front to Vercel.

## Kept current

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/kiln-flow-dark.svg">
    <img src="docs/assets/kiln-flow-light.svg" alt="One release, every repo current: kiln, then a candidate tried on kiln's own repos, the release on PyPI, a rehearsal on a clone of your repo, then kiln update merges it only if the checks pass" width="820">
  </picture>
</p>

A kiln release first ships as a candidate, tagged only once its CI is green on Linux and macOS,
including an update from every release since v0.3.0 through an installed tool. It is promoted
once it has soaked (24 hours and at least one repo updated to it; 2 hours for fixes only), then rehearsed on a clone of each repo before
`kiln update --all` merges it, one worktree per repo. Repos quote kiln's workflows at the exact
release they follow, so nothing reaches them between releases, and `kiln update` shows what is
new in each release it crosses. A repo brought in by `kiln adopt` is updated the same way.

## The grid

<p align="center">
  <img src="docs/assets/kiln-rule.svg" alt="kiln grid pinned-actions: why the rule holds, its theme, scope and level, how it is detected and fixed, its source checked on a date, and how to waive it" width="820">
</p>
<p align="center"><i><code>kiln grid &lt;ID&gt;</code>: one rule in full, with its reason, a source checked on a date, and how a repo can waive it.</i></p>

One small TOML file per rule, on two axes: its theme (supply chain, containers, tests…) and its
scope (universal, a language, a framework, a tool). Each says why, cites sources weighed in a
fixed order (official docs, security advisories, measured studies, adoption data, blogs) and
carries a level from Thoughtworks' Technology Radar: adopt, trial, assess, hold. Only adopted
rules count: 40 of them (supply chain, CI, containers, tests, code standards, Django and Vue
security), each run on two real repos for false positives; 95 drafts wait behind
`kiln grid --level assess`.
Each scored rule ships with a repo that passes it and one that fails it.

## Compared with Copier and cookiecutter

kiln is [Copier](https://copier.readthedocs.io) underneath: every project keeps its
`.copier-answers.yml`, and plain Copier still works on it. kiln adds what comes after day one,
and gives up some breadth for it.

| | cookiecutter | Copier | **kiln** |
|---|:---:|:---:|:---:|
| Generate a project | ✅ | ✅ | ✅ |
| Any language or framework | ✅ | ✅ | ❌ |
| Community templates to start from | ✅ | ✅ | ❌ |
| Apply template updates to existing projects | ❌ | ✅ | ✅ |
| Pick the stack from what you build | ❌ | ❌ | ✅ |
| Change the stack later (`kiln set frontend=nuxt`) | ❌ | partial | ✅ |
| Upgrade dependencies and run the checks in the same step | ❌ | ❌ | ✅ |
| Rehearse, then update every repo at once | ❌ | ❌ | ✅ |
| Shared CI workflows, quoted at a release | ❌ | ❌ | ✅ |
| A rule engine with dated waivers (`charter`) | ❌ | ❌ | ✅ |
| Claude Code skills, hooks and instructions | ❌ | ❌ | ✅ |

kiln is opinionated on purpose. For a neutral templating engine, use Copier; for a workflow that
stays maintained, use kiln, or fork it and make the opinions yours.

## Reference

Every command and option, every `kiln set` key, the reusable workflows and the Claude Code
plugins: [**docs/reference.md**](docs/reference.md). In a terminal, `kiln <command> --help`.

## Status

kiln runs a handful of real repos every day, one of them in production. One maintainer writes it
with Claude Code, under the same rules it gives your repos. Releases are numbered like Claude
Code's: in `0.x`, each release bumps the patch, breaking changes come first in the
[changelog](CHANGELOG.md) and `kiln update` converts them; the minor marks a milestone. Strict
semver starts at 1.0. What comes next is for the repos you already have: any Django or Nuxt repo
scored against the grid in seconds, then brought up to it by script wherever a script can
(v0.5.0).

## Contributing

Issues and pull requests are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md), the
[code of conduct](CODE_OF_CONDUCT.md), and the
[`good first issue`](https://github.com/antoine-tena/kiln/labels/good%20first%20issue) label to
start. In a kiln repo, `/kiln:report` turns a kiln defect into a ready-to-post issue or pull
request, posted only once you approve. If kiln saves you time, a star helps others find it.

## License

[MIT](LICENSE)
