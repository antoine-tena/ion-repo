# ion-repo#T-232 · Fast pipelines: concurrency, caches, runners, actionlint, zizmor
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

- [ ] **CI07** `CI-CONCURRENCY`: `concurrency:` with `cancel-in-progress` on pull-request runs. L1 ·
  fix S · adopt.
- [ ] **CI09** `CI-CACHES`: dependency caches on (setup-uv's `enable-cache`, setup-node's `cache`).
  L1 · fix S · adopt.
- [ ] **CI11** `ARTIFACT-RETENTION`: `retention-days` on uploaded artifacts. L1 · fix S · trial.
- [ ] **CI12** `SUPPORTED-RUNNERS`: no runner image GitHub has retired (`ubuntu-20.04` in 2025,
  older macOS ones), a calendar like the runtimes'. L1 · fix S · adopt.
- [ ] **CI14** `ACTIONLINT`: actionlint passes (expressions, types, the shellcheck it embeds). L4 ·
  fix J · adopt.
- [ ] **CI15** `ZIZMOR-CLEAN`: zizmor's audits pass, run by kiln or in CI. L4 · fix J · trial.
- [ ] **CI17** `CACHE-POISONING`: release workflows restore no cache that pull requests can write
  (zizmor's cache-poisoning). L4 · fix J · trial.
