# ion-repo#T-318 · Does the score mean anything? Seniors, incidents and tokens, measured
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Precision and recall, A grid that stays current,
  Measuring kiln score itself, What the grid doesn't know), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.9.1, "Does the score mean anything? Measured, on every stack": The last proof before
the stability promise, now that every stack is scored: ten senior engineers' ranking against kiln's,
the score against public repos' incidents, readability against tokens, each published whatever it
says.

- [ ] **H16** Seniors' agreement: ten senior engineers rank twenty repos, and kiln's order must
  agree with theirs (Kendall's tau of 0.7 or more). "Like a senior engineer would", measured.
- [ ] **Q09** A radar fed by the corpus: tools rising quarter after quarter become `assess`
  candidates, tools falling become `hold` candidates.
- [ ] **T04** Seniors' agreement (H) measured again each quarter.
- [ ] **T05** Does the score predict anything? Public repos' advisories and incidents against their
  score at the time: evidence for the launch's claim, or a humbling result to publish anyway.
- [ ] **T06** Does readability lower Claude's tokens? ion-repo#T-53's A/B test run again with the readability
  pillar's score as the variable.
- [ ] **U06** Suggestions from the corpus ("repos like yours, Django with Celery and Nuxt, usually
  also have X"): association rules mined from the corpus as `assess` candidates, never findings.
