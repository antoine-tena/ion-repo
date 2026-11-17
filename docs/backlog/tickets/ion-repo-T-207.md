# ion-repo#T-207 · The grid's data dated at each release: end of life, grid diff, consistency, proposals
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Rule format v2 and authoring, A
  grid that stays current), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.3, "The grid kept current: its sources watched": Every week the sources are read,
the data bundle refreshed, the rules whose sources moved flagged; each release note carries the
grid's diff.

- [ ] **B22** End of life for every product endoflife.date covers (runtimes, frameworks, databases,
  distributions, Kubernetes, CI runners), bundled at each release, refreshed by `--online`.
- [ ] **G12** `level_history`: when and why the rule moved on the radar, with the evidence
  (precision, sources). An auditable radar.
- [ ] **Q01** A data bundle per release, dated and shown by `kiln score --version`: end-of-life
  dates, deprecated and malicious packages, retired CI runners and commands, retired LLM model IDs,
  provider secret patterns.
- [ ] **Q06** A grid diff in each release note: rules added, promoted, demoted, retired.
- [ ] **Q10** A consistency check: no two rules contradict (examples cross-run: a pass example of
  one never fails another).
- [ ] **Q11** A `grid-proposal` issue template (a practice with its sources), triaged by the
  doctrine.
- [ ] **Q12** The decision behind each rule kept with it (why adopt, why now), like an architecture
  decision record.
