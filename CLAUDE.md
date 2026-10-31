# ion-repo

Copier template, `ion-repo` command, `charter` engine, Claude Code plugins, reusable workflows. Generic to repos lives here: generated-file defect → fix `template/`, then `ion repo update`. Overview `README.md`/`.fr.md`; detail `docs/reference.md`/`.fr.md`.

## Repo map

- `src/ion_repo/`: `cli.py`; one command per module: `new.py` (`questions.py`), `adopt.py` (kept files listed under `kept` in `.copier-answers.yml`), `install.py`, `dev/` (`processes`, `backing`, `menu`, `background`, `foreground`, `containers`), `check.py`, `settings.py`, `machine.py`, `waive.py`, `pause.py`, `frame.py`, `eval_skills.py` (`claude plugin eval` of `plugins/repo/evals/`, three ok first), `bot.py` (kiln-bot on `kiln/bot`; bench `antoine-tena/kiln-bot-test`), `update.py`, `contract.py`, `release.py`, `shipping.py` (`version cut|promote`), `github_ci.py`, `doctor.py`, `tool_update.py`, `fleet.py`, `adopted.py`, `adopted_names.py`, `rehearsal.py`. Core: `stack.py`, `template.py`, `deps.py`, `github.py`, `rules.py`, `statusline.py`, `versions.py`, `frozen.py`, `renames.py`, `ion_names.py`, `moved_dirs.py`, `banner.py`, `ui.py`, `shell.py`, `config.py`, `trailers.py`, `migrations.py`.
- `src/ion_repo/grid/`: `rules/<theme>/<ID>.toml`, `model.py`, `facts.py`, `detectors.py`, `forge.py` (`gh`, cached a day), `fixers/`, `fix.py`, `checks.py`, `show.py`, `score.py`, `gap_report.py`, `roadmap.py`; each rule has pass/fail examples in `tests/test_grid.py`.
- `src/ion_repo/ci/`: `ion repo ci` (verdict in git note). `src/ion_repo/charter/`: engine (`bans`, `ratchets`, `python_tools`, `waivers`).
- `hatch_build.py`: writes build commit to `ion_repo/_build.json`.
- `copier.yml`, `macros.jinja`, `template/` (`CLAUDE.md.jinja`, `.claude/rules/ion-repo/`, `.claude/settings.json.jinja`, CI…).
- `plugins/`: catalog `.claude-plugin/marketplace.json` (`renames`: `kiln`, `base`, `pile-django`, `pile-nuxt`, `vps-podman`). `repo/` (skills; `evals/`: one trigger case per skill; `hooks/`: `reminders`, `paused`, `first_prompt`, `place`, `session_start`; `scripts/statusline.py`, `lifetime_tokens.py`), `django/`, `nuxt/`, `vps/`, `stripe/`, `serena/`; `kiln/`, `base/`: forwards from old paths.
- `.github/workflows/`: reusable workflows (actions and `charter` at `job.workflow_sha`); own: `kiln.yml` (checks, score 100, zizmor; `.github/zizmor.yml`), `pypi.yml` (`ion-repo`, `kiln-cli` at promoted tag, provenance), `scorecard.yml`. `actions/`: `charter` (old `charte`), `services`. `.github/dependabot.yml` (uv, actions, after 7 days).
- `.claude/rules/`: `releases.md`, `docs.md`.
- Showcase: READMEs, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`. `docs/assets/`: drawn by `scripts/screenshots.py` (checked by `test_docs.py`); VHS demos `kiln-new`, `kiln-rescue` (on public `antoine-tena/kiln-demo-legacy`, old on purpose); `social-preview.png` (uploaded by hand).
- `docs/backlog/` (English, `/repo:backlog`): `backlog.md` (`## 🚀 Releases`, `## 📖` how-to, `## 🧭 Vision`, `## 💡` score thesis), `done.md`, `rejected.md`, `urgent.md`.
- `ROADMAP.md`/`.fr.md`: milestones by hand, releases from backlog via `scripts/roadmap.py`; rerun after each plan change (`test_docs.py` fails otherwise).
- `scripts/`: `screenshots.py`, `social_preview.py`, `demo_shell.sh`, `shrink_demo.sh` (<5 MB), `refresh_images.py` (pin base images, before each candidate).
- `tests/`: `test_<module>.py`, plus `test_template.py` (each stack), `test_e2e.py` (`-m e2e`: every release since v0.3.0, witness `antoine-tena/ion-repo-rehearsal` frozen at v0.3.3-rc.2: never update it), `test_plugins.py` (cited skills exist; rule paths match), `test_docs.py` (`.claude/rules/docs.md`), `conftest.py` (git config aside, test identity).

## Training repos

Trains on the association's repo (Django+Nuxt reference, grid ground; path in global instructions, never named here) and a university repo. **Detailed measures are private**: `antoine-tena/ion-repo-measures` (`mesures-repos-entrainement.md`), never in ion-repo, a branch or a commit. Public: association's repo as aggregate figures only, never its name; university repo not cited at all. Measure on a local copy only. Also trains on antoine's small repos (sweep, a course project: up to 100, own sessions) and `annway-copie` (Java pack), never annway.

## In every change

- A name changes through `ion repo set` or a conversion in `ion repo update`, never find-and-replace in a generated repo (conflicts at next update).
- **Breaking** = public API: CLI commands/options, `copier.yml` questions, generated tree, workflow/action inputs, skill and hook names, charter rule IDs. Mark `feat!:`/`BREAKING CHANGE`, ship its conversion in `ion repo update`; opens the `CHANGELOG.md` note.
- User-only post-update step: commit body line `After updating: …`; `version cut` copies it to the note, `ion repo update` makes a 🔴 "Finish the ion-repo update to vX.Y.Z" ticket in `docs/backlog/backlog.md` (not `urgent.md`), worked by `/repo:update` right after merge.
- Docs update in the same branch: every command, option, setting, plugin, skill, hook, workflow in both references; READMEs follow. `test_docs.py` runs at release only, a forgotten doc blocks the candidate (`.claude/rules/docs.md`).

## Releases

0.x: each release bumps patch, even features/breaking; minor about every ten (`version cut --minor`), at a themed milestone. One release per two days. Plan: `backlog.md`, shown by `ROADMAP.md`; public launch T-03. Candidates, promotion, channels: `.claude/rules/releases.md`, read before `/repo:release`.

## Checks

Merge into `develop`: `uv run ruff check` and `ruff format --check` on changed files only; no mypy, tests, GitHub CI. GitHub CI (`kiln.yml`) only on `release/**`, before `main`, and by hand. `uv run pytest -q` (xdist; `-n 0` to debug) in full at `version cut`. Pre-commit runs ruff at commit; nothing before push.

This machine runs ion-repo editable from this checkout (channel `beta`); local plugin catalog means open sessions call hooks and status line from the main tree's `plugins/`. Reaching `develop` is live: a removed/renamed plugin path blocks tools everywhere, so keep a forward (`plugins/base/`, `test_plugins.py`).
