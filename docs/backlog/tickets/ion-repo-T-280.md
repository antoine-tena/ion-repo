# ion-repo#T-280 · History: commit habits, signatures, release rhythm, regression tests
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (History, forge and registries, Tests), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.48, "History: how the repo is worked": Commit sizes and messages, merges and branch
names, releases and their notes, fixes that come with a test, all read from history.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **M03** Commit habits over the last 90 days (Conventional Commits share, size distribution):
  SMALL-COMMITS and a commit-message rule promoted on facts.
- [ ] **M04** Signed commits and tags (GPG, SSH, gitsign), as a share.
- [ ] **M05** Direct commits on the integration branch (first-parent commits that aren't merges):
  NO-COMMIT-ON-INTEGRATION from history.
- [ ] **M06** Merge style (MERGE-COMMITS) and branch names (BRANCH-NAMES) from history.
- [ ] **M07** Release rhythm from tags: the last release's age, semver tags, a changelog entry per
  tag (RELEASE-NOTES).
- [ ] **M11** `fix:` commits that come with a test change (REGRESSION-TEST from history).
- [ ] **TE10** `REGRESSION-TEST` (draft): `fix:` commits of the last hundred that touch no test,
  with `--history`. L5 · ratchet · trial.
