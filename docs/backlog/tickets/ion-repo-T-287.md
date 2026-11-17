# ion-repo#T-287 · What the grid doesn't know, shown: every file claimed
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every ecosystem, Precision
  and recall, A grid that stays current, Trust, privacy and safety, Measuring kiln score itself,
  What the grid doesn't know), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.53, "What the grid doesn't know, shown": Every tracked file claimed by a fact or
listed, fingerprints as data from Linguist and SchemaStore, the gap reports carrying them,
corrections counted as signals.

- [ ] **A26** Language by content when the extension lies: shebangs, `.h` (C, C++ or Objective-C),
  `.m` (Objective-C or MATLAB), `.pl`, `.v`, `.ts` (TypeScript or Qt translations), with Linguist's
  heuristics as data.
- [ ] **B25** A stack the grid doesn't cover yet is scored on the universal rules and told which
  pack would cover it, and how many corpus repos share it: a reason to write the pack.
- [ ] **H11** Waivers as signals beyond renewals (reported since v0.4.6): "false positive" in a
  reason, or one rule waived across many repos of a fleet, flags the rule for review.
- [ ] **Q07** A coverage map, themes by ecosystems with the number of scored rules in each cell,
  holes visible (`kiln grid --coverage`).
- [ ] **S05** No silent telemetry: ion-repo#T-38's report, with consent and the exact lines shown, as
  v0.4.6 does, and the opt-in counts of ion-repo#T-348 (antoine reversed "no telemetry, ever" on
  26 October 2026); every later signal (U) goes through one of the two.
- [ ] **T02** User effort measured: manual corrections needed per 100 corpus repos for a right score
  (target 0).
- [ ] **T03** The unclaimed-file rate on the corpus (target under 1 % outside docs and assets).
- [ ] **U01** Every tracked file claimed by a fact (code, a known tool's config, docs, asset, data);
  the rest listed as "kiln doesn't know these", with counts.
- [ ] **U02** A fingerprint library as data, seeded from GitHub Linguist (languages, vendored and
  generated patterns), the SchemaStore catalogue (config names to tools), github/gitignore,
  endoflife.date's products, Renovate's managers (⚠ AGPL: facts only, no code), Dependabot's and
  OSV's ecosystems, the pre-commit hooks index (appendix D).
- [ ] **U03** `NOTABLE_PACKAGES` (28 names in `score.py` today) grown into data: the top packages of
  each registry with what they are, so the gap report names what matters ("celery: background tasks,
  4 drafts, 0 scored") and still never a private name.
- [ ] **U04** Practices found but unclassified (a `scripts/backup.sh`, a `docs/runbook.md`, a
  `chaos/` folder), named so the grid can learn them.
- [ ] **U05** ion-repo#T-38's report (v0.4.6: stacks, notable packages, misfiring rules) also carries the
  kinds of unclaimed files (a config's name, never a path) and the corrections users made; the most
  reported become tickets first, counted by `/kiln:backlog`.
