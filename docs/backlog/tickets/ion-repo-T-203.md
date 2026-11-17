# ion-repo#T-203 · Tests that cost no tokens: properties, mutants, API fuzzing, journeys as rules
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The roadmap for Claude, Tests), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.5.16, "Tests at the lowest token cost": The other half of v0.6.0: generators that cost
no tokens in the template, coverage and surviving mutants measured by script, Claude on the holes
only.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **O08** Each place's coverage (from `--deep` or a committed report): untested places get
  "write a characterization test first".
- [ ] **TE05** `PROPERTY-TESTS` (draft): Hypothesis or fast-check where parsers, serializers or
  money code live, found by paths and names. L1≈ · fix J · assess.
- [ ] **TE06** `MUTATION-TESTS` (draft): mutmut, cosmic-ray or Stryker configured and scheduled. L1
  · fix J · assess.
- [ ] **TE07** `API-FUZZING` (draft): Schemathesis run against the committed OpenAPI schema. L1 ·
  fix S · trial.
- [ ] **TE08** `E2E-JOURNEYS` (draft): Playwright present, its specs naming the journeys the docs
  list. L1≈ · fix J · trial.
