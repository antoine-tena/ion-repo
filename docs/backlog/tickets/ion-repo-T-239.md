# ion-repo#T-239 · The score explained like a senior engineer would
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Rule format v2 and authoring, Scoring model v2,
  Nothing to do), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.27, "The score explained like a senior engineer would": The denominator, the weakest
themes, the effort to 100 in session hours, a verdict in plain words, `--explain` with this repo's
numbers.

- [ ] **G06** `effort` per place and per rule, in session minutes, and `impact`: the roadmap's order
  and the effort-to-100 estimate come from them.
- [ ] **I05** Scores per component and per theme, under the five pillars; under each pillar, its
  weakest themes (decision 5).
- [ ] **I06** The denominator explained: "31 rules apply: Python, Django, Docker, GitHub Actions"; a
  new Dockerfile says "5 more rules apply now, 2 met".
- [ ] **I08** Effort to 100 from the rules' effort estimates, in session hours, the backlog's unit.
- [ ] **I16** Remediation time in hours per rule and in total: a debt figure for practices.
- [ ] **I17** `kiln score --explain`: the formula with this repo's numbers in it.
- [ ] **I18** One function computes the score everywhere (CLI, badge, bot, fleet, HTML), with golden
  tests.
- [ ] **I19** The score model versioned (`score_model` in the JSON); a change re-scores the
  reference repos and the release note says its effect.
- [ ] **I20** "Rules met" stays on the first line (24 of 31): plainer than a percentage for a
  newcomer.
- [ ] **I21** A verdict in plain words generated from the findings, no model needed: "well tested,
  but the supply chain is open: unpinned actions and images, no update bot".
- [ ] **K15** Explanations a newcomer understands (one sentence, no jargon) and `--explain` for the
  details: "like a senior engineer would, even if you're not one".
