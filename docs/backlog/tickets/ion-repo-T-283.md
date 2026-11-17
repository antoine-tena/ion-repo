# ion-repo#T-283 · Repo hygiene on the forge: submodules, CODEOWNERS, force pushes, stale branches
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Git and versions), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.49, "The forge's settings, read": Through the `gh` already logged in: token
permissions, secrets' ages, environments, required checks, alerts left open, update pull requests
ignored.

The six drafts are questions about history: `--history` (M) gives them detectors.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **GV17** `SUBMODULES-SANE`: submodules over HTTPS, pinned to commits their remote still has.
  L1 + L6 · fix J · trial.
- [ ] **GV18** `CODEOWNERS-VALID`: paths that exist and owners that exist (L6), for team profiles.
  L1 · fix J · trial.
- [ ] **GV19** `NO-FORCE-PUSH-ON-MAIN`: force pushes and deletions blocked on the release and
  integration branches (L6, ion-repo#T-158). L6 · fix J · adopt.
- [ ] **GV20** `STALE-BRANCHES`: branches merged long ago and still on the remote (`/kiln:cleanup`,
  for the forge). L6 · fix S · assess.
