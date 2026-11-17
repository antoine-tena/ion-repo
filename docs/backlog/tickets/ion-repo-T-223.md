# ion-repo#T-223 · Nothing runs unpinned: install scripts, indexes, git dependencies, tools
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Supply chain), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.17, "Nothing runs that you didn't pin": Install scripts off, one index, tools and
hooks pinned, downloads checked, no token in a committed `.npmrc`, no binary in the tree, an SBOM
per release.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SU01** `SBOM` (draft): an SBOM (CycloneDX or SPDX) made in the release workflow (syft,
  cdxgen, the package manager). L1 · fix S · trial.
- [ ] **SU10** `NO-INSTALL-SCRIPTS`: npm lifecycle scripts off by default (`ignore-scripts`, pnpm's
  `onlyBuiltDependencies` allowlist, Bun's trusted dependencies); the 2025 npm worms spread through
  install scripts. L1 · fix S · adopt.
- [ ] **SU11** `ONE-INDEX`: Python packages from one index, no `--extra-index-url` (dependency
  confusion); uv's pinned indexes for private packages. L1 · fix S · adopt.
- [ ] **SU12** `GIT-DEPS-PINNED`: dependencies fetched from git pinned to a commit, never a branch.
  L1 · fix S (online) · adopt.
- [ ] **SU18** `NO-DUPLICATE-MAJORS`: one package in several major versions in a JS lock. L1 · fix S
  (dedupe) · trial.
- [ ] **SU20** `PINNED-PRE-COMMIT`: pre-commit hooks pinned by commit (`autoupdate --freeze`). L1 ·
  fix S · adopt.
- [ ] **SU21** `PINNED-TOOLS`: tools run through `npx`, `uvx`, `pipx run` or `go run` in CI and
  scripts carry a version. L1 · fix S · adopt.
