# ion-repo#T-193 · `kiln score` benchmarked: a startup budget, a lean path, slow candidates stopped
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Speed), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.5.8, "kiln never makes you wait": The same features, sooner: what was measured slow on
24 October (the suite every release waits for, the session start, `kiln status`, each Bash call, the
install), and the score's own start, benchmarked in CI.

- [ ] **J01** Measure first: `kiln score --profile` (time per phase: listing, model, each rule,
  output; the ten slowest rules) and a benchmark suite (an empty repo, kiln, a copy of the reference
  repo, a 50,000-file monorepo, a synthetic million-file tree) in CI, with thresholds.
- [ ] **J02** Startup measured (`-X importtime`) and budgeted (80 ms to the first line): `urllib`
  imported only for `--online` (60 ms today), copier and Jinja never imported by `score`.
- [ ] **J03** A lean path: the score's dependencies kept minimal, so `uvx kiln-cli score` downloads
  little on a first run; the template's dependencies only for `new`, `adopt` and `update`.
- [ ] **J21** A candidate more than 10 % slower on the suite waits for an explanation.
