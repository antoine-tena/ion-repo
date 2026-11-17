# ion-repo#T-235 · Tests that prove something: no sleeps, random order, assertions, names
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

- [ ] **TE17** `NO-SLEEP-IN-TESTS`: no `time.sleep` or `setTimeout` waits; a frozen clock or polling
  instead. L2 · fix J · trial.
- [ ] **TE18** `RANDOM-ORDER`: tests run shuffled (pytest-randomly, Vitest's `sequence.shuffle`) so
  hidden coupling shows. L1 · fix S · trial.
- [ ] **TE19** `PARALLEL-TESTS`: pytest-xdist or the runner's workers, for suites over a minute. L1
  · fix S · trial.
- [ ] **TE20** `ASSERTIONS-PRESENT`: no test without an assertion (`expect-expect` for Vitest and
  Jest, a syntax check for pytest). L2 · fix J · trial.
- [ ] **TE21** `FACTORIES`: factory_boy, model-bakery or fishery rather than big JSON fixtures. L1≈
  · fix J · assess.
- [ ] **TE24** `TESTS-TYPE-CHECKED`: tests not excluded from the type checker. L1 · fix S · trial.
- [ ] **TE25** `TEST-NAMES`: names that state the behaviour (`test_refuses_expired_token`), never
  `test_1` or `test_view`. L2≈ · fix J · assess.
- [ ] **TE26** `SNAPSHOTS-IN-CHECK`: obsolete snapshots fail in CI (`--ci`), snapshot files stay
  small. L1 · fix S · assess.
- [ ] **TE27** `CONTRACT-TESTS`: consumer-driven contracts (Pact) between the services of one
  organisation. L1 · fix J · assess.
- [ ] **TE28** `LOAD-SCENARIO`: a k6 or Locust scenario kept in the repo of an app with an SLO. L0 ·
  fix J · assess.
