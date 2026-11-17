# ion-repo#T-107 · After an update, Claude is told what changed in its rules
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, second batch, 16 October 2026; the grid changes at every release

A session opened before an update keeps working by the old rules.
- [ ] The session-start hook says, once, the rules added or changed by the last update (from
  the release notes and the grid's `since`), in three lines at most.
