# ion-repo#T-234 · Tests counted right: presence, clock, network, coverage, strict pytest
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Tests), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.23, "Tests that prove something": Tests per component that assert, run shuffled and
in parallel, without network or sleep, coverage that only rises; a front with no backend gets its
smoke test.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **TE01** `TESTS-PRESENT` (scored): per component, and a test file that collects nothing
  doesn't count (pytest's `--collect-only` with `--deep`).
- [ ] **TE03** `CLOCK` (draft): tests calling `now()`, `date.today()` or `Date.now()` with no
  time-machine, freezegun or `vi.useFakeTimers` in reach. L3≈ · fix J · trial.
- [ ] **TE04** `NO-NETWORK` (draft): sockets blocked in tests (pytest-socket's `--disable-socket`,
  msw with `onUnhandledRequest: "error"`, nock's `disableNetConnect`). L1 · fix S · trial.
- [ ] **TE09** `PERMISSION-TESTS` (draft): each protected route (from the URL conf or Ninja's
  routers) has a test that calls it anonymously. L3≈ · fix J · trial.
- [ ] **TE11** `COVERAGE-MEASURED`: coverage with branches (`[tool.coverage.run] branch = true`,
  Vitest's coverage provider). L1 · fix S · adopt.
- [ ] **TE12** `COVERAGE-FLOOR`: a floor that only rises (`fail_under`, Vitest's thresholds with
  `autoUpdate`). L1 · ratchet · trial.
- [ ] **TE13** `DIFF-COVERAGE`: changed lines covered in pull requests (diff-cover). L1 · fix S ·
  assess.
- [ ] **TE14** `PYTEST-STRICT`: `--strict-markers`, `--strict-config`, `xfail_strict = true`,
  warnings as errors with a named allow-list. L1 · fix S · adopt.
- [ ] **TE15** `NO-FOCUSED-TESTS`: no `.only`, `fit` or `fdescribe` committed. L2 · fix S · adopt.
- [ ] **TE16** `NO-SKIPPED-TESTS`: every `skip` and `xfail` gives a reason, and their count only
  goes down. L2 · ratchet · trial.
