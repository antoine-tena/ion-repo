# ion-repo#T-237 · One funnel for every repo: baselines, `kiln adopt` scored before and after
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine, One
  measure drives every command), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.25, "One funnel for every repo, new or old": `kiln adopt` as score, lay, fix,
roadmap, its result shown before it runs; baselines for the gradual path; the template a repo
started from recognised; `kiln new` as the same funnel run on an empty folder.

- [ ] **A38** The template a repo started from, fingerprinted (kiln, cookiecutter-django,
  create-next-app, `nuxi init`, `rails new`, Spring Initializr, the Laravel installer): what that
  template changed since can be compared.
- [ ] **E25** Baselines: `kiln score --baseline` records today's findings, and from then on only new
  ones fail a gate. The progressive path of doctrine 9 for any repo, not only kiln's.
- [ ] **P03** The radical form: `kiln new` as an empty folder, then `kiln adopt`, then `kiln fix`.
  The template and the converters can't drift apart.
- [ ] **P06** `kiln adopt` as a funnel: score before, lay files, `kiln fix`, score after, roadmap
  tickets; each step a commit on its branch.
- [ ] **P07** `kiln adopt --dry-run` shows the score it would reach.
