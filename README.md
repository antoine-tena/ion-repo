<div align="center">

<img src="docs/assets/kiln-logo.svg" alt="ion-repo's logo: a laughing kiln in pixel art" width="168">

# ion-repo

*Claude Code's workshop*

**Start every new project, and rescue every old one, like a senior engineer would — even if you're not one.**

Make Claude Code build production-grade repos, bring yours up to that grade, and keep them that way.

[![PyPI](https://img.shields.io/pypi/v/kiln-cli.svg?color=c2551f)](https://pypi.org/project/kiln-cli/)
[![CI](https://github.com/antoine-tena/ion-repo/actions/workflows/kiln.yml/badge.svg?branch=develop)](https://github.com/antoine-tena/ion-repo/actions/workflows/kiln.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/antoine-tena/ion-repo/badge)](https://scorecard.dev/viewer/?uri=github.com/antoine-tena/ion-repo)
[![License: MIT](https://img.shields.io/badge/license-MIT-4c4c4c.svg)](LICENSE)

[**Reference**](docs/reference.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Français](README.fr.md)

<img src="docs/assets/kiln-new.gif" alt="ion repo new my-app asks three questions (what you build, how big, the team's language), creates a Django and Nuxt app with its first commit, then ion repo check passes ruff, mypy, pytest, ESLint, the type checks and charter, and ion repo score gives it 100/100" width="820">

<i>A real run, played at 1.5× with the waits cut: <code>ion repo new</code>, then <code>ion repo check</code> and <code>ion repo score</code> in the new repo.</i>

</div>

Claude Code writes code fast. A repo needs more than that to stay healthy: a current stack, rules
an agent cannot argue its way around, a git workflow that survives a bad afternoon, and someone
to stop it going stale on day ninety. ion-repo brings all four to a new repo in three questions, and
to the one you already have, however old and messy: it lays down the rules, lists what falls
short, and Claude Code works it off. Then it keeps every repo current, release after release.
ion-repo itself calls no AI and needs no API key.

## Highlights

- A new repo in three questions (what you build, how big, the team's language): code, tests,
  linters, CI, pre-commit hooks, containers and the instructions Claude reads first.
- A repo you already have, however old: `ion repo adopt` brings it to the level of `ion repo new` on a
  work branch, laying the CI, hooks, rules and instructions it lacks without overwriting a file.
  The rules are checked after each edit Claude makes, the debt they find is listed for Claude to
  work off, and `ion repo update` keeps it current like a repo ion-repo created.
- `ion repo update` replays the template, takes compatible dependency upgrades, converts what a
  release renamed and runs your checks before you commit. `--rehearse` tries it on a throwaway
  clone first, `--all` updates every repo in your code folder.
- `charter`, ion-repo's rule checker, checks each file Claude edits in about 0.15 s: banned tools,
  names, file sizes, personal data in logs. Counts that may only go down (ratchets) and coverage
  floors hold at each commit and in CI. A waiver needs a reason and an end date.
- `ion repo grid` lists the practices ion-repo stands behind, each with its reason, its sources (checked
  and dated) and how it is detected. `ion repo score` measures any repo against them in about a
  second, without a token: a score out of 100, one per pillar, and the gaps to close first. `ion repo fix` closes on a
  branch those a script can close, one commit per rule, each proven, set aside if your checks turn
  red. `ion repo score --roadmap` hands the rest to Claude Code as a short list with file and line,
  and `/repo:modernize` works through it, each gap proven closed by `ion repo score --rule`.
  [kiln-bot](docs/reference.md) brings the fixes as a weekly pull request, in one
  copy-paste.
- Skills for worktrees, merges, releases and reviews; hooks that keep Claude off `main` and
  `develop`; a status line that shows CI, tickets and production.
- A private repo's CI runs on your machine (`ion repo ci`, its verdict kept as a git note) and spends
  no GitHub minutes; a public repo's runs on GitHub, where it is free.

## Rescue an old repo

<p align="center">
  <img src="docs/assets/kiln-rescue.gif" alt="ion repo score puts an old Django repo at 23 out of 100; ion repo adopt, ion repo fix and ion repo score --roadmap follow; Claude Code works through the roadmap with /repo:modernize, one commit per gap; ion repo score then gives it 100 out of 100" width="820">
</p>
<p align="center"><i>A real run on <a href="https://github.com/antoine-tena/kiln-demo-legacy">kiln-demo-legacy</a>, a Django app left as it was written around 2020, played at 1.5× with the waits cut; Claude Code's five minutes as a time-lapse.</i></p>

`ion repo score` puts it at 23/100. `ion repo adopt` lays ion-repo's rules, checks and instructions without
overwriting a file (39), `ion repo fix` closes what a script can, one commit per rule (65), and
`ion repo score --roadmap` hands the rest to Claude Code. `/repo:modernize` pins what the code does
today with tests first, then closes each gap in its own commit, proven by `ion repo score --rule`:
100/100. The demo repo's README gives the commands to replay it.

## Install

```sh
uv tool install kiln-cli     # uv fetches Python 3.14 if needed
kiln install                 # outside a repo: ion-repo's Claude Code plugin in every session
```

The published release still answers to `kiln`, under its former name: below, read `kiln` for
`ion repo` until `ion-repo` and `ion-sh` reach PyPI at the next release.

With Homebrew: `brew install antoine-tena/ion/kiln`. Or try it without installing anything:
`uvx kiln-cli new my-app` for a new repo, `uvx kiln-cli adopt` in one you already have. macOS,
Linux and Windows through WSL;
[pnpm](https://pnpm.io/) for JavaScript fronts, [podman](https://podman.io/) for containers.

## Quick start

A new repo:

```console
$ ion repo new my-app            # three questions, then a private GitHub repo (--no-github: local)
$ cd my-app && ion repo dev      # dev servers in the background, databases first, logs offered
$ ion repo check                 # ruff, mypy, ESLint, type checks, then charter (--tests: the suites)
$ claude                     # Claude Code, with ion-repo's rules, skills and hooks loaded
```

A repo you already have, on a work branch:

```console
$ git switch -c chore/ion-repo-adopt
$ ion repo adopt                 # what ion repo new writes, no file overwritten; then what falls short
$ claude                     # Claude Code works it off, with ion-repo's rules, skills and hooks
```

## What you get

| You build | Backend | Frontend |
|---|---|---|
| A full app (`app`) | Django + Django Ninja | Nuxt + Vue |
| An API (`api`) | FastAPI | — |
| A content site (`site`) | — | Astro |
| A data dashboard (`dashboard`) | polars, marimo, Plotly | Streamlit |
| A data analysis (`analysis`) | polars, marimo, Plotly | — |
| A command-line tool (`cli`) | Python, installable, with its own Claude Code plugin if you want one | — |

Next.js, Vite + React, Dash and Java 25 + Maven are there too, and ion-repo's tests generate and check every
combination. Django and Nuxt are complete; the other stacks are frozen but maintained: new grid
rules go to Django and Nuxt first.

Every repo also gets uv, pnpm and podman (never pip, npm or docker), CI that calls ion-repo's
reusable workflows, protected `main` and `develop` branches, a `docs/backlog/` of typed tickets,
and a size (`tiny`, `small`, `medium` or `large`) that sets how much process it carries. A
Django app can ship to a hardened VPS (Caddy, read-only containers, automatic rollback, tested
backups), a Nuxt front to Vercel.

## Kept current

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/kiln-flow-dark.svg">
    <img src="docs/assets/kiln-flow-light.svg" alt="One release, every repo current: ion-repo, then a candidate tried on ion-repo's own repos, the release on PyPI, a rehearsal on a clone of your repo, then ion repo update merges it only if the checks pass" width="820">
  </picture>
</p>

An ion-repo release first ships as a candidate, tagged only once its CI is green on Linux and macOS,
including an update from every release since v0.3.0 through an installed tool. It is promoted
once it has soaked (24 hours and at least one repo updated to it; 2 hours for fixes only), then rehearsed on a clone of each repo before
`ion repo update --all` merges it, one worktree per repo. Repos quote ion-repo's workflows at the exact
release they follow, so nothing reaches them between releases, and `ion repo update` shows what is
new in each release it crosses. A repo brought in by `ion repo adopt` is updated the same way.

## The grid

<p align="center">
  <img src="docs/assets/kiln-rule.svg" alt="ion repo grid pinned-actions: why the rule holds, its theme, scope and level, how it is detected and fixed, its source checked on a date, and how to waive it" width="820">
</p>
<p align="center"><i><code>ion repo grid &lt;ID&gt;</code>: one rule in full, with its reason, a source checked on a date, and how a repo can waive it.</i></p>

One small TOML file per rule, on two axes: its theme (supply chain, containers, tests…) and its
scope (universal, a language, a framework, a tool). Each says why, cites sources weighed in a
fixed order (official docs, security advisories, measured studies, adoption data, blogs) and
carries a level from Thoughtworks' Technology Radar: adopt, trial, assess, hold. Only adopted
rules count: 43 of them (supply chain, CI, containers, tests, code standards, Django and Vue
security), each run on two real repos for false positives; 96 drafts wait behind
`ion repo grid --level assess`.
Each scored rule ships with a repo that passes it and one that fails it.

## Compared with Copier and cookiecutter

ion-repo is [Copier](https://copier.readthedocs.io) underneath: every project keeps its
`.copier-answers.yml`, and plain Copier still works on it. ion-repo adds what comes after day one,
and gives up some breadth for it.

| | cookiecutter | Copier | **ion-repo** |
|---|:---:|:---:|:---:|
| Generate a project | ✅ | ✅ | ✅ |
| Any language or framework | ✅ | ✅ | ❌ |
| Community templates to start from | ✅ | ✅ | ❌ |
| Apply template updates to existing projects | ❌ | ✅ | ✅ |
| Pick the stack from what you build | ❌ | ❌ | ✅ |
| Change the stack later (`ion repo set frontend=nuxt`) | ❌ | partial | ✅ |
| Upgrade dependencies and run the checks in the same step | ❌ | ❌ | ✅ |
| Rehearse, then update every repo at once | ❌ | ❌ | ✅ |
| Shared CI workflows, quoted at a release | ❌ | ❌ | ✅ |
| A rule engine with dated waivers (`charter`) | ❌ | ❌ | ✅ |
| Claude Code skills, hooks and instructions | ❌ | ❌ | ✅ |

ion-repo is opinionated on purpose. For a neutral templating engine, use Copier; for a workflow that
stays maintained, use ion-repo, or fork it and make the opinions yours.

## Reference

Every command and option, every `ion repo set` key, the reusable workflows and the Claude Code
plugins: [**docs/reference.md**](docs/reference.md). In a terminal, `ion-repo <command> --help`.

## Status

ion-repo runs a handful of real repos every day, one of them in production. One maintainer writes it
with Claude Code, under the same rules it gives your repos. Releases are numbered like Claude
Code's: in `0.x`, each release bumps the patch, breaking changes come first in the
[changelog](CHANGELOG.md) and `ion repo update` converts them; the minor marks a milestone. Strict
semver starts at 1.0. What comes next is for the repos you already have: any Django or Nuxt repo
scored against the grid in seconds, then brought up to it by script wherever a script can
(v0.5.0). Then Claude Code closing alone what a script leaves, whole organisations, every common
stack, CI and machine, and the stability promise of 1.0, release by release:
[**ROADMAP.md**](ROADMAP.md).

## Contributing

Issues and pull requests are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md), the
[code of conduct](CODE_OF_CONDUCT.md), and the
[`good first issue`](https://github.com/antoine-tena/ion-repo/labels/good%20first%20issue) label to
start. In an ion-repo repo, `/repo:report` turns an ion-repo defect into a ready-to-post issue or pull
request, posted only once you approve. If ion-repo saves you time, a star helps others find it.

## License

[MIT](LICENSE)
