# ion-repo#T-296 · Packages published cleanly: trusted publishing, attestations, contents
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Packaging and publishing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.60, "Libraries and CLIs that publish cleanly": Trusted publishing with attestations,
complete metadata, one version source, typed exports, packages that hold what they should and
nothing else.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PK01** `TRUSTED-PUBLISHING`: PyPI and npm publish through OIDC trusted publishing, no
  long-lived token. L1 · fix S · adopt.
- [ ] **PK02** `ATTESTATIONS`: PyPI attestations (PEP 740) and npm provenance on published packages.
  L1 · fix S · trial.
- [ ] **PK03** `RELEASE-WORKFLOW`: publishing only from CI, on a tag, in a protected environment. L1
  · fix S · adopt.
- [ ] **PK04** `NPM-FILES-ALLOWLIST`: `files` in package.json so nothing private ships (`npm pack
  --dry-run` with `--deep`). L1 · fix S · adopt.
- [ ] **PK05** `PYPROJECT-METADATA`: `[project]` with name, version source, `requires-python`,
  licence expression, readme and URLs. L1 · fix S · adopt.
- [ ] **PK06** `NO-SETUP-PY`: a PEP 517 backend declared in `pyproject.toml`; `setup.py` kept only
  for C extensions. L1 · fix J · trial.
- [ ] **PK07** `PACKAGE-CONTENTS`: the sdist holds the tests and the licence, the wheel holds
  neither tests nor secrets (`--deep` builds both). L7 · fix J · trial.
