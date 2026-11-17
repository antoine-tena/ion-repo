# ion-repo#T-215 · Python standards ruff already decides: modern syntax, formatting, linting
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.12, "Code standards a linter proves": With ruff mapped (v0.6.10), the Python
standards it already decides become rules at once, its safe fixes their converters; shell scripts
and encodings come with them.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS06** `MODERN-PYTHON` (draft): ruff's UP rules at the `requires-python` target; ruff's
  fixes are the converter. L4 · fix S · adopt.
- [ ] **CS11** `RETURN-VALUES` (draft): functions that return a value on some paths and nothing on
  others (ruff's RET503). L4 · fix J · trial.
- [ ] **CS13** `NO-MAGIC-VALUES` (draft): ruff's PLR2004 and its JS counterpart. L4 · fix J · trial.
- [ ] **CS15** `FORMATTER`: a formatter configured for each language, as `PYTHON-LINTER` and
  `JS-LINTER` ask a linter (ruff format or Black, Prettier or Biome, gofmt, rustfmt, Spotless,
  `dotnet format`, RuboCop, PHP-CS-Fixer). L1 · fix S · adopt.
- [ ] **CS16** `FORMATTED`: the code really is formatted (`ruff format --check` and the other
  formatters shipped as wheels). L4 · fix S · adopt.
- [ ] **CS17** `LINTER-CLEAN`: the repo's own linter config passes, or its error count only goes
  down. L4 · ratchet · trial.
- [ ] **CS21** `NO-COMMENTED-CODE`: no code left commented out (ruff's ERA001). L4 · fix S · trial.
- [ ] **CS22** `NO-MUTABLE-DEFAULTS` (Python): ruff's B006. L4 · fix S · adopt.
- [ ] **CS23** `NO-STAR-IMPORTS` (Python): F403, settings modules aside. L4 · fix J · adopt.
