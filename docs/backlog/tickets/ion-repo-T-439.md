# ion-repo#T-439 · See and merge several worktrees at once
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, six requests with a table rebuilt by hand (`23395c39` 19:40, `b1e53646` 13:04, `2d6ab461` 08:10, `d0318e7e` 18:55)

- [ ] A command (not `git -C`, which an isolated session refuses; one session exported each tree to `/tmp` to compare): per worktree, commits ahead, uncommitted files, server, last activity, verdict.
- [ ] `/repo:merge` or `/repo:cleanup` takes the chosen batch: merge these, delete those, leave the rest.
- [ ] Nothing is ever said clean without a real `git status`: file dates gave a wrong table.
