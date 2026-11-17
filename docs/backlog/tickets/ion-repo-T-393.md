# ion-repo#T-393 · The grid leaves ion-repo for ion-score
- **Type**: task
- **Priority**: 🟠 important
- **Status**: in progress — branch refactor/grid-to-ion-score, since 2026-11-02
- **Opened**: 2026-10-30
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: ion-repo#T-387. ⚠ breaking only if a charter rule ID or a command changes: neither does

antoine, 2 November 2026: the whole grid moves (fixers, roadmap and gap report included), ion-repo
depends on the `ion-score` package, no subprocess; ion-score also holds the ground both share
(`ui`, `shell`, waivers, rule IDs).

- [x] ion-repo depends on `ion-score`; `src/ion_repo/grid/` gone, with its history in ion-score.
- [x] `cli.py`, `adopted.py`, `update.py`, `bot.py`, `charter/cli.py` import `ion_score`; `ion repo
  grid|score|fix` build on `ion_score.cli`; the grid's tests live in ion-score, `test_grid_rules.py`
  (grid vs template) stays here.
- [x] `ion repo score` gives the same result, rule by rule, on the training repos (four copies).
- [ ] ion-score on PyPI and public before the next ion-repo release: until then the dependency is a
  git source on a private repo, which this public repo's CI and PyPI's wheel cannot install.
