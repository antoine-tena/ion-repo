# What's new in kiln

One entry per release, the most recent first: `## vX.Y.Z — date`, then one line per visible
change (`- …`), breaking changes first (`**Breaking**`). `kiln update` shows the entries of the
releases a project crosses; `kiln version cut` drafts the entry of the release it cuts, on the
`release/vX.Y.Z` branch, rewritten before its first candidate. Names are those of their release:
entries before v0.4.0 quote kiln's former French names.

## v0.4.8 — 2026-10-26
<!-- readme: unchanged: a fix, no new command nor option -->
- `kiln install`, `kiln check`, `kiln dev` and `kiln update` no longer fail with `ERR_PNPM_IGNORED_BUILDS` in a front whose `pnpm-workspace.yaml` does not list its dependencies' build scripts under `allowBuilds` (pnpm 11+): those scripts are skipped, as in generated repos, and pnpm names them.

## v0.4.7 — 2026-10-26
<!-- readme: unchanged: a fix, no new command nor option -->
- `kiln install` and `kiln check` no longer fail with `ERR_PNPM_NO_LOCKFILE` in a repo whose front has no `pnpm-lock.yaml`: pnpm installs without `--frozen-lockfile` and creates the lockfile, to commit.

## v0.4.6 — 2026-10-24
- `kiln adopt` brings an existing repo to the level of `kiln new`: `CLAUDE.md`, the Claude rules, the size's charter, pre-commit hooks, the CI calling kiln's workflows and the backlog, for the stack it finds in `backend/` and `frontend/`. Nothing the repo has is overwritten: those files, and its code folders, are kept under `kept` in `.copier-answers.yml`, and `kiln update` then keeps the repo current like a generated one (#59).
- **After updating**: in a repo adopted before 0.4.6, run `kiln adopt` again on a work branch to lay the rest of the template; until then `kiln update` only moves its workflows' tag.
- A Vite + React front, for `kiln new --frontend vite-react` and for adoption: Vite 8, React 19, Tailwind, Vitest, strict `tsc`, its Claude rules and CI.
- A Streamlit or Dash front deploys to your own server with `deploy=vps`: its image behind Caddy (websockets included), switched and rolled back by `scripts/ops/deploy-frontend.sh`, no database to run (#43, thanks @darnak69).
- Data projects tie committed trained models to their code: a manifest per model (code hash, seed, dataset, metrics), tests that fail when the code moved on or the metrics drop, and the grid rule `MODEL-TRACED` (#44, thanks @darnak69).
- `kiln score` names what the grid does not cover yet (Celery, SQLAlchemy, React…) and the rules waived again and again, then offers, in a terminal, to tell kiln with exactly those lines: one issue per gap, a 👍 when it is already open (#42, thanks @darnak69).
- `kiln dev` refuses to start a server whose port another process holds, and names that process or the worktree running it (#60); it installs a folder's missing Node dependencies before running its scripts.
- The tool update moves the kiln plugin to its new version too, instead of leaving the old one installed (#58, thanks @NathanBarrachin).
- An adopted repo runs the dev scripts of a `package.json` the stack does not serve, and follows kiln's `develop` on the beta channel; pnpm's postinstall runs even when an install has nothing to add; the grid counts `.test.tsx` files as tests.

## v0.4.5 — 2026-10-23
- Generated repos run GitHub's CI only on `release/**` branches (and by hand), no longer on each push: a merge into `develop` runs the fast linters on the files it changed, the release runs everything. `kiln check` looks at the branch's changed files only. `kiln update` brings the new `ci.yml`.
- Claude Code sessions stay cheaper: generated repos compact at 400k tokens (`kiln set compact_window=…`) and leave claude.ai connectors to each person; the status line shows the context in tokens, turns it red once the prompt cache has expired, and refreshes every 5 seconds; `/kiln:merge` suggests `/clear` only when it saves something.
- `kiln fix --rule DEAD-CODE` and `--rule UNUSED-DEPENDENCIES` (trial rules, out of the score): dead code and unused dependencies removed, each removal proven by the repo's checks.
- kiln installs with Homebrew: a formula is pushed to the tap at each release, every package pinned by its hash.
- `kiln dev` offers the front alone, on its own `.env`; `.env.dev` overrides `.env` on the machine.
- `kiln update` turns an adopted repo's `docs/a-faire/` into its backlog, as in generated repos.
- `kiln dev` sees a server listening on IPv6 only, such as Nuxt on macOS (#54, thanks @NathanBarrachin).
- `kiln check` and `kiln install` no longer crash in a repo without `backend/.env.example` (#55, thanks @NathanBarrachin).
- `kiln install` installs pre-commit's hook only when the repo has a `.pre-commit-config.yaml`, so commits keep working in an adopted repo (#56, thanks @NathanBarrachin).
- `kiln install` without Claude Code installed no longer fails on the plugin catalogue: the status line waits for the next run.
- A Streamlit or Dash front can no longer be deployed to Vercel, and nothing generated cites a deployment that does not exist (part of #43).
- Fixes: a waiver limited to paths lifts a rule that scans the whole repo (#57); `kiln set` keeps a value such as `a : b` as text, stops on conflicts, and a machine-only key set in a repo goes to the machine; `kiln doctor` gives the right install hint on macOS; no `kiln update` offered when the integration branch already has it; new generated files are exempt from the charter; containers of a killed `kiln check` are removed.

## v0.4.4 — 2026-10-21
- **Breaking**: `kiln check` no longer runs the test suites (pytest, Maven tests): lint, types and charter only, so a merge stays fast; `kiln check --tests` runs them, and the release runs them all (`kiln ci`). Nothing to convert.
- **Breaking**: `kiln dev` runs in the background and gives the terminal back once each server answers; `--foreground` keeps the old interleaved output until Ctrl+C. Nothing to convert: a script that relied on it adds `--foreground`.
- `kiln dev` runs the code you edit on the machine and what you never edit in podman: the compose's `db`, `postgres` and `redis` are restarted with their data and waited for (health check) before the servers, and before `kiln check` and the migrations of `kiln install`. A folder's `Procfile.dev` adds processes, one `name: command` line (a Celery worker, a scheduler). From three processes on, a terminal asks what to run (everything, as last time, or one by one) and `--only django,nuxt` answers without asking; then kiln offers to follow the logs. `kiln dev status`, `kiln dev logs [service] [-f]` and `kiln dev stop`, which keeps the databases another worktree of the repo still uses. `--containers` finds the compose where it is (`config/local/compose.yml`).
- A Django project under podman develops on its compose's PostgreSQL, as in production, on a port drawn from its name: two projects never fight over 5432.
- Every Claude Code session, after `/clear` and compaction too, is reminded to ask whether a failure comes from kiln, even when it shows up elsewhere, and to fix it in kiln or report it with `/kiln:report` ([REPORT-TO-KILN]).
- `kiln score --roadmap`: the gaps no converter closes, sure ones first, each with its why, its places and its proof; `--write` turns them into backlog tickets, `--rule ID` proves one closed, and the `/kiln:modernize` skill works through them, tests first, one commit per gap. A waiver with paths dismisses a false positive for good.
- Generated repos pass kiln's own grid: actions and workflows pinned by SHA, Dependabot with its cooldown, read-only workflow tokens, images by digest on Debian 13, non-root hardened compose services, OSV-Scanner for Maven.
- `kiln install` outside a repo (or `--machine`) sets up kiln for the whole machine: the command, the plugin and its settings. A command typed in a terminal offers the newer release of the machine's channel, at most once a day.
- `kiln update` moves an adopted repo off kiln's 0.3 names (`charte.toml`, the `charte` command, the old workflows and their inputs), keeping its own rule identifiers.
- `kiln check` runs as the CI does: Django tests on the CI job's throwaway PostgreSQL and Redis, mypy through `charter types` when the charter declares it, pnpm dependencies installed as the lockfile says, a venv moved with its repo reinstalled.
- `kiln score` names the stacks it only knows by their sources (.NET, Java, PHP) and says when the score rests on universal rules only.
- Fixes: a hardened Astro container starts; the status line knows a front deployed by the Vercel CLI; `kiln fix --dry-run` accepts a tree with changes.
- **After updating**: in a Django project under podman, copy the DATABASE_URL line of backend/.env.example into backend/.env to develop on the compose's PostgreSQL.

## v0.4.3 — 2026-10-20
- `kiln fix`: every gap a script can close, closed on a work branch `kiln/fix-<date>`, one commit per rule with its why and source. Your checks run before and after each converter; one that turns them red is undone and reported, and a repo without tests is fixed anyway, each commit marked unverified. `--dry-run` shows the plan and the diff, `--rule ID` takes one rule, and the score before and after closes the run.
- Fourteen converters to start: actions pinned by commit SHA, a 7-day cooldown on updates, Dependabot for every ecosystem found, read-only workflow tokens, gitleaks, a minimal CI, obsolete backports removed, loose `requirements.txt` compiled to exact versions by uv, ruff with its safe fixes, `@ts-expect-error`, images pinned by digest, Debian 13, a non-root user, Node and Python moved off their end of life. Those that reach the network say so first.
- Fixes: `kiln version cut` no longer tags a release whose cut stopped on a conflict before its changelog entry was drafted; the README's `kiln update` image is drawn from the right notes.

## v0.4.2 — 2026-10-20
- `kiln score`: any repo, made by kiln or not, measured against the grid in about a second, offline and without a token. A score out of 100 and one per pillar, the three gaps to close first, then each gap with its reason, where it is, its source and what closes it; waived rules shown apart, stacks the grid does not cover listed at the end. `--all`, `--json` (schema 1), `--badge` for a README, `--online` for fresh end-of-life dates.
- Grid v1: 40 scored rules, up from 6. CI and workflows (token permissions, untrusted input in scripts, `pull_request_target`, tests, linter, vulnerability audit, secret scan), containers (images by digest, current Debian, hardened compose services, health checks), Django settings (`DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`), Python and TypeScript standards, runtimes past their end of life. Each one sourced and dated, and run on two real repos for false positives: those that can flag wrongly are `review` or `ratchet`. A `requirements.txt` pinned to exact versions now counts as locked.
- `kiln dev` runs a Java API next to its front.
- The session start no longer calls a CI red when GitHub never started its jobs (billing, spending limit): it says there is nothing to fix in the code, and that `kiln ci` replays it on the machine (#45, thanks @NathanBarrachin).
- `kiln update` from 0.3 keeps the outline of the instructions it carries over: their headings sit under the carried-over part, and a line added to a generated section keeps its heading (#46, thanks @NathanBarrachin).
- Fixes: generation is one line in a terminal like every other step; a long panel line wraps instead of being cut; release notes show code in colour; `kiln version cut` redraws the README's images of the release.

## v0.4.1 — 2026-10-19
- A private repo's CI runs on the machine: new answer `ci_runner` (`local` for a private repo, `github` for a public one, picked from the repo's visibility by `kiln update` when missing). In `local`, `ci.yml` has no push trigger (no GitHub minutes spent), `/kiln:merge` replays it with `kiln ci`, and the status line and the session start read its verdict; `kiln set ci_runner=github` brings it back on each push.
- `kiln grid`: the practices kiln holds as the best, one small TOML file per rule, each with its why, its sources checked and dated, its level (adopt, trial, assess, hold), its regime and how it is detected. Six rules to start (lockfiles, pinned actions, dependency updates and their cooldown, non-root containers, no committed `.env`), and 105 assessed drafts drawn from the reference repo (`kiln grid --level assess`).
- In a repo brought under kiln by `kiln adopt`, `kiln update` moves the references to kiln's workflows to the latest public release, after checking each input against the workflow at that tag; `kiln adopt` does it at adoption, and `kiln status` shows the tag an adopted repo quotes.
- `kiln new` says when a stack is frozen: Django and Nuxt are complete, the other stacks stay generated and tested, without new grid rules for now.
- Both READMEs now describe everything kiln offers (every command and option, every `kiln set` key, plugin, skill, hook and reusable workflow), checked by kiln's tests at each change; `kiln version cut` moves the version they quote and refuses a release whose READMEs did not change. Generated repos get the same rule: the README follows each change in its branch.
- Fixes: `kiln version cut` carries the candidate still open into the next release; a deprecation now fails kiln's tests (an escape in `copier.yml` had slipped through).; `kiln dev` runs the API of a Java backend that has a front (its jar, rebuilt at each start), and every server it starts receives the `.env` of its folder

## v0.4.0 — 2026-10-19
- **Breaking**: kiln speaks English. `kiln update` converts a generated project in one go, and the names of 0.3 are still read until the next minor.
- **Breaking**: the template's questions are in English (`size`, `name`, `owner`, `team`, `project_type`…); `kiln update` hands Copier the new names and still reads the old answers.
- **Breaking**: the charter is in English: `charte.toml` becomes `charter.toml` (bans, ratchets, floors) and rules take English identifiers. `kiln update` rewrites the file with its budgets and the project's own rules, and the rule identifiers cited in waivers and in the code; an adopted repo keeps its `charte.toml`, read under its French names, and `charte` stays an alias of the `charter` command.
- **Breaking**: commands and options in English: `contrat` → `contract`, `set --poste` → `set --global`, `ci --sauter/--sans-pousser/--garder/--statut` → `--skip/--no-push/--keep/--status`; the old names still work, with a warning.
- **Breaking**: kiln's instructions for Claude move to `.claude/rules/kiln/`: the project and charter rules always loaded, each stack's rules only when Claude touches its files, production and browser security rules from the `ember` size on. The root `CLAUDE.md` now belongs to the project; `kiln update` carries over what the project added to the old one.
- **Breaking**: plugins renamed: `base`, `pile-django`, `pile-nuxt`, `vps-podman` become `kiln`, `django`, `nuxt`, `vps`, with English skill names (`/kiln:merge`, `/kiln:release`, `/kiln:cleanup`, `/kiln:review`, `/kiln:update`, `/kiln:adopt`, `/kiln:report`…). The catalogue moves existing installs to the new names, and the former hook and status line paths keep working.
- **Breaking**: reusable workflows `charter.yml`, `security.yml` and `api-contract.yml`, with English inputs; `charte.yml`, `securite.yml` and `contrat-api.yml` stay as relays, and the old inputs are still accepted. The `kiln ci` note starts with `kiln ci: success` or `kiln ci: failure`; notes of 0.3 are still read.
- **Breaking**: machine settings and status line styles in English (`channel=internal`, `plain`, `band`, `classic`…); the old keys and values are still read in `config.toml` and accepted by `kiln set`.
- `kiln new` in three questions (what you build, the size, the team's language), then the next steps; `--all-questions` for the whole questionnaire.
- Generated code, comments, scripts and workflows in English; what users read (pages, messages, README) follows the project's language.
- The hook after each edit checks the edited file alone (`charter file`, about 0.15 s), and says how to waive a rule; ratchets and floors run at commit and in CI.
- At session start, kiln's logo shows the new release and its main changes above a shorter update question.
- `kiln version cut` and `kiln version promote`: kiln's own release in two commands, with a GitHub Release for each promoted version.
- Only a release of kiln updates a repo: a kiln installed from a checkout ahead of its tag (or with changes, or from a branch) is refused by `kiln update`, `new` and `adopt`, with the command that installs the release, instead of mixing its code with an older template. `kiln --version` says what is installed, not what the checkout became since, and the session start replaces such a tool by the release.
- `kiln update --rehearse` plays the update on a throwaway clone with its checks and only reports, the repo untouched; `kiln update --all --rehearse` does it for every repo.
- At session start, Claude is told when the last CI of the integration branch is red, to say so before any new work.
- `/kiln:merge` runs the repo's checks before merging and reads GitHub's verdict on the merge.
- `kiln update` opens a ticket for what only the team can complete after an update (`After updating:` in a commit), and a backlog ticket can be reserved for one GitHub account.
- `kiln version cut` waits for GitHub's CI of the release branch and tags only on green; `kiln version` and `promote` hold back a candidate whose CI is not green; a fix of a candidate bumps the plugins it touches.

## v0.3.4 — 2026-10-16
- The template is never newer than the installed tool: `kiln update` applies the installed kiln release (conversions from one release to the next live in the tool), refuses to take a repo back to a release older than its own, and says when a newer release is out.
- `kiln new` without `gh`, or outside a terminal without a login, creates the project locally, and `kiln publish` creates the GitHub repository afterwards. The default owner comes from the machine's settings or from the account logged in to gh; a project without a team has neither CODEOWNERS nor a "Team" section.
- The generated CI looks for secrets through the `secrets.yml` workflow (gitleaks pinned and verified, without the license gitleaks-action requires for an organization); `kiln ci` replays it with the machine's gitleaks.
- `kiln` answers in 0.12 s instead of 0.5 s (commands imported on demand); the generated README installs kiln from PyPI.
- Reliability: end-to-end tests (each framework generated, installed and checked; a project of the previous releases updated without conflict), run on every release branch; kiln's CI on macOS too.

## v0.3.3 — 2026-10-16
- `kiln completion bash`: completion script drawn from kiln's commands and options, enabled by `eval "$(kiln completion bash)"` in `~/.bashrc` (#41, thanks @HarshRajSinghania).
- `good-first-issues` skill: keeps a few beginner issues open on GitHub, drawn from the backlog and reserved for outside contributors.
- Fixes: `kiln update` no longer stops on a conflict in `ci.yml` after a release is promoted (only the `@<tag>` of kiln's workflows differed); `base:worktree` no longer trips on a repo without a `.env` file; updating a kiln installed from a folder also removes the former `kiln` tool.

## v0.3.2 — 2026-10-16
- `kiln adopt` makes an existing repo follow kiln, without regenerating it; the `adoption` skill sorts out with the user what the charter finds there, and the session start offers it in a repo of one's own that does not follow kiln yet.
- Charter waivers in `kiln-waivers.toml`, with a reason and a deadline that grows at each renewal: `kiln waive` adds, renews or lists them, `kiln update` spares frozen files and says what it would have changed, `kiln status` counts each repo's.
- `relecture` skill: a branch's commits and diff reviewed and tidied before the merge (`fusion` runs it), the whole repo before a release (`version` runs it); the `garde-branche` hook refuses a commit message signed by Claude.
- kiln's questions at session start follow a common policy: each "no" spaces out the next one, each "yes" brings it closer.
- `kiln --version` (#39, thanks @SakarPaisen, first outside contribution).
- Fixes: `kiln update --all` says "GitHub unreachable" in one line instead of a Python traceback, and a failed run no longer blocks the next one with a worktree left empty.

## v0.3.1 — 2026-10-16
- **Breaking**: work tracking moves to English, `docs/a-faire/` becomes `docs/backlog/` (tickets `T-NN`, skill `base:backlog` instead of `base:a-faire`); `kiln update` moves the old folder.
- Numbering like Claude Code: in 0.x, each release bumps the patch, breaking ones included; the minor only moves for a milestone (`kiln version --minor`). A release is promoted as soon as the next one is ready as a candidate, without a waiting period.
- kiln installs from PyPI: package `kiln-cli` (the command stays `kiln`), published at the tag of each promoted release; `kiln doctor` and `maj-kiln` offer the update that way.
- New skills: `report-to-kiln` (a defect of kiln met in a repo becomes an issue or a PR, posted only with the user's consent), `token` (a service's token in `.<service>/`, pasted without showing), `contribution` (handling an outside contributor's PR).
- The generated CI runs gitleaks and can be called by other workflows (`workflow_call`).
- Status line: four styles in kiln's colours, in English (`kiln set statusline=…`), session name, RAM and busy cores.
- Fixes: `kiln doctor` offers the update at the release's tag, `kiln status` template column wide enough.

## v0.3.0 — 2026-10-15
- First published release. Semver in 0.x: a release first comes out as a candidate (`-rc.N`) for machines on the `interne` channel, then is promoted when the next one is ready and it has held for three days; `kiln version` says where the candidates stand.
- Projects quote kiln's workflows at the exact tag they start from; `kiln update` moves it forward and shows what is new in each release crossed. The session-start hook offers the tool, then the repo, at each release.
- `kiln status` says which release each repo starts from (`f611f82 → v0.3.0`); `kiln set canal=interne` (machine setting) follows the candidates.
- New interface: laughing kiln as a banner, sectioned welcome screen, spinner and duration for each external command, boxed recap of the steps; no colour outside a terminal, `KILN_VERBOSE=1` for the full output.
- `kiln doctor`: diagnosis of the machine and the repo, each problem with the command that fixes it.
- `kiln dev`: servers' output interleaved, prefixed by service in colour.
- `kiln update --all` merges each repo whose checks pass directly, without a PR.
- Java backend (Maven), `maj-kiln` skill, `.claude/kiln` link to the plugin, machine settings through `kiln set`.
