# ion-repo#T-91 · Findings where people look: SARIF in pull requests and code scanning
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: growth review, 16 October 2026; rewritten 17 October 2026 for the grid

- [ ] `kiln score --sarif`, uploaded by kiln-bot (ion-repo#T-59) and the charter workflow: findings in
  the pull request diff and in GitHub code scanning.
- [ ] Repo-local rules in the grid's format (`.kiln/grid/`), tested like kiln's; a rule that
  proves useful is proposed to kiln by `/kiln:report`.

From the kiln score ideas of 24 October 2026:
- [ ] **L02** Complete SARIF 2.1.0: rules with `helpUri` to their page, regions,
  `partialFingerprints`, `fixes` for scripted fixes, waivers as `suppressions` with their reason
  (ion-repo#T-91).
- [ ] **R01** Repo-local rules in `.kiln/grid/` (ion-repo#T-91), in the same format, their examples run by
  `kiln grid test`.
