# ion-repo#T-224 · Nothing downloaded blind: curl pipes, checksums, binaries, tokens in config
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Supply chain), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.17, "Nothing runs that you didn't pin": Install scripts off, one index, tools and
hooks pinned, downloads checked, no token in a committed `.npmrc`, no binary in the tree, an SBOM
per release.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SU22** `NO-CURL-PIPE-SHELL`: no `curl … | sh` in Dockerfiles, CI or setup scripts: download,
  verify, then run. L1 · fix J · adopt (review in READMEs).
- [ ] **SU23** `CHECKSUMS-FOR-DOWNLOADS`: binaries fetched in Dockerfiles and CI checked against a
  SHA-256. L1≈ · fix S (online) · trial.
- [ ] **SU29** `VENDORED-JS-VULNERABILITIES`: front-end libraries copied into static folders
  (jQuery, Bootstrap, Moment and the rest) matched against retire.js's signatures. L1 · fix J ·
  adopt.
- [ ] **SU34** `NO-HTTP-INDEXES`: package indexes and registries over HTTPS only (`.npmrc`,
  `pip.conf`, `uv.toml`, Maven's `settings.xml`). L1 · fix S · adopt.
- [ ] **SU35** `NO-TOKENS-IN-NPMRC`: no auth token in a committed `.npmrc` or `.pypirc`. L1 · fix J
  · adopt, critical.
- [ ] **SU36** `NO-BINARY-ARTIFACTS`: no executable, `.jar`, `.class`, `.dll` or wheel committed
  outside declared fixtures (Scorecard's Binary-Artifacts). L0 · fix J · adopt.
