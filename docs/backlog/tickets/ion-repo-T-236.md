# ion-repo#T-236 · No new finding: history, the score of a change, `--compare`, PR comments
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Scoring model v2, Speed, Nothing to do, Outputs
  and integrations, History, forge and registries, One measure drives every command), made a ticket
  on 25 October 2026 at antoine's request

Planned in v0.6.24, "Progress, not perfection: no new finding": The score of a change, a comparison
with any ref, gates on new findings only, scores kept in git notes and drawn as a curve.

- [ ] **I12** `kiln score --history`: the score at each tag or merge (cheap with the cache), drawn
  as a curve; "41 to 78 since adoption".
- [ ] **I13** The score of a change: "this branch takes the score from 74 to 76; 1 new finding, 3
  fixed". The gate is "no new finding", never an absolute number.
- [ ] **J23** `--first` for hooks: stop at the first critical finding.
- [ ] **K09** Exit code 0 by default, since it is a measure; gates are explicit: `--fail-under 80`,
  `--fail-on critical`, `--no-new` against a baseline or the integration branch.
- [ ] **L08** `--compare <ref or report.json>`: new, fixed and still-open findings, the delta, the
  rules that started or stopped applying.
- [ ] **L09** Pull request comments by the action: the delta, new findings as review comments on the
  diff's lines, fixed ones thanked.
- [ ] **L11** Scores kept in git notes (`refs/notes/kiln-score`), as `kiln ci` keeps its verdicts:
  history for free, travelling with the repo when pushed.
- [ ] **M30** `--at <ref>`: the repo scored as it was at a tag or a commit (a throwaway worktree,
  cached).
- [ ] **P10** `kiln check` includes "no new finding against the integration branch".
