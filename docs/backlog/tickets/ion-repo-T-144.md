# ion-repo#T-144 · Checks as fast as they are precise: oxlint, TypeScript 7, ty or pyrefly, measured
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-18
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026, doctrine 11 ("the fastest, at equal precision"; on the
  reference repo: ruff 0.4 s, the charter 1.1 s, mypy 22.6 s, eslint 42.3 s)

A slow check ends up not being run, and the time goes into the tools, not into kiln's code.
- [ ] Each candidate measured on a local copy of the reference repo against the tool it would
  replace, for time and for what it finds: oxlint next to eslint (2.7 s, fewer rules, weak on Vue
  templates), TypeScript 7's native compiler for the type check, ty or pyrefly next to mypy on
  Django code.
- [ ] Each one a grid rule (ion-repo#T-123): `trial` in the template only when it finds at least what the
  old tool found on the rules it covers, `assess` otherwise; the measurement kept as its source.
- [ ] kiln's own rules written as ast-grep patterns where a pattern can say them; Rust only where
  a measurement shows kiln's code is the slow part.
