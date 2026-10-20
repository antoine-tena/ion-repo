<div align="center">

# kiln 🔥

**Start every project like a senior engineer would — even if you're not one.**

Three questions, and Claude Code gets a modern repo: stack chosen for you, tests, CI,
guardrails, a GitHub repo — kept up to date for as long as the project lives.

[![CI](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml/badge.svg?branch=develop)](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Built on Copier](https://img.shields.io/badge/built%20on-Copier-8a2be2.svg)](https://copier.readthedocs.io)
[![Claude Code plugins](https://img.shields.io/badge/Claude%20Code-plugins-d97757.svg)](#claude-code-plugins)

*English · [Français](README.fr.md)*

<img src="docs/assets/kiln-home.svg" alt="kiln welcome screen: a pixel-art kiln and the list of commands" width="720">

</div>

---

Claude Code writes code fast, but a real repo needs more than a prompt: an up-to-date stack,
rules the agent cannot talk its way around, a sane git workflow, and someone to stop the repo
from going stale on day ninety. **kiln** brings all four. Built on
[Copier](https://copier.readthedocs.io), it generates the repo, wires Claude Code into it, and
keeps every repo you own current:

- 🧱 **`kiln new`** — three questions (what you are building, its size, your language), then
  a complete repo: code, tests, linters, CI, pre-commit, containers, a `CLAUDE.md` for AI
  agents, a GitHub repo with protected branches.
- 🎛️ **`kiln set`** — change your mind later. `kiln set frontend=nuxt podman=true` re-renders
  the repo; a removed framework takes its files with it.
- 🔄 **`kiln update`** — pull template improvements *and* dependency upgrades into an existing
  repo, then run the checks before anything is committed. Local edits are kept; real conflicts
  are marked inline.
- 🚚 **`kiln update --all`** — do it for **every** kiln repo in `~/code` at once: one worktree
  per repo, small commits, merge only when the checks pass.
- 📏 **`charter`** — a rule engine for things linters don't catch (no `pip`/`docker`, file-size
  ratchets, Django locks, personal-data patterns, coverage floors…), declared per repo in
  `charter.toml`. Disagree with a rule? `kiln waive` it in `kiln-waivers.toml`, with a reason and an
  expiry that grows with each renewal (a week, a month, three months, six months).
- 🤖 **Claude Code native** — every generated repo ships agent instructions and enables kiln's
  Claude Code plugins (branch guards, worktree/merge/release skills, status line).

> [!NOTE]
> kiln was born to run a real production app (a non-profit's Django + Nuxt site) and the
> repos around it. Since v0.4.0 it speaks English: commands, messages, generated code and
> docs. What your users read (pages, messages, README) follows the project's language, English
> or French.

## Quick start

```sh
# 1. Install (needs uv and git; Python 3.14 is fetched by uv if missing).
#    macOS, Linux, and Windows through WSL. The PyPI package is kiln-cli, the command is kiln.
uv tool install kiln-cli
#    …or try it without installing anything: uvx kiln-cli new my-app
#    Tab completion in bash: add  eval "$(kiln completion bash)"  to ~/.bashrc

# 2. Create a project — answer a few questions, or pass them as flags
kiln new my-app
kiln new my-api --size ember --type api --backend fastapi --no-github

# 3. Work in it
cd my-app
kiln dev       # start the dev servers of the stack
kiln check     # ruff, mypy, pytest, ESLint, type checks, then charter

# 4. Months later
kiln update            # template changes + compatible dependency upgrades + checks
kiln update --major    # major versions too
```

`kiln new` creates a private GitHub repo by default (via `gh`); `--no-github` skips it.
Optional tools: [pnpm](https://pnpm.io/) for JavaScript fronts, a JDK 25 for Java,
[podman](https://podman.io/) for containers.

## What you get

| Project type | Recommended backend | Recommended frontend |
|---|---|---|
| Full app (`app`) | Django + Django Ninja | Nuxt + Vue |
| API only (`api`) | FastAPI | — |
| Content site (`site`) | — | Astro |
| Data dashboard (`dashboard`) | Python data (polars, marimo, Plotly) | Streamlit |
| Data analysis (`analysis`) | Python data | — |
| CLI tool (`cli`) | Python CLI (argparse, installable) | — |

Backends: `django`, `fastapi`, `data`, `cli`, `java` (Java 25 + Maven, no framework).
Frontends: `nuxt`, `next`, `astro`, `streamlit`, `dash`. **Every combination is generated and
validated by the test suite.**

**Django and Nuxt: complete. The others: frozen, maintained.** Every stack stays generated and
tested, but new grid rules go to Django and Nuxt first, until they reach the top of the grid;
the universal rules (CI, containers, supply chain, secrets) score them all.

Each generated repo comes with:

- **Opinionated tooling, no `pip`, no `docker`:** uv for Python, pnpm for JavaScript, podman
  for containers; ruff, mypy (strict), pytest + coverage floor, ESLint, pre-commit (which also
  refuses commits on `main`/`develop`).
- **CI on GitHub Actions** that calls kiln's reusable workflows — so fixing CI once in kiln
  fixes it everywhere.
- **A project size** (`spark` → `ember` → `flame` → `blaze`) that tunes defaults: a weekend
  script doesn't get the same ceremony as a multi-team service.
- **Agent-ready instructions:** kiln's rules for Claude in `.claude/rules/kiln/`, with stable
  rule IDs the `charter` engine can check; each stack's rules load only when Claude touches its
  files. The root `CLAUDE.md` belongs to the project.
- **Optional production setups:** a hardened VPS deployment for Django (Caddy with automatic
  TLS, read-only containers, one image per commit, automatic rollback, daily backups with
  restore tests) and Vercel deployment for Nuxt fronts.
- **A backlog** (`docs/backlog/`: typed `T-NN` tickets by priority) that Claude Code's status line counts.

## Why not just Copier / cookiecutter?

kiln **is** Copier underneath — every project keeps its `.copier-answers.yml`, so you can
always fall back to plain Copier. What kiln adds is everything around the template:

| | cookiecutter | Copier | **kiln** |
|---|:---:|:---:|:---:|
| Generate a project | ✅ | ✅ | ✅ |
| Apply template updates to existing projects | ❌ | ✅ | ✅ |
| Stack recommendation from the project type | ❌ | ❌ | ✅ |
| Change stack/options after generation (`kiln set`) | ❌ | partial | ✅ |
| Upgrade dependencies + run checks in the same step | ❌ | ❌ | ✅ |
| Update all your repos at once (`update --all`) | ❌ | ❌ | ✅ |
| Shared, reusable CI workflows | ❌ | ❌ | ✅ |
| Repo-level rule engine (`charter`) | ❌ | ❌ | ✅ |
| Replay CI locally, verdict stored as a git note (`kiln ci`) | ❌ | ❌ | ✅ |
| Claude Code plugins and agent instructions | ❌ | ❌ | ✅ |

kiln is opinionated on purpose. If you want a neutral templating engine, use Copier directly;
if you want a batteries-included workflow that stays maintained, use kiln — or fork it and
make the opinions yours.

## Commands

| Command | What it does |
|---|---|
| `kiln new [dir]` | Questionnaire, generation, lockfiles, install, first commit on `main`, then `develop` where all work happens. Three questions (what you build, size, language), the rest by option: `--name`, `--title`, `--description`, `--type`, `--size`, `--backend`, `--frontend`, `--language`, `--owner`, `--team`, `--podman`, `--vps`, `--goal`, `--prod-url`; `--no-github` (local only), `--no-install`, `--template` (another source), `--all-questions` (the whole questionnaire). |
| `kiln adopt` | Bring an existing repo that kiln did not generate under kiln (`--template` for another source), on a work branch: `charter.toml` (size via `--size`, rules that apply anywhere, checked after each edit), `docs/backlog/` if missing, then the existing debt the charter finds. Never touches an existing file. |
| `kiln publish` | Create the private GitHub repo and protect its branches, for a project generated without `gh`. |
| `kiln install` | Set up a machine after a clone: tools, dependencies, `.env`, migrations, pre-commit. Re-runnable. |
| `kiln dev` | Start the stack's dev servers, their output interleaved and prefixed by service in colour (`django │ …`); `--containers` runs everything in podman. |
| `kiln check` | Ruff, mypy, pytest for each Python project, ESLint and type checks for the front, then `charter`. |
| `kiln set [key=value…]` | Show or change the repo's settings (see [Settings](#settings)); the repo is re-rendered. Outside a repo, or with `--global`, this machine's settings. |
| `kiln waive [RULE\|file]` | Waive a kiln rule (`--paths`, `--reason`), or freeze a generated file so `kiln update` leaves it alone; `--renew` moves to the next tier (a week, a month, three months, six months); `--permanent` for a waiver with no deadline, `--upstream` to link the issue or PR opened on kiln. No argument: list the waivers. |
| `kiln update` | Move to the latest kiln release (with a box listing what's new in each release crossed), compatible dependency upgrades, then checks. `--major`, `--no-template`, `--no-deps`. `--rehearse` plays it on a throwaway clone first and only reports, the repo untouched. In an adopted repo (`kiln adopt`), only the references to kiln's workflows move, to the latest public release, their inputs checked. Only a release of kiln updates a repo: a tool built from a checkout is refused, with the command that installs the release. |
| `kiln update --all` | Update every kiln repo in your code folder, one worktree each, merged only if checks pass. `--all --rehearse`: each update on a clone, nothing touched, a summary per repo. |
| `kiln status` | Branch, clean tree, template release (`v0.4.0 → v0.4.2` when behind), waivers, stack — for every kiln repo, then the most waived rules across them. |
| `kiln version` | In kiln's own repo: latest public release, candidates (age, adopting repos, ready to promote), the number the next release should take and the planned tickets still open. `--minor` when the next one is a milestone. `kiln version cut` cuts the release branch with a drafted changelog entry, then (once the entry is rewritten) runs the checks, waits for GitHub's CI and tags `-rc.N` only on green; `kiln version promote` tags the ready candidate (green CI), merges it into `main` and `develop`, and PyPI and the GitHub Release follow. |
| `kiln grid [RULE-ID]` | The grid: the practices kiln holds as the best today, one small TOML file per rule, each with its why, its sources (checked and dated), its level (adopt, trial, assess, hold) and how it is detected and fixed. `--theme`, `--scope`, `--level` filter; a rule ID shows it in full, with how to waive it. |
| `kiln doctor` | Check the machine (git, uv, gh login, pnpm, podman, Java, pre-commit, kiln release, Claude plugin) and the current repo; each problem comes with the command that fixes it. Changes nothing. |
| `kiln ci [commit]` | Replay the repo's GitHub CI locally against throwaway PostgreSQL/Redis, and push the verdict as a git note (`--skip <job>`, `--no-push` to keep the note local, `--keep` the commit's worktree, `--status` for the verdict only). A private repo runs its CI this way by default (`ci_runner: local`): no GitHub minutes spent; a public one runs on GitHub, free. `kiln set ci_runner=github` switches. |
| `kiln contract` | Django + Nuxt: export `openapi.json` and regenerate the front's API types. |
| `kiln completion bash` | Print a bash completion script built from the parser; enable it with `eval "$(kiln completion bash)"` in `~/.bashrc`. |
| `charter` | Check the repo against its `charter.toml` (`--detail`, `--unverified`, `types`, `coverage`, `file <path>`); `charte` is its former name. |

Full reference (in French): [README.fr.md](README.fr.md#commandes).

## Settings

Every answer of the template, shown by `kiln set` and changed by `kiln set key=value` (the repo
is re-rendered, on a work branch):

| Key | What it sets |
|---|---|
| `name`, `title`, `description` | Short name (packages' prefix), displayed title, one sentence. |
| `project_type`, `size` | What you build (`app`, `api`, `site`, `dashboard`, `analysis`, `cli`) and how hot it burns (`spark`, `ember`, `flame`, `blaze`): the stack and the rules follow. |
| `backend`, `frontend`, `podman` | The stack (see [What you get](#what-you-get)) and podman containers. |
| `language`, `language_comments`, `language_commits`, `language_docs`, `language_tickets`, `language_ui` | The team's language, and per use when they differ. |
| `owner`, `team` | GitHub account owning the repo, and the team's logins (reviewers). |
| `java_package` | Root package of the Java sources. |
| `timezone` | Time zone of the project's calendar notions (dates are stored in UTC). |
| `serena` | Serena for Claude Code (symbol navigation on big codebases). |
| `deploy`, `vps_host`, `api_domain`, `site_url`, `deploy_branch`, `frontend_deploy` | Production: a hardened VPS (SSH host, API domain, site address, deployed branch) and the front on Vercel. |
| `north_star` | The goal that orders the priorities of `docs/backlog/`. |
| `ci_runner` | Where each push's CI runs: `local` (`kiln ci`, no GitHub minutes, a private repo's default) or `github` (free for a public repo). |
| `statusline_ci`, `prod_health_url` | Claude Code's status line: CI state, and production's health probe. |

## Reusable GitHub workflows

kiln's workflows work from any repository, kiln-generated or not:

```yaml
jobs:
  backend:
    uses: antoine-tena/kiln/.github/workflows/django.yml@v0.4.1   # a kiln release tag
```

`django.yml`, `python.yml`, `maven.yml`, `pnpm.yml`, `charter.yml`, `security.yml` (`uv audit`,
`pnpm audit`), `secrets.yml` (gitleaks), `api-contract.yml`, `infra.yml` (podman build,
actionlint, shellcheck), `sbom.yml` (CycloneDX), `mutation.yml` (mutmut), `vercel.yml`. `charte.yml`,
`securite.yml` and `contrat-api.yml` are their former names, kept as relays. Databases for tests run in
podman. See [`.github/workflows/`](.github/workflows/).

## Claude Code plugins

kiln is also a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace:

```sh
claude plugin marketplace add antoine-tena/kiln
claude plugin install kiln@kiln
```

| Plugin | What's inside |
|---|---|
| `kiln` | Skills for the git workflow (`worktree`, `merge`, `release`, `cleanup`, `review` = a branch's commits before they go public, and the whole repo before a release, `backlog`, `update` = self-update, `adopt` = bring an existing repo under kiln), `report` (a kiln defect met in your repo becomes an issue or a PR, posted once you approve), `contribution` (an outside contributor's PR handled like a well-run open-source project: untrusted code read before anything runs, triage, review, a merge that credits them, nothing posted without your yes), `good-first-issues` (a small, steady stock of `good first issue` issues drawn from your backlog and reserved for newcomers, refilled as they get merged) and `token` (a service token pasted once into a git-ignored `.<service>/` folder, never shown); hooks that guard protected branches and files (`branch_guard.py`, `protect_files.py`), refuse a commit message signed by Claude, check each edited file (`check_file.py`), and ask at session start (`session_start.py`, with kiln's logo and what's new above the first prompt, `first_prompt.py`; a red integration branch is told to Claude): kiln updates in kiln repos, adoption in your other repos ("Yes", "Later", "Never for this repo"), all paced by one goodwill score that each yes raises and each no lowers (`reminders.py`); a shared status line in four styles (`kiln set statusline=…`, or `none` / `custom` to keep your own); condensed command output with [rtk](https://github.com/rtk-ai/rtk) (`rtk.py`). |
| `django` | Skills `migration`, `regen-api` (API types regenerated) and `postgres-read` (read-only PostgreSQL MCP). |
| `nuxt` | Skills `nuxt`, `vue-best-practices`, `vue-testing-best-practices`, `vitest`, `polish` (UI polish) and `preview` (screenshots on three phones and a desktop, Playwright MCP). |
| `vps` | Skills `deploy`, `prod-logs` (read-only diagnosis) and `prod-dump` (production copied into a throwaway database). |
| `stripe` | Stripe MCP in test mode. |
| `serena` | Read-only [Serena](https://github.com/oraios/serena) MCP for symbol navigation in big repos. |

Generated repos enable the right plugins for their stack automatically.

## Status

kiln is used daily on a handful of real repos, including one in production. It is young, so it
numbers releases like Claude Code does: in `0.x`, every release bumps the patch, breaking changes
included (`0.4.1 → 0.4.2`), listed first in the release notes and migrated by `kiln update`; the
minor only moves for a milestone. Strict semver starts at 1.0. Each release is first a candidate
(`v0.4.2-rc.1`) used on the author's own repos; it is promoted to `main` (`v0.4.2`) only once
the next candidate is ready, its CI green (macOS and end-to-end tests included) and its update
rehearsed on a copy of each repo, so a release never needs an emergency fix. Projects are generated and updated from the latest release, pin kiln's workflows to
that exact tag, and `kiln update` shows what changed in each release it applies (see
[`CHANGELOG.md`](CHANGELOG.md)).
Linux, WSL and macOS are supported.

## Contributing

Issues and pull requests are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
Small fixes can go straight to a PR; for bigger changes, open an issue first so we agree on
the approach. Good places to start: the
[`good first issue`](https://github.com/antoine-tena/kiln/labels/good%20first%20issue) label.
Using Claude Code in a kiln repo? `/kiln:report` turns a kiln defect into a
ready-to-post issue or PR: checked against the latest release and the existing issues, scrubbed
of anything private, posted only once you approve.

If kiln saves you time, a ⭐ helps other people find it.

## License

[MIT](LICENSE)
