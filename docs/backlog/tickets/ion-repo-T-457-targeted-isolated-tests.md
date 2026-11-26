# ion-repo#T-457 · `ion repo check --tests` on a branch runs only the touched apps' tests, each run on its own services
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Session**: sonnet high
- **Touches**: `ion repo check` (scope of the test step); no migration, no API contract
- **Origin**: review of the three-role organisation (global CLAUDE.md of 2026-11-26): several Sonnet subagents work in parallel worktrees, and a sensitive ticket must pass its apps' tests before merging

Why: today `ion repo check --tests` runs the whole suite (`uv run pytest -q`, about 19 minutes on
annski) even on a branch, so agents run `pytest` by hand instead, all against the same shared
test database (`test_annski` on 127.0.0.1:55432) and Redis db: two runs at once collide. The
check already starts throwaway Postgres and Redis per run (`ion-repo-check-<pid>`), so routing
targeted runs through it isolates them for free.

- [ ] Without `--all`, `--tests` runs only the test directories of the Django apps (and other Python packages) the branch's changes touch: an app's own `tests/`, plus apps whose tests import a changed module when that is cheap to find; a change to settings, `conftest.py`, the lockfile or shared `core/` runs the whole suite.
- [ ] With `--all`, unchanged: the whole suite (the release).
- [ ] Each targeted run keeps its own throwaway services (already per pid): two worktrees checking at once never share a database.
- [ ] Prints which test paths it chose and why, in one line.
- [ ] Same scoping for the front's unit tests when cheap (`vitest related <changed files>`); otherwise leave the front as is and say so in the changelog.

## Files
- `src/ion_repo/check.py` — edit (`_check_commands` l. 96+, `_run_check` l. 65-85)
- `src/ion_repo/stack.py` — source of truth of the test commands (`PYTHON_TESTS` l. 135)
- `tests/test_check_scope.py` — test (scope chosen from a list of changed files)
- `CHANGELOG.md`, `README.md` (the `check` options) — edit

## Done when
`ion repo check --tests` green on ion-repo; in a copy of annski with one change in `backend/treasury/`, `ion repo check --tests` runs only `treasury` tests on its own containers, while a second run in another worktree goes on at the same time.
