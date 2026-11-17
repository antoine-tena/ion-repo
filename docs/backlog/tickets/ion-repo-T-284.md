# ion-repo#T-284 · What you depend on, checked at the registry: vulnerabilities, malware, licences
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Speed, History, forge
  and registries, Supply chain, Licensing), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.50, "What you depend on, checked at the registry": Real vulnerabilities in the
locked versions, malicious and abandoned packages, typosquats, the provenance of what is published,
dependencies' licences, a health card for a new one.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **F09** osv-scanner, or OSV's batch API, for real vulnerability counts in the locked versions.
  VULNERABILITY-AUDIT checks today that an audit runs, not what it would find.
- [ ] **J19** `--online` calls in parallel, cached a day with ETags (endoflife.date, OSV, forge
  APIs), batched (OSV's `querybatch` takes hundreds of packages at once).
- [ ] **M26** Registries: trusted publishing and attestations on PyPI (PEP 740) and npm
  (provenance), checked on the published files.
- [ ] **M27** Registries: each dependency's health (last release, deprecated flag, yanked versions,
  archived source, a single maintainer) for ABANDONED-DEPENDENCIES.
- [ ] **M28** Registries: typosquat suspects (one edit from a popular name, few downloads) and known
  malicious packages (OSV's `MAL-` advisories).
- [ ] **SU03** `NEW-DEPENDENCY` (draft): a dependency added on a branch gets a health card in the
  pull request (maintainers, age, downloads, licence, install scripts). L6 · fix J · trial.
- [ ] **SU13** `MALICIOUS-PACKAGES`: no dependency known to be malicious (OSV's `MAL-`). L1 with
  data · fix J · adopt, critical.
- [ ] **SU14** `KNOWN-VULNERABILITIES`: no known critical or high vulnerability in the locked
  versions (OSV's batch query, or a cached database offline). L6 · fix S (bump within range) ·
  adopt.
- [ ] **SU15** `ABANDONED-DEPENDENCIES`: no dependency deprecated, yanked, archived, or three years
  without a release with open security issues. L6 · fix J · trial.
- [ ] **SU16** `TYPOSQUAT-SUSPECTS`: dependencies one edit from a popular name, with few downloads.
  L6 · fix J · trial.
- [ ] **SU37** `REPRODUCIBLE-LOCK`: the lock still resolves today (no yanked version, no dead URL),
  with `--online`. L6 · fix S · trial.
- [ ] **LI04** `DEPENDENCY-LICENSES`: licences of the locked dependencies compatible with the
  project's and its profile (no AGPL in a closed service without a decision), from the registries
  (L6) or a bundled cache. L6 · fix J · trial.
