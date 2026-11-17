# ion-repo#T-233 · Safe pipelines: secrets through `env`, pinned reusable workflows, provenance
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (CI/CD), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.22, "Fast and safe pipelines": Concurrency, caches and retention, supported runners,
secrets through `env:`, reusable workflows pinned, provenance on what ships, the same CI on a
laptop.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CI18** `SECRETS-THROUGH-ENV`: `${{ secrets.X }}` passed through `env:`, never inlined in
  `run:`. L2 · fix S · adopt.
- [ ] **CI19** `REUSABLE-WORKFLOWS-PINNED`: `uses: org/repo/.github/workflows/x.yml@<sha>`
  (`PINNED-ACTIONS` extended); kiln's own workflows, cited by tag and moved by `kiln update`, stay
  one accepted way. L1 · fix S · adopt.
- [ ] **CI20** `ACTIONS-UPDATED`: the `github-actions` ecosystem in the update bot's config
  (`DEPENDENCY-UPDATES` per ecosystem). L1 · fix S · adopt.
- [ ] **CI22** `MATRIX-COVERS-SUPPORT`: a library's CI matrix covers the versions it claims
  (`requires-python`, `engines`). L1 · fix S · trial.
- [ ] **CI23** `PROVENANCE`: release artifacts attested (`actions/attest-build-provenance`, PyPI's
  attestations); ion-repo#T-90 asks it of kiln. L1 · fix S · trial.
- [ ] **CI24** `BUILD-ONCE`: the artifact deployed is the one tested (an image promoted by digest),
  never rebuilt per environment. L2≈ · fix J · assess.
- [ ] **CI25** `CI-REPLAYABLE`: the CI's commands run on a laptop too (`kiln ci`, `make ci`, `just
  ci`). L1≈ · fix J · trial.
