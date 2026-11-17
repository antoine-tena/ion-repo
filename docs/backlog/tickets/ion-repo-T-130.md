# ion-repo#T-130 · Generated repos pass the whole grid
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 ("bring kiln's Django + Nuxt template to the top of the
  grid"); two of the reference repo's gaps came from kiln itself

Fixing the grid in kiln fixes it everywhere at once; a kiln repo below 100 would make the whole
pitch hollow.
- [ ] `kiln new` Django + Nuxt, at each size: 100 on the rules that apply; the end-to-end tests
  fail when a template change lowers it.
- [x] The template's gaps closed (from the 17 October audit: actions by SHA, cooldown,
  Debian 13, read-only containers): shipped in v0.4.4.
- [ ] `kiln update` takes an older generated repo to 100 (the converters of ion-repo#T-126).
- [ ] The frozen templates (ion-repo#T-133) measured, their score in the docs.

From the kiln score ideas of 24 October 2026:
- [ ] **P01** `kiln new` proven at 100: every combination of answers (stack, size, options)
  generated and scored at each candidate; a template change that lowers any of them fails (ion-repo#T-130's
  matrix).
- [ ] **T07** kiln, its generated repos and the reference repo at 100, visibly (ion-repo#T-90, ion-repo#T-130, ion-repo#T-134).
