# ion-repo#T-360 · The plan renumbered: a minor every ten releases or so
- **Type**: task
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.5.0 candidate
- **Origin**: antoine's yes to decision 23 of 26 October 2026 (Q58: "I don't want too many p in
  vN.m.p")

Long runs of patches (v0.5.17, v0.6.23) are what antoine does not want; uv and ruff move the minor
every few weeks, each minor a themed group holding its breaking changes.
- [ ] `## 🚀 Releases` regrouped into minors of about ten releases, each named for its theme, the
  launch staying v0.5.0; the big milestones (Claude alone, teams, every stack, any CI, 1.0) keep
  their order and get their new numbers.
- [ ] `ROADMAP.md`'s two hand-written milestone tables, `.claude/rules/releases.md`, the vision's
  dates and the tickets' "Planned in" lines follow; `scripts/roadmap.py` rerun.
