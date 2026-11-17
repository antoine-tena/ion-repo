# ion-repo#T-87 · Fleet view: every repo of an organisation scored, without cloning
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 (the vision's targets: a
  university whose student teams change every year, an association network)

- [ ] `kiln status --org <name>`: through the GitHub API, each repo's score, its lag behind the
  grid, its CI and its open security alerts.
- [ ] An HTML report, also produced weekly by a workflow in the organisation's `.github` repo.

From the kiln score ideas of 24 October 2026:
- [ ] **K05** Remote scoring without a clone for L0 and L1 rules: the Git Trees API lists every path
  in one call for most repos, then a few config files are fetched. Seconds, for ion-repo#T-87's fleet view.
- [ ] **P17** The fleet (ion-repo#T-87) scores an organisation's repos remotely (K) and ranks gaps by how
  many repos share them: one fix in kiln helps them all.
