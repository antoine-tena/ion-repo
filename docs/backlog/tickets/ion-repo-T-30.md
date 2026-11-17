# ion-repo#T-30 · README and English docs for strangers, with the demos already recorded
- **Type**: task
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-16
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: ion-repo#T-03 prerequisites; issues #37 and #38; rewritten 17 October 2026 for the vision

- [x] Today's README brought to the level of the best (20 October 2026, branch
  `docs/showcase`), after measuring the READMEs of 70 repos of 10,000 stars or more (uv, ruff,
  Bun, ripgrep, fzf, mise, Claude Code…): the pixel kiln on top, one promise, three badges that
  measure something (beyond five, popular npm packages get fewer downloads: Trockman et al.,
  ICSE 2018), a recorded demo first, plain bullets, the words of a visitor, a comparison where
  the others win rows too; the help screen, the rule list and the update note moved to the
  reference. `tests/test_docs.py` now fails on the marks readers take for AI writing (em dashes,
  list items opened in bold or by an emoji, sales words), on a README whose images or links
  would break on PyPI, and on a demo that types what kiln no longer offers.
- [x] Demo recorded with vhs (`docs/assets/kiln-new.tape`, `scripts/demo_shell.sh`): `kiln new`,
  its three questions, then `kiln check` on the new repo; replayed before each candidate.
- [ ] v0.5.0 first screen: the promise (ion-repo#T-33), `uvx kiln-cli score`, then the demos already
  recorded (antoine, 30 October 2026: no study, no new demo); then how it works in five
  steps (score, fix, roadmap for Claude, verified by the script, continuous), the grid, and
  "Built for Claude Code; the score and the fixes need no AI at all".
- [x] A second tape (24 October 2026, `docs/assets/kiln-rescue.tape`): on the public
  `antoine-tena/kiln-demo-legacy`, a Django app kept deliberately outdated (never a team's
  project shown at fault), `kiln score` 23, `kiln adopt` 39, `kiln fix` 65, the roadmap, a real
  Claude Code on `/kiln:modernize` as a time-lapse (about ten minutes), `kiln score` 100. The
  `kiln new` tape now ends on `kiln score` at 100/100.
- [ ] The kiln-bot pull request in the rescue tape, once kiln-bot exists (ion-repo#T-59).
- [ ] Docs in English in `docs/`: getting started, score, fix, modernize, the grid (one page per
  theme generated from the rule files: the Technology Radar that applies itself), update,
  charter, plugins, workflows, versions, in English only (ion-repo#T-177). Closes #37 and #38 (another
  good first issue opened instead).
- [ ] A comparison page, facts only: what Dependabot and Renovate, Copier and cruft,
  sp-repo-review, OpenRewrite, AWS Transform and Claude Code's `/doctor` do, and what kiln adds
  (from the vision's market table); the r/Python Showcase format asks for it (ion-repo#T-03).
- [ ] `kiln new` second: "Starting a repo? It starts at 100."
- [ ] From the decisions of 26 October 2026: `kiln score` first, then `kiln adopt`, then `kiln new`
  (decision 4); "the kiln standard" (ion-repo#T-346); no Ubuntu image; one line each for `kiln check`,
  `kiln ci` and `kiln score` (decision 40); the review gap as the sourced why (decision 8); the
  score in Lighthouse's bands (decision 6); `uvx` first.
- [ ] The default branch becomes `main` with v0.5.0, so the repo page and `claude plugin
  marketplace add` show what `uvx kiln-cli` installs; pull requests still go to `develop`
  (CONTRIBUTING).
