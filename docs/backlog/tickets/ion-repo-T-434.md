# ion-repo#T-434 · `version cut` checks the rehearsal repo is public before the long checks
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, ion-repo release v0.4.13 (21:34)

`ion-repo-rehearsal` went private with the other Ion repos that afternoon; the e2e job clones it
anonymously, so the release candidate's CI went red after the whole run, no tag.
- [ ] `ion repo version cut` checks first, without credentials, that the rehearsal repo can be
  cloned, and stops with the fix (`gh repo edit … --visibility public`).
- [ ] `CLAUDE.md` of ion-repo says the rehearsal repo stays public, beside the satellites.
