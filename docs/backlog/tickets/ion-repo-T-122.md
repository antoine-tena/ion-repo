# ion-repo#T-122 · `kiln version` proposes 1.0.0
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: milestones decided by antoine, 16 October 2026 (v0.5.0, v0.6.0, v0.7.0, v1.0.0)

In 0.x, `kiln version --minor` only moves to the next minor (`release.py`): nothing proposes
leaving 0.x.
- [ ] `kiln version --stable` proposes `1.0.0` from any 0.x release, says what changes from then
  on (strict semver, breaking → major) and refuses without a `## v1.0.0` note that states the
  promise (what is public API, the grid format included; how long a major is supported).
- [ ] `kiln version` reads the milestones of `docs/backlog/` and says "the next release is the
  v0.6.0 milestone" instead of proposing a patch.
