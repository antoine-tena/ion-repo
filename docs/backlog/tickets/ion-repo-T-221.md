# ion-repo#T-221 · A number that can't lie: severity, the critical cap, confidence, anti-gaming
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Rule format v2 and
  authoring, Precision and recall, Scoring model v2, Trust, privacy and safety), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.15, "A number that can't lie": Severity orders the gaps, critical findings cap the
score at 49 once they are 99 % precise (decision 2), a maybe is never punished, an empty file earns
nothing, a report can be verified.

- [ ] **E26** Approximate detectors return candidates with a confidence: the roadmap sends the
  uncertain ones to Claude "to confirm" and the certain ones as gaps.
- [ ] **G05** `severity` (critical, high, medium, low, info), apart from `regime` (how it is
  enforced) and `level` (the radar).
- [ ] **H13** A confidence per finding (the rule's precision times its context: test file,
  generated, comment), shown as "certain" or "likely".
- [ ] **H18** Precision shown to users ("this rule is 99.4 % precise on 1,000 repos"): trust earned
  with numbers.
- [ ] **I01** A severity on each rule (critical, high, medium, low) that orders the gaps and marks
  the critical ones; it never weighs the number (decision 2).
- [ ] **I02** Critical findings cap the score at 49 (decision 2), each critical rule proven at 99 %
  precision first: a committed secret, `DEBUG = True` in production settings, `pull_request_target`
  checking out the pull request's code, the engine's socket mounted in a container. A repo that
  leaks its keys can't show 90.
- [ ] **I03** Progress shown per place, never as partial credit: "`IMAGES-BY-DIGEST`: 37 of 40
  pinned" beside the rule, so every fix shows while the number keeps meaning rules met (decision 2).
- [ ] **I04** Approximate findings not counted until Claude or the user confirms them: the score
  never punishes a maybe.
- [ ] **I14** Anti-gaming: presence rules check content (a README with install and usage, a
  SECURITY.md with a contact, tests that assert, CI that runs on pull requests and pushes). An empty
  file earns nothing.
- [ ] **S06** Reproducible: the report carries kiln's version, the grid's hash, the data's date and
  the commit; `kiln score --verify report.json` runs again and compares.
