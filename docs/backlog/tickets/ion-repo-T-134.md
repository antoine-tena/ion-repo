# ion-repo#T-134 · The reference repo's score in every release note
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (the reference repo as training ground: its score
  measured at each kiln release)

- [ ] `kiln version` runs `kiln score --json` on the reference repo (read-only, its path in a
  machine setting) and on a local copy after `kiln fix`, and writes one line in the release
  entry, such as "Reference repo: 58 → 61, and 74 with `kiln fix`".
- [ ] A drop stops the candidate until it is explained.

From the kiln score ideas of 24 October 2026:
- [ ] **P15** The reference repo's score and its potential after `kiln fix` in every release note
  (ion-repo#T-134).
