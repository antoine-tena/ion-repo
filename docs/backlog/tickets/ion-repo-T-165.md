# ion-repo#T-165 · Write less code, measured: a ladder before writing
- **Type**: idea
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-21
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: the most-starred token savers, 21 October 2026: ponytail (a skill, about 45 % fewer
  tokens and more risky logic tested, by its maintainer's own benchmark)

Before writing, Claude climbs a ladder and stops at the first rung that works: does this code
need to exist, does the repo already have it, the standard library, an installed dependency, a
few lines; never cut: validation at the boundaries, security, data loss, accessibility, a test
for each risky logic. Same pillar as ion-repo#T-138 and ion-repo#T-139, which remove code that exists; this one
keeps it from being written.
- [ ] A few lines in `template/.claude/rules/kiln/` (they are read at every message).
- [ ] Measured before it stays, with ion-repo#T-53's method: the same tasks with and without, tokens,
  lines written, tests, bugs caught; dropped if it does not win.
