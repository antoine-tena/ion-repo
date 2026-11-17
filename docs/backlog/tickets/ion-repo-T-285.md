# ion-repo#T-285 · `--deep`: the repo's own checks in a sandbox
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Deep checks, opt-in
  and sandboxed, Trust, privacy and safety, Developer experience), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.51, "`--deep`: the repo's own checks, in a sandbox": Opt-in, in a throwaway copy
with the network off: the install from the lock, the tests (flaky, order, network, clock), Django's
deploy check, type checkers at their strictest, a clean clone.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F14** Type checkers as ratchet metrics in `--deep` (mypy, pyright, ty or pyrefly once
  mature, tsc, vue-tsc): the error count at strict settings.
- [ ] **N01** `--deep` runs in a throwaway copy, in a container when an engine is there, network off
  unless a step needs it, within a time budget; never in the user's tree.
- [ ] **N04** An install from the lock that works (`uv sync --locked`, `pnpm install
  --frozen-lockfile`): LOCK-IN-SYNC proven.
- [ ] **N05** Tests run: pass rate, duration, the slowest, the flaky (failures run again), order
  dependence (random order), network use (sockets blocked: NO-NETWORK proven), clock dependence (a
  shifted fake clock: CLOCK proven).
- [ ] **N06** Coverage measured (lines and branches) and mutation testing on a sample (mutmut,
  Stryker): the tests theme's ratchets fed with real numbers.
- [ ] **N07** Django's own `manage.py check --deploy` against the production settings: HSTS, SSL
  redirect, secure cookies, `DEBUG`, `SECRET_KEY`'s strength, `ALLOWED_HOSTS`, X-Frame-Options.
  Official checks, mapped onto grid rules.
- [ ] **N08** `manage.py makemigrations --check --dry-run`: models and migrations in sync.
- [ ] **N15** Type checkers and the repo's linters at their strictest: error counts as ratchets.
- [ ] **N16** The app's start-up time and memory, as ratchets.
- [ ] **N17** Deep results cached by commit and marked "measured at <commit>"; kiln-bot's weekly run
  uses `--deep` in CI, where running code is normal.
- [ ] **S08** Network calls listed before they start, as the fixers' `network` flag does, and only
  with `--online` or `--deep`.
- [ ] **DX07** `CLEAN-CLONE-WORKS`: a fresh clone installs and passes its checks with the documented
  commands (`--deep`, in a sandbox). L7 · fix J · trial.
