# ion-repo#T-219 · The corpus: precision and recall per rule at every candidate
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every ecosystem, Rule
  format v2 and authoring, Precision and recall, A grid that stays current), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.14, "Precision measured on a thousand repos": A labelled corpus re-scored at every
candidate, precision and recall per rule as a release gate, new detectors in shadow first; the radar
moves on that evidence only.

- [ ] **A35** A corpus for the model itself: 500 real trees (paths and manifests) with their
  expected model; each fact's precision tracked like a rule's.
- [ ] **B01** The order of ecosystems set by the corpus (share of repos, share of code), never
  assumed; Django and Nuxt stay the reference.
- [ ] **G14** `precision` and `prevalence` written by the calibration job (H), shown in `kiln grid
  ID` and on the rule's page.
- [ ] **G23** `shadow = true`: a new detector runs and records on the corpus and on beta machines
  without showing, for one release, before it counts.
- [ ] **H02** Labels from Claude in batches (20 places per rule, "to confirm"), spot-checked by
  antoine, stored by fingerprint; only aggregates in public, anything that names a project in
  `kiln-measures`.
- [ ] **H03** Precision and recall per rule at every candidate; a strict rule under 99 % precision,
  or any drop, stops the candidate (`kiln version cut`).
- [ ] **H04** Differential tests against reference tools (zizmor, Scorecard, gitleaks, ruff): each
  disagreement triaged into a kiln bug or a documented difference.
- [ ] **H12** Inline markers and waivers counted per rule across the corpus: the most-waived rules
  are examined first.
- [ ] **H14** Recall measured with seeded faults: secrets, unpinned images, root containers planted
  in copies of corpus repos must all be found.
- [ ] **H19** The corpus's labels versioned with the grid, so a rule's precision history is a plot,
  not a memory.
- [ ] **H20** A rule that flags more than half of the corpus is looked at twice: either the practice
  is rare (say so) or the detector is wrong.
- [ ] **Q03** Radar moves on evidence only: assess to trial needs a detector and examples; trial to
  adopt needs 99 % precision on the corpus (strict rules) and fresh sources; adopt to hold when the
  practice is superseded.
