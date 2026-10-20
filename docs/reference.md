# kiln reference

Everything kiln offers, at the release it is: every command and option, every setting, the
reusable workflows and the Claude Code plugins. The [README](../README.md) shows what kiln is
for; this page is what you look things up in. `tests/test_docs.py` fails when a command,
option, setting, plugin, skill, hook or workflow is missing here.

*English · [Français](reference.fr.md)*

- [Commands](#commands)
- [Settings](#settings)
- [What a generated repo holds](#what-a-generated-repo-holds)
- [Reusable GitHub workflows](#reusable-github-workflows)
- [Claude Code plugins](#claude-code-plugins)
- [Releases](#releases)

## Commands

<p align="center">
  <img src="assets/kiln-home.svg" alt="kiln's welcome screen: a pixel-art kiln above its commands, grouped by project, day to day, the grid and all repos" width="620">
</p>
<p align="center"><i><code>kiln</code> on its own: every command, grouped by what you are doing.</i></p>

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
| `kiln score [PATH]` | Any repo, made by kiln or not, measured against the grid's scored rules in about a second, offline and without a token: a score out of 100 and one per pillar (every rule that applies weighs the same; rules outside the repo's stacks, or with nothing to look at, are left out), the three gaps to close first, then each gap with its reason, where it is, its source and what closes it. Waived rules (`kiln-waivers.toml`) are shown apart. `--all` lists every rule and location, `--json` the report (schema 1), `--badge` a README badge, `--online` refreshes end-of-life dates from endoflife.date. Nothing is written in the repo. |
| `kiln doctor` | Check the machine (git, uv, gh login, pnpm, podman, Java, pre-commit, kiln release, Claude plugin) and the current repo; each problem comes with the command that fixes it. Changes nothing. |
| `kiln ci [commit]` | Replay the repo's GitHub CI locally against throwaway PostgreSQL/Redis, and push the verdict as a git note (`--skip <job>`, `--no-push` to keep the note local, `--keep` the commit's worktree, `--status` for the verdict only). A private repo runs its CI this way by default (`ci_runner: local`): no GitHub minutes spent; a public one runs on GitHub, free. `kiln set ci_runner=github` switches. |
| `kiln contract` | Django + Nuxt: export `openapi.json` and regenerate the front's API types. |
| `kiln completion bash` | Print a bash completion script built from the parser; enable it with `eval "$(kiln completion bash)"` in `~/.bashrc`. |
| `charter` | Check the repo against its `charter.toml` (`--detail`, `--unverified`, `types`, `coverage`, `file <path>`); `charte` is its former name. |


<p align="center">
  <img src="assets/kiln-grid.svg" alt="kiln grid: the rules kiln stands behind, by theme, each with its level" width="680">
</p>
<p align="center"><i><code>kiln grid</code>: the rules kiln stands behind today; <code>kiln grid &lt;ID&gt;</code> shows one in full, as in the README.</i></p>

## Settings

Every answer of the template, shown by `kiln set` and changed by `kiln set key=value` (the repo
is re-rendered, on a work branch):

| Key | What it sets |
|---|---|
| `name`, `title`, `description` | Short name (packages' prefix), displayed title, one sentence. |
| `project_type`, `size` | What you build (`app`, `api`, `site`, `dashboard`, `analysis`, `cli`) and how hot it burns (`spark`, `ember`, `flame`, `blaze`): the stack and the rules follow. |
| `backend`, `frontend`, `podman` | The stack (see [What you get](../README.md#what-you-get)) and podman containers. |
| `language`, `language_comments`, `language_commits`, `language_docs`, `language_tickets`, `language_ui` | The team's language, and per use when they differ. |
| `owner`, `team` | GitHub account owning the repo, and the team's logins (reviewers). |
| `java_package` | Root package of the Java sources. |
| `timezone` | Time zone of the project's calendar notions (dates are stored in UTC). |
| `serena` | Serena for Claude Code (symbol navigation on big codebases). |
| `deploy`, `vps_host`, `api_domain`, `site_url`, `deploy_branch`, `frontend_deploy` | Production: a hardened VPS (SSH host, API domain, site address, deployed branch) and the front on Vercel. |
| `north_star` | The goal that orders the priorities of `docs/backlog/`. |
| `ci_runner` | Where each push's CI runs: `local` (`kiln ci`, no GitHub minutes, a private repo's default) or `github` (free for a public repo). |
| `statusline_ci`, `prod_health_url` | Claude Code's status line: CI state, and production's health probe. |

## What a generated repo holds

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

## Reusable GitHub workflows

kiln's workflows work from any repository, kiln-generated or not:

```yaml
jobs:
  backend:
    uses: antoine-tena/kiln/.github/workflows/django.yml@v0.4.2   # a kiln release tag
```

`django.yml`, `python.yml`, `maven.yml`, `pnpm.yml`, `charter.yml`, `security.yml` (`uv audit`,
`pnpm audit`), `secrets.yml` (gitleaks), `api-contract.yml`, `infra.yml` (podman build,
actionlint, shellcheck), `sbom.yml` (CycloneDX), `mutation.yml` (mutmut), `vercel.yml`. `charte.yml`,
`securite.yml` and `contrat-api.yml` are their former names, kept as relays. Databases for tests run in
podman. See [`.github/workflows/`](../.github/workflows/).

## Claude Code plugins

kiln is also a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace:

```sh
claude plugin marketplace add antoine-tena/kiln
claude plugin install kiln@kiln
```

| Plugin | What's inside |
|---|---|
| `kiln` | Skills for the git workflow (`worktree`, `merge`, `release`, `cleanup`, `review` = a branch's commits before they go public, and the whole repo before a release, `backlog`, `update` = self-update, `adopt` = bring an existing repo under kiln), `report` (a kiln defect met in your repo becomes an issue or a PR, posted once you approve), `contribution` (an outside contributor's PR handled like a well-run open-source project: untrusted code read before anything runs, triage, review, a merge that credits them, nothing posted without your yes), `good-first-issues` (a small, steady stock of `good first issue` issues drawn from your backlog and reserved for newcomers, refilled as they get merged) and `token` (a service token pasted once into a git-ignored `.<service>/` folder, never shown); hooks that guard protected branches and files (`branch_guard.py`, `protect_files.py`), refuse a commit message signed by Claude, check each edited file (`check_file.py`), and ask at session start (`session_start.py`, with kiln's logo and what's new above the first prompt, `first_prompt.py`; a red integration branch is told to Claude, a run GitHub never started apart from a failure of the code): kiln updates in kiln repos, adoption in your other repos ("Yes", "Later", "Never for this repo"), all paced by one goodwill score that each yes raises and each no lowers (`reminders.py`); a shared status line in four styles (`kiln set statusline=…`, or `none` / `custom` to keep your own); condensed command output with [rtk](https://github.com/rtk-ai/rtk) (`rtk.py`). |
| `django` | Skills `migration`, `regen-api` (API types regenerated) and `postgres-read` (read-only PostgreSQL MCP). |
| `nuxt` | Skills `nuxt`, `vue-best-practices`, `vue-testing-best-practices`, `vitest`, `polish` (UI polish) and `preview` (screenshots on three phones and a desktop, Playwright MCP). |
| `vps` | Skills `deploy`, `prod-logs` (read-only diagnosis) and `prod-dump` (production copied into a throwaway database). |
| `stripe` | Stripe MCP in test mode. |
| `serena` | Read-only [Serena](https://github.com/oraios/serena) MCP for symbol navigation in big repos. |

Generated repos enable the right plugins for their stack automatically.

## Releases

kiln is used daily on a handful of real repos, including one in production. It is young, so it
numbers releases like Claude Code does: in `0.x`, every release bumps the patch, breaking changes
included (`0.4.1 → 0.4.2`), listed first in the release notes and migrated by `kiln update`; the
minor only moves for a milestone. Strict semver starts at 1.0. Each release is first a candidate
(`v0.4.2-rc.1`) used on the author's own repos; it is promoted to `main` (`v0.4.2`) only once
the next candidate is ready, its CI green (macOS and end-to-end tests included) and its update
rehearsed on a copy of each repo, so a release never needs an emergency fix. Projects are generated and updated from the latest release, pin kiln's workflows to
that exact tag, and `kiln update` shows what changed in each release it applies (see
[`CHANGELOG.md`](../CHANGELOG.md)).
Linux, WSL and macOS are supported.

<p align="center">
  <img src="assets/kiln-update.svg" alt="kiln update: a framed list of what is new in each release crossed, read from kiln's changelog" width="680">
</p>
<p align="center"><i>What <code>kiln update</code> shows as it crosses a release, read from kiln's changelog.</i></p>
