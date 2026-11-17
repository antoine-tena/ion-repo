# ion-repo#T-297 · Packages that behave: typed exports, engines, one version source, CLIs
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Packaging and publishing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.60, "Libraries and CLIs that publish cleanly": Trusted publishing with attestations,
complete metadata, one version source, typed exports, packages that hold what they should and
nothing else.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PK08** `TYPED-EXPORTS`: package.json `exports` with `types` conditions; publint and
  arethetypeswrong clean. L4 · fix J · trial.
- [ ] **PK09** `ENGINES-DECLARED`: `engines.node` and `requires-python` set and matching the CI
  matrix. L1 · fix S · adopt.
- [ ] **PK10** `VERSION-SINGLE-SOURCE`: the version in one place, the manifest or the tag
  (hatch-vcs, setuptools-scm). L1 · fix J · trial.
- [ ] **PK11** `CLI-ENTRY-POINTS`: command-line tools declared in `[project.scripts]` or `bin`, with
  `--version` and `--help` that work (L7). L1 · fix S · trial.
- [ ] **PK12** `DEPRECATION-POLICY`: a deprecation warns for at least one release before the removal
  (`DeprecationWarning`), and the docs say so. L2≈ · fix J · assess.
- [ ] **PK13** `REPRODUCIBLE-BUILD`: `SOURCE_DATE_EPOCH` honoured; two builds give the same hash
  (`--deep`). L7 · fix J · assess.
