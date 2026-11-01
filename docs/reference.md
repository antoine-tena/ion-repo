# ion-repo reference

> **kiln is now ion-repo** (31 October 2026), the repo tool of the Ion family: the command is `ion-repo`, typed `ion repo …`; the package `ion-repo` on PyPI; the Claude Code plugin `repo` (skills `/repo:merge`…) in the `ion-repo` catalogue. kiln (the command, and the `kiln-cli` package) stays an alias for a while, which says the new name. `ion repo update` moves a project's old names: rules in `.claude/rules/ion-repo/`, skills `/repo:…`, `[REPORT-TO-ION-REPO]`, variables `ION_REPO_…` (`KILN_…` still read), plugins `repo@ion-repo`; `ion repo install --machine` moves the machine's kiln catalogue to `ion-repo`.

Everything ion-repo offers, at the release it is: every command and option, every setting, the
reusable workflows and the Claude Code plugins. The [README](../README.md) shows what ion-repo is
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
  <img src="assets/kiln-home.svg" alt="kiln's welcome screen: a pixel-art ion-repo above its commands, grouped by project, day to day, the grid and all repos" width="620">
</p>
<p align="center"><i><code>ion-repo</code> on its own: every command, grouped by what you are doing.</i></p>

`ion-repo <command> --help` (or `-h`) draws a command's options the same way: the banner, a short usage line (`ion repo new [options] [directory]`), its arguments and options. `ion-repo --version` (or `-V`, `-v`) prints the version.

| Command | What it does |
|---|---|
| `ion repo new [dir]` | Questionnaire, generation, lockfiles, install, first commit on `main`, then `develop` where all work happens. Three questions (what you build, size, language), the rest by option: `--name`, `--title`, `--description`, `--type`, `--size`, `--backend`, `--frontend`, `--language`, `--owner`, `--team`, `--podman`, `--vps`, `--goal`, `--prod-url`; `--no-github` (local only), `--no-install`, `--template` (another source), `--all-questions` (the whole questionnaire). |
| `ion repo adopt` | Bring an existing repo that ion-repo did not generate to the level of `ion repo new` (`--template` for another source), on a work branch (`chore/ion-repo-adopt`, opened by ion-repo when run on `main`, `master` or `develop`): the template rendered with what ion-repo finds in the repo (the stack, from the marker files of `backend/` and `frontend/`, or of the root when the code lives there: a Vite app or a `manage.py` at the root, recorded as `frontend_dir = "."` or `backend_dir = "."` in the answers, which CI, hooks, rules, charter, Dependabot, `ion repo check` and `ion repo dev` follow; the size via `--size`; the owner, from the `origin` remote) and every file the repo lacks laid: `CLAUDE.md`, `.claude/rules/ion-repo/`, the size's `charter.toml`, pre-commit hooks, the CI calling ion-repo's workflows, `docs/backlog/`. Never overwrites a file: those the repo has, and its code folders, are recorded under `kept` in `.copier-answers.yml`, which `ion repo update` never writes either; the `.gitignore` gets the template's missing lines. Then the existing debt the charter finds. From then on `ion repo update` replays the template like in a generated repo; a repo adopted before 0.4.6 is completed by `ion repo adopt` again. |
| `ion repo publish` | Create the private GitHub repo and protect its branches, for a project generated without `gh`. |
| `ion repo install` | Set up a machine after a clone: tools, dependencies, `.env`, migrations, pre-commit. Outside a repo, or with `--machine`, ion-repo for the whole machine: the `ion-repo` command as a uv tool, the plugin catalogue and the `ion-repo` plugin at user scope (every Claude session), the machine's settings. Re-runnable: only what is missing is done. |
| `ion repo dev` | Run the project on the machine, in the background. The code you edit runs there, reloaded at each change: the stack's servers and the processes a folder's `Procfile.dev` lists (`worker: uv run celery -A core worker`, in foreman's format). A folder the stack does not serve, such as an adopted repo with Vite and Express at its root, runs the `dev`, `dev:*`, `server`, `serve` and `watch` scripts of its `package.json` (`start` when there is none of them), with the package manager its lock names, its dependencies installed first when `node_modules/` is missing or older than the lock. The stack's front goes through its lock's manager too: an adopted Nuxt app kept on npm runs `npm run dev`, not `pnpm dev`. What you never edit runs in podman: the `db`, `postgres` and `redis` services of the compose file, restarted with their data and waited for (health check) when a process outside the front needs them. A server whose port another process already holds is not started: ion-repo names that process, or the worktree whose `ion repo dev` holds it. A small project runs everything at once; from three processes on, ion-repo asks what to run (everything, as last time, the front alone, or one by one; the front alone reads its folder's `.env` and not its `.env.dev`, the full local stack's overrides, so it can run on a remote API), and `--only django,nuxt` answers without asking. Once each server answers, ion-repo shows where to open it and offers to follow the logs (Ctrl+C leaves them, the servers keep running). Then `ion repo dev status`, `ion repo dev logs [service]` (`-f`, `--follow`, to keep reading) and `ion repo dev stop`, databases included unless another worktree of the repo still runs on them; `ion repo dev` again shows what runs. `--foreground` keeps it in the terminal, output interleaved and prefixed by process in colour (`django │ …`), until Ctrl+C. `--containers` runs the whole stack in podman instead, as in production. In a repo ion-repo's stack does not serve, whose compose file runs the project's own services while ion-repo would run its `package.json` scripts, the terminal offers the compose services in podman or the scripts on the machine, the last answer kept as the default; outside a terminal the scripts run and the compose file is pointed to. Outside a terminal (a script, a Claude session), nothing is asked. |
| `ion repo check` | Ruff and mypy for each Python project, ESLint and type checks for the front, then `charter`; the test suites (pytest, Maven tests) only with `--tests`, the release runs them all (`ion repo ci`). Typing goes through `charter types` when the charter declares `[types]`; a Django backend's tests run on the throwaway PostgreSQL and Redis of the Django job of `ci.yml`, with its variables, as `ion repo ci` replays them. Missing or outdated `node_modules` are installed from the lockfile first, a venv moved with its repo reinstalled. A front's scripts run through the package manager that wrote its lock (`npm run lint` in an adopted npm repo, which pnpm would install over); a check the repo has no means for (a `lint` or `typecheck` script its `package.json` lacks, mypy neither its venv nor its `pyproject.toml` has) is named and skipped, not failed. |
| `ion repo set [key=value…]` | Show or change the repo's settings (see [Settings](#settings)); the repo is re-rendered. Outside a repo, or with `--global`, this machine's settings (`system`, `owner`, `team`, `code_dir`, `channel`, `statusline`, `ai_trailers` = whether Claude's commits and pull requests say Claude helped: `disclose`, the default and the answer to "choose for me" at the first `ion repo install`, or `never`, which empties Claude Code's `attribution` and makes the branch guard refuse a `Co-Authored-By: Claude`; `frozen_repos` = the repos of the code folder, by their path in it, that `ion repo update --all` leaves as they are, such as a witness repo kept at an old release on purpose); a key that only the machine has (`statusline`, `channel`, `system`, `code_dir`, `ai_trailers`, `frozen_repos`) goes there from a repo too. |
| `ion repo waive [RULE\|file]` | Waive an ion-repo rule (`--paths`, `--reason`), or freeze a generated file so `ion repo update` leaves it alone; `--renew` moves to the next tier (a week, a month, three months, six months); `--permanent` for a waiver with no deadline, `--upstream` to link the issue or PR opened on ion-repo. No argument: list the waivers. |
| `ion repo update` | Move to the latest ion-repo release (with a box listing what's new in each release crossed), compatible dependency upgrades, then checks. `--major`, `--no-template`, `--no-deps`. Run on `main`, `master` or `develop` with a clean tree, it opens its work branch itself (`chore/ion-repo-update`, dated when that one exists). `--rehearse` plays it on a throwaway clone first and only reports, the repo untouched. After the template, `ion repo fix`'s converters close what it leaves to the repo (actions and ion-repo's workflows pinned by SHA, digests), uncommitted like the rest; ion-repo's workflows pinned by SHA follow the next release without a conflict, then are pinned again. In an adopted repo (`ion repo adopt`), only what belongs to ion-repo moves: its names of 0.3 first (`charte.toml` → `charter.toml` with the repo's rule identifiers kept, the `charte` command of its hooks, the workflows `charte.yml`, `contrat-api.yml`, `securite.yml` and their inputs; the files whose own text still cites them are listed; a `docs/a-faire/` becomes ion-repo's `docs/backlog/`, `AF-NN` tickets turned `T-NN` with the same numbers), then the references to ion-repo's workflows, to the latest public release (ion-repo's `develop` on the `beta` channel), their inputs checked. Only a release of ion-repo updates a repo: a tool built from a checkout is refused, with the command that installs the release. A conflict the template leaves (marked `<<<<<<< before updating`) stops it right after the template, named, before the dependencies: resolve it, then `ion repo update --no-template`. |
| `ion repo tickets [PATH…]` | Write the repo's ticket IDs as `<repo>#T-NN` in `docs/backlog/` and `CLAUDE.md` (plus `PATH`s): shows the plan and what it leaves alone, writes on a yes, a second run changes nothing. `--dry-run`, `--yes`. `ion repo update` offers it. |
| `ion repo update --all` | Update every ion-repo repo in your code folder, one worktree each, merged only if checks pass (the checks run once the update is whole: a repo with nothing to take gets no branch, a template conflict is reported as such, to resolve in its worktree; a repo of `frozen_repos` is left as it is): one line per repo (✓ or ✗, the outcome, the duration), each repo's full output in a log under `~/.cache/kiln/update-all/`, named for a repo left to finish by hand; `--verbose` shows it all as it runs. `--all --rehearse`: each update on a clone, nothing touched, a summary per repo. |
| `ion repo status` | Branch, clean tree, template release (`v0.4.0 → v0.4.2` when behind), waivers, stack — for every ion-repo repo, then the most waived rules across them. |
| `ion repo version` | In ion-repo's own repo: latest public release, candidates (age, adopting repos, ready to promote), the number the next release should take and the planned tickets still open. `--minor` when the next one is a milestone. `ion repo version cut` cuts the release branch with a drafted changelog entry, then (once the entry is rewritten) runs the checks, waits for GitHub's CI and tags `-rc.N` only on green; `ion repo version promote` tags the ready candidate (green CI; `--urgent` skips the soak and the adopting repo), merges it into `main` and `develop`, and PyPI and the GitHub Release follow. |
| `ion repo grid [RULE-ID]` | The grid: the practices ion-repo holds as the best today, one small TOML file per rule, each with its why, its sources (checked and dated), its level (adopt, trial, assess, hold) and how it is detected and fixed. `--theme`, `--scope`, `--level` filter; a rule ID shows it in full, with how to waive it. |
| `ion repo score [PATH]` | Any repo, made by ion-repo or not, measured against the grid's scored rules in about a second, without a token: a score out of 100 and one per pillar (every rule that applies weighs the same; rules outside the repo's stacks, or with nothing to look at, are left out), the three gaps to close first, then each gap with its reason, where it is, its source and what closes it, and the score again at the end so that a long list does not scroll it out of sight. Waived rules (`kiln-waivers.toml`) are shown apart. What the files cannot say, the GitHub settings (the default branch neither force-pushed nor deleted, plus a linear history when the repo does not merge with merge commits; secret scanning and push protection; Dependabot alerts and security updates; private vulnerability reporting on a public repo), is read through `gh` when it is logged in with admin rights on the repo, each gap with the direct link to its settings page; ion-repo never reads, stores nor prints the token. Without that access these rules are left out and the score says the settings are unknown, never a failure. A read is kept a day (`~/.cache/kiln/forge/`) and skipped in CI, so a setting's detail stays on the owner's machine: the badge, a report to ion-repo and a CI log carry the score and the rule IDs alone. Files are read as they are: a source that is not UTF-8 is decoded (its byte order mark, then cp1252 or latin-1) and listed rather than read as empty, a binary file (a NUL byte in its first 8 KB) and a minified source (a line over 1,000 characters) are left out of the code rules. Coding without an agent is no fault: a rule about agent files (`AI-CONTEXT`) is out of the score, shown as advice only to a repo worked with one (a `.claude/`, `.cursor/`, `.codex/` or `.gemini/` folder), and a map of the repo counts wherever it is written (`README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md` as well as `CLAUDE.md` or `AGENTS.md`). Stacks the grid does not cover yet (Java, .NET, PHP, Go…), known by a manifest or by their sources alone, are named; when none it covers is found, the score says it rests on the universal rules only. So are known packages no rule covers yet (Celery, SQLAlchemy, React…) and the rules waived again and again. In a terminal, ion-repo then offers to tell ion-repo, showing the exact lines that would leave and nothing else (never code, a path or a private package name): one issue per gap on GitHub, a 👍 when it is already open, a prefilled link without `gh`; "never" holds for the repo, and a line told once is not offered again. `--all` lists every rule and location, `--json` the report (schema 1), `--badge` a README badge, `--online` refreshes end-of-life dates from endoflife.date and reads the GitHub settings again. Nothing is written in the repo. `--roadmap`: what no converter closes, for Claude Code, sure gaps first then the smallest, each with its why, its places (file and line) and its proof; an approximate detector's places are marked "to confirm", and a false positive is dismissed for good by a waiver on its path (`ion repo waive ID --paths FILE --permanent`). `--roadmap --write` turns the items into tickets of `docs/backlog/backlog.md`, once each. `--rule ID`: that rule only, failing while its gap is open (the proof `/repo:modernize` waits for). `--against REF`: what changed since a commit, the score and the rules closed and opened, in Markdown (what `score.yml` comments on a pull request). |
| `ion repo bot [PATH]` | kiln-bot's run, what the reusable workflow `bot.yml` calls: on the branch `kiln/bot`, started again from the last commit (refused when a person committed on it), `ion repo update` in an ion-repo repo (`--no-update` to skip it) then `ion repo fix` (`--no-workflows` leaves out the commits that write `.github/workflows/`, which `GITHUB_TOKEN` may not push); `--body FILE` writes the pull request's description (the score before and after, the why and points of each commit); nothing when nothing changed. Your tree is never touched. |
| `ion repo pause NAME` | Keep the place of the Claude Code session it runs in (`--next` for the next step), in `~/.local/state/kiln/sessions/`: the next session start, in any repo, lists it above the first prompt with its age and `claude --resume <id>`; it leaves the list once resumed or its branch deleted. Run by the skill `/repo:pause`. Without `NAME`, proposes names drawn from the work at hand (the branch, the backlog's tickets in progress, the last commit), each with its ready command. |
| `ion repo frame TOOL SKILL` | Print the two rules that frame an Ion tool's skill answer, `══ ◆ ion · <word> ═…═` and `═…═ /<word>:<skill> ══`, the tool named by its word whatever its plugin is called (`learn`, `ion-learn` and its old name `grog` all give `learn`), as wide as the terminal less 6 columns (Claude Code's bullet and code block padding). Claude's Bash has no terminal, so the width is read from the nearest ancestor process that has one (`/proc`, or `ps` on macOS), 80 columns without any (a cloud session); `--width` sets it. |
| `ion repo eval-skills` | In ion-repo's own repo: check that each skill of the `repo` plugin fires on the sentence meant for it, a thin wrapper over `claude plugin eval plugins/repo`. The cases live in `plugins/repo/evals/<case>/` (`prompt.md`: a user sentence tagged with its skill; `graders/`: a `tool_used: Skill` grader on that skill, or one that allows no skill at all for the should-not-fire cases tagged `none`). Each case is one Claude session on your own quota, so it locks what the defaults multiply: `--runs 1` (default 3), `--ablation none` (the default no-plugin arm doubles the sessions), `-j 1`, `--model opus` (Haiku does not choose its skills as Opus does), `--max-cost-usd` (2 by default), `--no-publish` (the report stays in `plugins/repo/evals/results/`, ignored by git). It runs the cases of the skills changed against `develop`, plus the `none` ones; `--skill NAME` (repeatable) or `--all` choose them. Before starting it prints the cases, the number of sessions and the command, then waits for `ok` typed three times at a terminal; without one (Claude's Bash) it refuses, so you run it yourself. `--dry-run` prints and stops. |
| `ion repo fix [PATH]` | Every gap a script can close, closed on a work branch `ion-repo/fix-<date>` by converters run in a throwaway worktree of the last commit (under `~/.cache/kiln/worktrees`, the installed `node_modules` linked and the `.env` copied for the checks): your tree, uncommitted changes included, is never touched and only the branch remains; a second run the same day takes over its branch when it holds only `ion repo fix` commits, otherwise opens `ion-repo/fix-<date>-2`, one commit per rule with its why and source. The repo's own checks run on the whole repo before and after each converter (`ion repo check --all` in an ion-repo repo, otherwise the lint, type and test commands its manifests declare, at the root and one folder down: ruff, mypy, pytest or a Django project's `manage.py test`, the `lint`, `typecheck` and `test` scripts of a `package.json` run by npm, pnpm, yarn or bun after its lock), each with a 10-minute timeout. Each check runs once before the first converter: one whose tool is missing (named, with how to install it), already red or timed out cannot judge and the summary says which and why; the green ones judge every converter, named in each commit (`Checked: …`). Each commit is proven: the rule's detector runs again (`fixed` when it passes, `partial` when a gap is left for judgment), the whole grid is compared before and after (a converter that turns another rule red is undone, a converter bug), and any error of a converter puts the tree back and the run goes on (`converter bug`). A converter that turns the checks red leaves the batch, never merged red, never dropped: its commit waits on a branch of its own (`ion-repo/fix-<date>-<rule>`), the failing output kept in the git folder, where `ion repo score --roadmap` hands the gap to Claude with its log and the branch. A rule a converter brings into play (the audit a new CI needs) joins the run. Each commit gives the points it won (`Score: 62 → 65 (+3)`), and so does the summary. A converter that touches a `Containerfile` or a `Dockerfile` also builds its image with podman (or docker): one that no longer builds is undone like a red check, unless it did not build before either. A repo with no check found is fixed anyway, each commit marked "unverified: no check found" (or with why none of its checks can judge). mypy checks the `files` its config names, `.` when it names none. Converters: actions pinned by SHA with their exact version in a comment, update cooldown, Dependabot for every ecosystem found (composite actions included), read-only workflow tokens, gitleaks, a minimal CI, the lint, tests and dependency audit (`uv audit`, pip-audit, `pnpm audit` or `npm audit`, also every Monday) an existing GitHub CI lacks as workflows of their own, an outsider's text (`${{ github.event.issue.title }}`) moved out of `run:` into the step's `env:`, a tracked `.env` taken out of git (left on disk, ignored, its keys in an `.env.example`; its secrets stay in the history, to rotate), obsolete backports removed, requirements files alone turned into a uv project (`pyproject.toml`, `uv.lock`, the `requirements` exported back from it), loose requirements compiled to exact versions by uv otherwise, ruff set up with its safe fixes, `@ts-expect-error`, images pinned by digest, Debian 13, a non-root user, compose services hardened (read-only filesystem, no new privileges, capabilities dropped) where each still starts under podman with it (built and started on a throwaway copy, at most 10 minutes, under a progress line), the others named and left as they were, runtimes moved off their end of life. The compressor (rules `DEAD-CODE` and `UNUSED-DEPENDENCIES`, out of the score while in trial) runs only when named: `ion repo fix --rule DEAD-CODE` removes the functions, classes, methods and files nothing calls (vulture, knip), `--rule UNUSED-DEPENDENCIES` the dependencies nothing imports (deptry, knip). Guards keep what a static tool cannot see (a framework's conventions and decorators, an override, a name in a template, a string or a config, code the tests ran, a plugin loaded by its entry points, tests and configs; security, parsing, time zones and text encoding are never touched); each removal is then proven in steps, the type checker then the tests compared one by one with a run before anything was removed, by batches split in halves until the one that breaks stands alone and stays. Without a passing test, nothing is removed. Those that need the network say so before starting. `--dry-run` shows the plan and the diff, nothing written; `--rule ID` for one rule. Ctrl-C stops it cleanly (throwaway copies and containers removed, the commits already made kept on the branch, exit code 130). Ends with the score before and after, and the points of each rule. `ion repo update` runs the same converters after the template, in place, left uncommitted with the template's changes for review, frozen and kept files untouched. |
| `ion repo doctor` | Check the machine (git, uv, gh login, pnpm, podman, Java, pre-commit, ion-repo release, Claude plugin) and the current repo (a venv moved with its repo, `node_modules` behind the lockfile); each problem comes with the command that fixes it. Changes nothing. |
| `ion repo ci [commit]` | Replay the repo's GitHub CI locally against throwaway PostgreSQL/Redis, and push the verdict as a git note (`--skip <job>`, `--no-push` to keep the note local, `--keep` the commit's worktree, `--status` for the verdict only). A private repo runs its CI this way by default (`ci_runner: local`): no GitHub minutes spent; a public one runs on GitHub, free. `ion repo set ci_runner=github` switches. |
| `ion repo contract` | Django + Nuxt: export `openapi.json` (ion-repo's `export_openapi`, otherwise drf-spectacular's `spectacular` in a DRF repo ion-repo did not generate) and regenerate the front's API types (`pnpm generate:api`, skipped and said when the front has no such script). |
| `ion repo completion [bash]` | Print a bash completion script (bash by default, the only shell for now) built from the parser; enable it with `eval "$(ion-repo completion bash)"` in `~/.bashrc`. |
| `charter` | Check the repo against its `charter.toml` (`--detail`, `--unverified`, `types`, `coverage`, `file <path>`); `charte` is its former name. |

When a newer ion-repo release is out on the machine's channel, a command typed in a terminal ends by offering to install it (GitHub asked at most once a day; after a no, the same release comes back a week later). Not in Claude Code, whose session start asks instead, not in `ion repo doctor`, not for a tool installed from a checkout; `ION_REPO_NO_UPDATE_CHECK=1` turns it off.

Release channel of the machine (`ion repo set channel=…`): `public` (promoted releases, the default), `internal` (candidates too) or `beta`, for ion-repo's own development: the tool runs ion-repo's `develop`, ion-repo's checkout, in the code directory, one of its folders or one level further, installed editable (`uv tool install --force --editable ~/code/kiln`), so a merge into `develop` is live at once, without a release; `ion repo update` takes the template at the tool's pushed commit.


<p align="center">
  <img src="assets/kiln-grid.svg" alt="ion repo grid: the rules ion-repo stands behind, by theme, each with its level" width="680">
</p>
<p align="center"><i><code>ion repo grid</code>: the rules ion-repo stands behind today; <code>ion repo grid &lt;ID&gt;</code> shows one in full, as in the README.</i></p>

## Settings

Every answer of the template, shown by `ion repo set` and changed by `ion repo set key=value` (the repo
is re-rendered, on a work branch: `chore/ion-repo-set`, opened by ion-repo on `main`, `master` or `develop`):

| Key | What it sets |
|---|---|
| `name`, `title`, `description` | Short name (packages' prefix), displayed title, one sentence. |
| `project_type`, `size` | What you build (`app`, `api`, `site`, `dashboard`, `analysis`, `cli`) and how big the stakes are (`tiny`, `small`, `medium`, `large`): the stack and the rules follow. |
| `backend`, `frontend`, `podman` | The stack (see [What you get](../README.md#what-you-get)) and podman containers. |
| `language`, `language_comments`, `language_commits`, `language_docs`, `language_tickets`, `language_ui` | The team's language, and per use when they differ. |
| `owner`, `team` | GitHub account owning the repo, and the team's logins (reviewers). |
| `claude_plugin` | A command-line tool that ships its own Claude Code plugin: `plugins/<plugin_name>/` (manifest, a first `run` skill to replace), its catalog `.claude-plugin/marketplace.json`, a test that Claude Code would load it, and the plugin enabled in the repo's sessions from its GitHub repo at `main`. Elsewhere: `claude plugin marketplace add <owner>/<name>`. |
| `plugin_name` | The name of that plugin, what its skills are typed with (`/<plugin_name>:…`). By default the project's name without the `ion-` prefix of the Ion family: `ion-host` ships the plugin `host`, `/host:domain`, in the catalog `ion-host`. A new `name` or `plugin_name` moves the package's folder (`backend/<package>/`) and the plugin's, each file merged at its new path: what the project removed stays removed, its own files follow, and what cites the old names (imports, paths, skills, the name in the code and the text) is rewritten; a kept `pypi_name`, folder paths, URLs and file names (`ion-host.toml`, which the projects using the tool may hold: the update lists them, to rename by hand with the old name read as a fallback) stay, and a one-word name follows only when quoted or in a code span. |
| `pypi_name` | A command-line tool published on PyPI under this name (the command keeps the project's name): `.github/workflows/pypi.yml` builds and publishes it at each release tag `vX.Y.Z`, its version taken from the tag, with build provenance on a public repo; it publishes with the PyPI token in the secret `PYPI_TOKEN` of the `pypi` environment (`/repo:token`), otherwise through trusted publishing (the publisher declared once at https://pypi.org/manage/account/publishing/: repository, workflow `pypi.yml`, environment `pypi`). Empty, the default: not published. |
| `java_package` | Root package of the Java sources. |
| `timezone` | Time zone of the project's calendar notions (dates are stored in UTC). |
| `serena` | Serena for Claude Code (symbol navigation on big codebases). |
| `compact_window` | Claude Code's sessions: the context size, in tokens, at which a conversation compacts (`400000` by default, as every message re-reads the whole context; `1000000` keeps Claude Code's own; `claude --autocompact 1M` lifts it for one launch). |
| `deploy`, `vps_host`, `api_domain`, `vps_port`, `vps_db_port`, `site_url`, `deploy_branch`, `frontend_deploy` | Production: a hardened VPS (SSH host, API domain, the API's and the database's ports on 127.0.0.1 for a server shared with other projects, site address, deployed branch) for a Django backend, or for a Streamlit or Dash front alone (its image behind Caddy, no database), and a Nuxt front on Vercel. |
| `north_star` | The goal that orders the priorities of `docs/backlog/`. |
| `ci_runner` | Where the CI of a release branch runs: `local` (`ion repo ci`, no GitHub minutes, a private repo's default) or `github` (free for a public repo). |
| `update_bot` | kiln-bot: `off` (the default: a private repo pays its GitHub minutes), `weekly` or `monthly`; see [kiln-bot](#kiln-bot). |
| `statusline_ci`, `prod_health_url` | Claude Code's status line: CI state, and production's health probe. |
| `large_files` | Heavy files the repo keeps on purpose (a site's film), by their exact path from the root, as a list or `a,b`: pre-commit's 1 MB ceiling (`check-added-large-files`) lets them through, and only them. |

## What a generated repo holds

- **Opinionated tooling, no `pip`, no `docker`:** uv for Python, pnpm for JavaScript, podman
  for containers; ruff, mypy (strict), pytest + coverage floor, ESLint, pre-commit (which also
  refuses commits on `main`/`develop`).
- **CI on GitHub Actions** that calls ion-repo's reusable workflows — so fixing CI once in ion-repo
  fixes it everywhere. They are pinned to the release's commit SHA, its tag in a comment, and
  the workflow token only reads the repo.
- **A repo that passes ion-repo's own grid:** `ion repo score` gives a new project 100 (once `ion repo new`
  has locked its dependencies; a front with no backend still lacks a test). Dependabot for each
  ecosystem, weekly, after a 7-day cooldown; container images on Debian 13 pinned by digest;
  compose services read-only, every capability dropped, with health checks.
- **A project size** (`tiny` → `small` → `medium` → `large`) that tunes defaults: a weekend
  script doesn't get the same ceremony as a multi-team service.
- **Agent-ready instructions:** ion-repo's rules for Claude in `.claude/rules/ion-repo/`, with stable
  rule IDs the `charter` engine can check; each stack's rules load only when Claude touches its
  files. The root `CLAUDE.md` belongs to the project. `.claude/` is laid out one way everywhere:
  `settings.json`, `skills/`, `rules/`, `hooks/` (their scripts) and `plans/` (plan mode's
  plans, `plansDirectory`) are committed; `settings.local.json`, `worktrees/`, `memory/` and
  `sessions/` stay on each machine, ignored by git.
- **Optional production setups:** a hardened VPS deployment for Django (Caddy with automatic
  TLS, read-only containers, one image per commit, automatic rollback, daily backups with
  restore tests) and Vercel deployment for Nuxt fronts.
- **A backlog** (`docs/backlog/`: typed `<repo>#T-NN` tickets by priority) that Claude Code's status line counts.

## Reusable GitHub workflows

ion-repo's workflows work from any repository, ion-repo-generated or not:

```yaml
jobs:
  backend:
    uses: antoine-tena/ion-repo/.github/workflows/django.yml@v0.4.12   # an ion-repo release tag
```

`django.yml`, `python.yml`, `maven.yml`, `pnpm.yml`, `charter.yml`, `security.yml` (`uv audit`,
`pnpm audit`, OSV-Scanner for Maven), `secrets.yml` (gitleaks), `api-contract.yml`, `infra.yml` (podman build,
actionlint, shellcheck), `sbom.yml` (CycloneDX), `mutation.yml` (mutmut), `vercel.yml`, `bot.yml` (kiln-bot) and `score.yml` (the score's change on a pull request). `charte.yml`,
`securite.yml` and `contrat-api.yml` are their former names, kept as relays. Databases for tests run in
podman. See [`.github/workflows/`](../.github/workflows/).

### kiln-bot

The grid's fixes as one pull request, on a schedule ("Dependabot for your methods"). Paste this
in any repo:

```yaml
# .github/workflows/kiln-bot.yml
name: kiln-bot
on:
  schedule:
    - cron: "0 6 * * 1"
  workflow_dispatch:
permissions:
  contents: read
jobs:
  bot:
    permissions:
      contents: write
      pull-requests: write
    uses: antoine-tena/ion-repo/.github/workflows/bot.yml@v0.4.12
    secrets:
      token: ${{ secrets.KILN_BOT_TOKEN }}  # optional, see below
```

Every run starts the branch `kiln/bot` again from the default branch: `ion repo update` in an ion-repo
repo, then `ion repo fix`, each commit proven, and one pull request kept up to date with the score
before and after and the why of each commit; closed when nothing is left to propose. The catch:
a pull request opened with `GITHUB_TOKEN` does not start the repo's CI. Create a
[fine-grained token](https://github.com/settings/personal-access-tokens/new) on that repo only,
with *Contents*, *Pull requests* and *Workflows* set to read and write, and save it as the secret
`KILN_BOT_TOKEN` (or use a GitHub App's token). Without it, kiln-bot still runs, but
`GITHUB_TOKEN` may never push `.github/workflows/`: the commits that write there are left out and
named in the pull request, and the repo must allow it in *Settings*, *Actions*, *General*: "Allow
GitHub Actions to create and approve pull requests". `score.yml`, called `on: pull_request`, comments
on each pull request what it changes in the score (the rules it closes and opens); a fork's pull
request gets it in the run's summary only. In a generated repo: `ion repo set update_bot=weekly` (or
`monthly`).

## Claude Code plugins

ion-repo is also a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace; `ion repo install`, outside a repo, adds it and enables `ion-repo` for every session, or by hand:

```sh
claude plugin marketplace add antoine-tena/ion-repo
claude plugin install repo@ion-repo
```

| Plugin | What's inside |
|---|---|
| `repo` | Skills for the git workflow (`worktree`, `merge` = into `develop`, and in a repo that ships a Claude Code plugin, the installed plugin updated after the push in the scopes where it is installed, then Claude Code to restart, `release`, `cleanup`, `review` = a branch's commits before they go public, and the whole repo before a release, `backlog`, `update` = self-update, `adopt` = bring an existing repo under ion-repo, `resize` = move a repo up or down ion-repo's sizes, what the new size brings or removes shown before the merge, `modernize` = the gaps of `ion repo score --roadmap` closed one at a time, tests first, each proven by `ion repo score --rule`), `report` (an ion-repo defect met in your repo becomes an issue or a PR, posted once you approve), `contribution` (an outside contributor's PR handled like a well-run open-source project: untrusted code read before anything runs, triage, review, a merge that credits them, nothing posted without your yes), `good-first-issues` (a small, steady stock of `good first issue` issues drawn from your backlog and reserved for newcomers, refilled as they get merged), `token` (a service token pasted once into a git-ignored `.<service>/` folder, never shown), `prompt` (a clean prompt, ready to paste, for a Claude Code session, a subagent, a system prompt or another model: the goal and why, the context this session holds, constraints, when it is done, the output expected) and `pause` (the session's place kept before leaving it: its name, where it stopped, the next step, listed above the first prompt of the next session in any repo with `claude --resume <id>`, until resumed or its branch deleted, by `session_start.py` through `paused.py`); the `debrief` output style (`output-styles/debrief.md`, shown as `repo:debrief`), forced in every session where the plugin is on: the message that closes a piece of work opens with one bold sentence giving the real git state (merged, pushed, worktree removed, or committed on the branch, not merged), then **◆ Summary** (the three points that matter, a departure from the request always among them), **◆ Not working** (`Broken:` or `Not verified:` lines, or "nothing known" and what was checked), **◆ Next** (at most three actions Claude can take, the first `← recommended`, one `ok` starts it) and **◆ Your turn:** (only what Claude cannot do, its command in one `bash` block), titles in the user's language, each line opening with its keyword, no diff nor file list; Claude writes freely when the format falls short, often for a long output; the skills that used to sum up in their own way (`merge`, `release`, `cleanup`, `review`, `update`, `adopt`, `/vps:deploy`) point to it; being forced, it replaces any `outputStyle` chosen in your settings or with `/output-style` (Claude Code reads the forced style first and the setting not at all; with several forcing plugins, the first loaded wins), and disabling the plugin gives your style back; hooks that guard protected branches and files (`branch_guard.py`, `protect_files.py`), refuse a `Claude-Session:` line in a commit message, and a `Co-Authored-By: Claude` on a machine set to `ai_trailers=never`, check each edited file (`check_file.py`), and ask at session start (`session_start.py`, which also has the answer of any Keramos tool's skill framed by the two double-line rules `ion repo frame <tool> <skill>` prints at the terminal's width, `══ ◆ keramos · <tool> ═…═` above and `═…═ /<tool>:<skill> ══` below, each in a plain code block, with ion-repo's logo and what's new above the first prompt, `first_prompt.py`; a session started outside any repo, in `~` or `~/code`, gives Claude the repos below it, and Claude says in one line, with the command that restarts there, when a task belongs to one of them, since a repo's `.claude/settings.json` (its plugins, permissions and env) loads only from the launch folder, `place.py`; another session still running and at work on the same repo in the last ten minutes, worktrees included, is told to Claude at start and resume, which asks you whether to go on, `others.py`; a red integration branch is told to Claude, a run GitHub never started apart from a failure of the code): ion-repo updates in ion-repo repos, adoption in your other repos ("Yes", "Later", "Never for this repo"), all paced by one goodwill score that each yes raises and each no lowers (`reminders.py`); a shared status line in four styles, redrawn every 5 seconds (`ion repo set statusline=…`, or `none` / `custom` to keep your own) that shows the context in tokens, its colour rising with what each message costs, in red once the prompt cache has expired (the next message writes it all again); condensed command output with [rtk](https://github.com/rtk-ai/rtk) (`rtk.py`). |
| `debrief` | The `debrief` output style of `repo` alone, forced the same way, without its skills, hooks or status line: for a machine that wants the end-of-work report and keeps its own git habits (`claude plugin install debrief@ion-repo`). |
| `kiln` | The `repo` plugin under its old name, kept for the machines still moving from kiln (the update command of kiln 0.4.10 installs `kiln@kiln`); `ion repo install --machine` replaces it by `repo@ion-repo`. Install `repo`. |
| `django` | Skills `migration`, `regen-api` (API types regenerated) and `postgres-read` (read-only PostgreSQL MCP). |
| `nuxt` | Skills `nuxt`, `vue-best-practices`, `vue-testing-best-practices`, `vitest`, `polish` (UI polish) and `preview` (screenshots on three phones and a desktop, Playwright MCP). |
| `vps` | Skills `deploy`, `prod-logs` (read-only diagnosis) and `prod-dump` (production copied into a throwaway database). |
| `stripe` | Stripe MCP in test mode. |
| `serena` | Read-only [Serena](https://github.com/oraios/serena) MCP for symbol navigation in big repos. |

Generated repos enable the right plugins for their stack automatically.

## Releases

ion-repo is used daily on a handful of real repos, including one in production. It is young, so it
numbers releases like Claude Code does: in `0.x`, every release bumps the patch, breaking changes
included (`0.4.1 → 0.4.2`), listed first in the release notes and migrated by `ion repo update`; the
minor only moves for a milestone. Strict semver starts at 1.0. Each release is first a candidate
(`v0.4.2-rc.1`) used on the author's own repos; it is promoted to `main` (`v0.4.2`) only once
it has soaked (24 hours since its tag and at least one repo updated to it; 2 hours, no repo
required, for a candidate of fixes only), its CI green (macOS and end-to-end tests included) and its update
rehearsed on a copy of each repo, so a release never needs an emergency fix. A promoted release
reaches PyPI (`uv tool install ion-repo`) and the Homebrew tap (`brew install
antoine-tena/ion/ion-repo`, then `brew upgrade ion-repo`; from the old `kiln` formula, Homebrew first asks for `brew trust antoine-tena/kiln`, then `brew upgrade kiln` follows the rename). `kiln-cli` and `keramos-kiln` had their last release at v0.4.11:
at its first run as a uv tool each installs `ion-sh` and `ion-repo`, removes itself and moves the Claude
Code catalogue; a failure leaves it working and prints the command that finishes. Projects are generated and updated from the latest release, pin ion-repo's workflows to
that exact tag, and `ion repo update` shows what changed in each release it applies (see
[`CHANGELOG.md`](../CHANGELOG.md)).
Linux, WSL and macOS are supported.

<p align="center">
  <img src="assets/kiln-update.svg" alt="ion repo update: a framed list of what is new in each release crossed, read from ion-repo's changelog" width="680">
</p>
<p align="center"><i>What <code>ion repo update</code> shows as it crosses a release, read from ion-repo's changelog.</i></p>
