# ion-repo#T-245 · oxlint or Biome mapped, barrel files counted
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Structure), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.31, "Code standards from the syntax tree": What a regex can't tell: modern Vue,
explicit imports, floating promises, debug prints, TODOs without a ticket, barrel files, with oxlint
or Biome where they decide.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F07** oxlint or Biome for JS/TS rules (no-eval, eqeqeq, no-debugger, accessibility) as
  native binaries (ion-repo#T-144 measures them).
- [ ] **ST12** `NO-BARREL-FILES`: no `index.ts` re-exporting a whole folder (slower bundles and
  tests, one more hop for Claude). L2 · fix J · assess.
