# ion-repo#T-432 · `ion repo ci --status` tells an interrupted run from one never run
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, a release whose first CI died
  midway (20:39)

The run's process was gone, its logs stopped at 7 % of pytest, its worktree stayed in
`~/.cache/kiln/ci/` with its `.pid`, and `--status` said "never replayed": the session had to
find the logs to understand, and nearly took the copy for a leftover.
- [ ] `--status` reads the `.pid` and the logs: "interrupted at <job>, <time>" when the process
  is dead without a verdict.
- [ ] The next run of the same commit removes the dead run's worktree; `/repo:cleanup` lists
  `~/.cache/kiln/ci` copies as the CI's, not as agents'.
