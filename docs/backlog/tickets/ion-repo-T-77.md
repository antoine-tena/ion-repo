# ion-repo#T-77 · Tests in seconds after each edit: only those the change touches
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; complements ion-repo#T-27 (doctrine 11: only recheck what
  changed)

Claude Code learns from fast feedback; a full suite after each edit is too slow on big repos.
- [ ] `kiln test --changed`: pytest-testmon, `vitest related`; the full suite stays in
  `kiln check` and CI.
- [ ] Offered to Claude as the default test command in the generated rules.
