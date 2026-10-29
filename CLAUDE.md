# kiln: working instructions

Claude Code's workshop: knowledge, guardrails, ways of working and keeping repos up to date
(Copier template, `kiln` command, `charter` engine, Claude Code plugins, reusable workflows).
Everything generic to repos lives here: a defect in a generated file is fixed in `template/`,
then `kiln update` in the repo. Overview in [`README.md`](README.md) (French:
[`README.fr.md`](README.fr.md)), every detail in [`docs/reference.md`](docs/reference.md)
([`docs/reference.fr.md`](docs/reference.fr.md)).

## Repo map

Where to look instead of exploring; keep it current in the commit that adds, moves or removes a
folder or a module.

- `src/kiln/`: the command. `cli.py` (arguments; 0.3 names accepted by `modernize`); one command
  per module: `new.py` (questions in `questions.py`), `adopt.py` (`kiln adopt`, an existing repo:
  the template rendered without overwriting a file, the files kept listed under `kept` in
  `.copier-answers.yml` and never written by `kiln update`), `install.py`, `dev/` (`kiln dev`:
  `processes.py` the stack's servers and `Procfile.dev`, `backing.py` the compose databases in
  podman, `menu.py` what to run and the logs offered, `background.py` background, `status`,
  `logs`, `stop`, `foreground.py` `--foreground`, `containers.py` `--containers`), `check.py`,
  `settings.py` (`kiln set`, the settable keys), `machine.py` (`kiln set` outside a repo: machine
  settings), `waive.py` (`kiln waive`), `pause.py` (`kiln pause`, a session's place kept, T-344), `bot.py` (`kiln bot`, kiln-bot's run on `kiln/bot`, T-59; its public test bench
  `antoine-tena/kiln-bot-test` calls `bot.yml`, `score.yml` and `charter.yml`), `update.py`, `contract.py`, `release.py`
  (`kiln version`), `shipping.py` (`kiln version cut` and `promote`), `github_ci.py` (GitHub CI's
  verdict on a commit, awaited by `cut` and `promote`), `doctor.py` (machine and repo diagnosis),
  `tool_update.py` (tool update offered after a command typed outside Claude Code), `fleet.py`
  (`status`, `update --all`), `adopted.py` (a repo adopted before 0.4.6, a charter without
  answers: only its kiln workflow tag moves to the latest public release, until `kiln adopt`
  completes it, T-146), `adopted_names.py` (adopted repo: its kiln 0.3 names converted by
  `kiln update`), `rehearsal.py` (`kiln update --rehearse`, the update on a throwaway clone);
  core: `stack.py` (stack read from `.copier-answers.yml`), `template.py`, `deps.py`,
  `github.py`, `rules.py` (unchecked rules), `statusline.py`, `versions.py` (tags, channels,
  release log, tool version), `frozen.py` (files frozen by `kiln-waivers.toml`, spared by
  `update`), `renames.py` (pre-0.4.0 names and their English names), `banner.py` (banner,
  welcome screen), `ui.py` (stone-and-fire palette, steps, spinner, summary, success, errors),
  `shell.py`, `config.py` (`~/.config/kiln/config.toml`), `trailers.py` (`kiln set ai_trailers`:
  whether Claude's commits say Claude helped, Claude Code's `attribution`).
- `src/kiln/grid/`: the grid (T-123): `rules/<theme>/<ID>.toml` one rule per file, `model.py`
  (format, closed lists, validation), `facts.py` (what a repo is made of), `detectors.py`
  (declarative detectors, Python checks), `forge.py` (the GitHub settings read through `gh`,
  cached a day), `fixers/` (`kiln fix` converters: `ci.py`, `workflows.py`
  (what an existing CI lacks, a tracked `.env`), `python.py`, `containers.py`, `resolve.py` for SHAs and digests online), `fix.py` (`kiln fix`), `checks.py` (the repo's checks that judge
  each converter: found, timed out, told apart, a reverted converter's log kept), `show.py`
  (`kiln grid`), `score.py` (`kiln score`, a repo scored against the grid), `gap_report.py` (what
  the grid doesn't cover, reported to kiln with the user's consent, T-38), `roadmap.py`
  (`kiln score --roadmap`, `--rule`, `--write`: what needs judgment, for Claude); every rule has a
  passing and a failing example in `tests/test_grid.py`.
- `src/kiln/ci/`: `kiln ci` (CI replayed on the machine, verdict in a git note);
  `src/kiln/charter/`: the `charter` engine (`bans.py`, `ratchets.py`, `python_tools.py`,
  `waivers.py`: the waivers of `kiln-waivers.toml`).
- `hatch_build.py`: writes into the package the commit it is built from (`kiln/_build.json`,
  read by `versions.py`).
- `copier.yml`: the template's questions; `template/`: the template (`CLAUDE.md.jinja`, Claude's
  instructions in `.claude/rules/kiln/`: project, charter, one per stack;
  `.claude/settings.json.jinja`, CI…); `macros.jinja`.
- `plugins/`: Claude Code plugins, catalog `.claude-plugin/marketplace.json` (with `renames`:
  old names `base`, `pile-django`, `pile-nuxt`, `vps-podman`); `kiln/` (skills `worktree`,
  `merge`, `release`, `cleanup`, `review` (a branch's commits and diff before the merge, the whole
  repo before a release), `backlog`, `update`, `adopt`, `modernize` (roadmap gaps closed one by
  one), `report` (a kiln defect raised as an issue or a PR), `token` (a service's token in
  `.<service>/`), `contribution` (an outside contributor's PR), `good-first-issues`, `pause` (the session's place kept, `kiln pause`); `hooks/`
  (including `reminders.py`, the spacing of update questions, `paused.py`, the sessions `kiln pause` kept, listed at start, and `first_prompt.py`, kiln's logo
  and what's new above the prompt); `scripts/statusline.py`, `scripts/lifetime_tokens.py`, the tokens of every transcript), `django/`, `nuxt/`, `vps/`,
  `stripe/`, `serena/`; `base/`: forwards from the old paths of the hooks and scripts (open
  sessions, status line).
- `.github/workflows/`: reusable workflows called by generated repos (they take their actions
  and the `charter` command at their own commit, `job.workflow_sha`), plus kiln's own
  (`kiln.yml` checks, `kiln score` at 100 and zizmor included, its false positives explained in
  `.github/zizmor.yml`; `pypi.yml` publishes the `kiln-cli` package at the promoted tag, with
  build provenance, attached to the GitHub Release; `scorecard.yml` the weekly OpenSSF Scorecard);
  `actions/`: composite actions (`charter`, its old name `charte`,
  `services`); `.github/dependabot.yml`: proposed updates (uv, the actions of the workflows and
  composite actions, after 7 days).
- `.claude/rules/`: instructions loaded with their files: `releases.md` (versions, candidates,
  promotion, channels), `docs.md` (READMEs, reference, images, demos, the promise).
- Public showcase: `README.md` (and its translation `README.fr.md`), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, `LICENSE` (MIT),
  `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`; full reference
  `docs/reference.md` and `docs/reference.fr.md`; images in `docs/assets/` (drawn by
  `scripts/screenshots.py`, checked by `test_docs.py`), including the two animated demos recorded
  with VHS, `kiln-new.gif` (`kiln-new.tape`) and `kiln-rescue.gif` (`kiln-rescue.tape`, on the
  public repo `antoine-tena/kiln-demo-legacy`, kept old on purpose), and the share image
  `social-preview.png` (uploaded by hand in GitHub's settings).
- `docs/backlog/`: work tracking, in English (skill `/kiln:backlog`), with the release plan
  (`## 🚀 Releases`); `backlog.md` ends with its how-to (`## 📖`: tickets, effort scale, session
  budget), the vision that orders the tickets (`## 🧭 Vision`) and the thesis of `kiln score`
  (`## 💡`, source of T-186 to T-319); next to it, only `done.md`, `rejected.md` and `urgent.md`.
- `ROADMAP.md` (and `ROADMAP.fr.md`): the public roadmap, linked from the READMEs; milestones
  written by hand, releases drawn from the backlog's `## 🚀 Releases` by `scripts/roadmap.py`, to
  rerun after every change to the plan (`test_docs.py` fails otherwise).
- `scripts/screenshots.py`: draws the README's images from kiln's real outputs (and the logo, the
  share image); `scripts/social_preview.py`: the share image as a PNG (Playwright);
  `scripts/demo_shell.sh`: the shell of the recorded demos (this folder's kiln, without a version
  number, in a throwaway folder on disk, the template rendered like a release, Claude Code as a
  visitor has it); `scripts/shrink_demo.sh`: a recorded demo brought under 5 MB (palette, frozen
  stretch cut); `scripts/refresh_images.py`: the template's base images pinned to the digest of
  their tag (before each candidate).
- `tests/`: `test_template.py` (the template rendered for each stack), `test_cli.py` (the
  command: welcome, errors, summary, output outside a terminal, old names), `test_questions.py`
  (`kiln new`'s questions), `test_new.py` (what `kiln new` says at the end), `test_contract.py` (`kiln contract`'s export, a dirty tree named), `test_pause.py` (`kiln pause`'s proposed names), `test_update_conflicts.py` (`kiln update` stopped by a template's conflict), `test_grid.py` (the
  grid), `test_score.py` (`kiln score`), `test_gap_report.py` (reports of the grid's gaps), `test_forge.py` (GitHub settings through a
  fake `gh`),
  `test_fix.py` (`kiln fix` and its conversions), `test_adopted.py` (adopted repos),
  `test_unites.py`, `test_ci.py`, `test_flotte.py`, `test_waivers.py` (waivers), `test_waive.py`,
  `test_charter_file.py` (`charter file`, the hook after an edit), `test_shipping.py`
  (`kiln version cut` and `promote`), `test_rehearsal.py` (`update --rehearse`), `test_e2e.py`
  (end to end, `-m e2e`: every release since v0.3.0 through an installed tool, and the witness
  repo `antoine-tena/kiln-rehearsal`, frozen at v0.3.3-rc.2: never update it),
  `test_deployment.py`, `test_statusline.py` (the machine's choices and the script's rendering),
  `test_plugins.py` (cited skills exist, named like their folder; each path of a rule in
  `.claude/rules/` matches a file), `test_docs.py` (the showcase up to date:
  `.claude/rules/docs.md`), `test_branch_guard.py` (branch guard hook), `test_adopt.py`,
  `test_reminders.py`, `test_session_start.py`; `conftest.py`: the machine's git config set
  aside, a test identity.

## Training repos

kiln trains on two real repos, measured on 17 October 2026: the association's repo (the
Django + Nuxt reference, the grid's training ground, T-124, T-134; its path is in the machine's
global instructions, never named here) and a university repo (an ordinary repo, the test for a
repo kiln didn't create, T-131). **The detailed measurements are not public** (security gaps of
a site in production, vulnerabilities of a third-party project not yet reported to its team):
they live in the **private** repo `antoine-tena/kiln-private` (`~/code/kiln-private`,
`mesures-repos-entrainement.md`), never in kiln, not on a branch, not in a commit. Write only
aggregate figures in the public repo about the association's repo, never its name; the
university repo is not cited at all, not even in aggregate (antoine, 26 October 2026). Always
measure on a local copy, never in the repo itself. kiln may also train on antoine's small repos
(sweep, a course project: up to 100, in their own sessions) and on a copy of annway
(`annway-copie`, for the Java pack), never on annway itself.

## In every change

- **Breaking** is whatever touches kiln's public API: commands and options of the CLI,
  questions of `copier.yml`, the generated tree, inputs of the reusable workflows and actions,
  names of skills and hooks, IDs of charter rules. Mark it in the commit (`feat!:` or
  `BREAKING CHANGE`) and ship its conversion in `kiln update`; it opens the release note in
  `CHANGELOG.md`.
- What only the user can complete after an update (information kiln can't guess, such as each
  person's GitHub login) goes in a line of the commit body, `After updating: …`:
  `kiln version cut` copies it into the note (`- **After updating**: …`) and `kiln update` turns
  it into a 🔴 "Finish the kiln update to vX.Y.Z" ticket of each repo's
  `docs/backlog/backlog.md` (not `urgent.md`), which `/kiln:update` works through with the user
  right after the merge.
- A change updates the docs in its own branch, never at the release: every command, option,
  `kiln set` setting, plugin, skill, hook and reusable workflow is in both references
  (`docs/reference.md`, `docs/reference.fr.md`), and both READMEs follow what they show.
  `test_docs.py` only runs at the release, where a forgotten doc blocks the candidate; its
  checks: `.claude/rules/docs.md`.

## Releases

0.x: every release bumps the patch, features and breaking changes included; the minor moves about
every ten releases (`kiln version cut --minor`), at a themed milestone holding its breaking
changes, as uv and ruff do (antoine, 26 October 2026; the plan renumbered by T-360). One release
every two days. The plan and the milestones: `docs/backlog/backlog.md` (`## 🚀 Releases`, `## 🧭 Vision`), shown by
`ROADMAP.md`; the public launch: T-03. Candidates, promotion and channels:
`.claude/rules/releases.md`, to read before `/kiln:release`.

## Checks

At a merge into `develop`: `uv run ruff check` and `uv run ruff format --check` on the files the
branch changed, nothing else: no mypy, no tests, no GitHub CI (antoine's choice). GitHub CI
(`kiln.yml`) only runs on `release/**`, before `main`, and by hand. `uv run pytest -q` (spread
over every core by pytest-xdist; `-n 0` for a single process, when debugging) runs in full at the
release (`kiln version cut`), which plays everything. kiln's pre-commit hook
(`.pre-commit-config.yaml`, set up by `kiln install`) runs ruff at each commit, nothing before a
push.

antoine's machine runs kiln from this checkout: the tool is installed as editable (channel
`beta`), and since the plugin catalog is declared as a local folder, open sessions call the hooks
and the status line **in the main tree** (`~/code/kiln/plugins/…`). What reaches `develop` runs
at once in his sessions, and a file removed or renamed breaks every session at once (hook not
found = tool blocked): a plugin path that changes keeps a forward from the old one
(`plugins/base/`, checked by `test_plugins.py`).
