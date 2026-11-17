# ion-repo#T-205 · The slimming rules: dead code, unused dependencies, duplication, a dependency budget
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Code standards, Supply
  chain), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.1, "Less code to carry": The vision's fourth pillar, measured before anything is
built: the compressor's dry run, removals proven by types, tests and behaviour, the slimming rules
promoted once precise.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F13** deptry and knip (unused and missing dependencies) and vulture (dead code), already
  used by the compressor: their findings feed UNUSED-DEPENDENCIES and DEAD-CODE once their precision
  is measured.
- [ ] **CS09** `DEAD-CODE` (trial): vulture and knip, promoted once their precision is measured on
  the corpus. L4≈ · fix S (the compressor) · trial.
- [ ] **CS31** `DUPLICATION`: no duplicated block over about 50 tokens across files (the charter's
  `identical-copies`, generalized). L3 · ratchet · trial.
- [ ] **SU02** `UNUSED-DEPENDENCIES` (trial): deptry and knip, promoted once precise. L4≈ · fix S ·
  trial.
- [ ] **SU17** `DEPENDENCY-BUDGET`: the count of transitive dependencies tracked as a ratchet (the
  slimming pillar). L1 · ratchet · trial.
