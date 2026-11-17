# ion-repo#T-294 · Licences right: files, manifests, notices, assets, community health
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, History, forge and
  registries, Licensing), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.59, "Open source done right": A licence that says the same everywhere, notices kept,
contributing, conduct and security policies, issue forms, sponsors, the OpenSSF badge.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F17** The REUSE tool and a licence detector in licensee's manner for the licensing theme.
- [ ] **M25** Community health from the forge (README, licence, conduct, contributing, templates)
  and maintainers' responsiveness (median first response), for open-source profiles.
- [ ] **LI02** `LICENSE-DECLARED`: the manifest's licence as an SPDX expression (`license = "MIT"`
  with PEP 639, package.json's `license`). L1 · fix S · adopt.
- [ ] **LI03** `LICENSE-CONSISTENT`: the file, the manifests and the README say the same licence. L1
  · fix J · adopt.
- [ ] **LI05** `THIRD-PARTY-NOTICES`: vendored code keeps its licence and notice. L1 · fix J ·
  adopt.
- [ ] **LI06** `ASSETS-LICENSED`: fonts, images and icons committed with their licence or source (a
  font's OFL file). L0≈ · fix J · trial.
- [ ] **LI07** `SPDX-HEADERS`: REUSE-compliant headers or a `REUSE.toml`, for projects that want
  them. L1 · fix S · assess.
- [ ] **LI08** `SIGN-OFF`: contributions under a DCO sign-off or a CLA, for profiles that need one.
  L5 · fix J · assess.
