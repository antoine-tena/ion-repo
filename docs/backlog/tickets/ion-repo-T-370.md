# ion-repo#T-370 · Worktree cleanup decided by a script: safe, review, protected, undo
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026 (`sauravpanda/bonsai`)

Planned in v0.5.14, "Repos safe to hand to an agent". `/kiln:cleanup` has Claude put together the
`git worktree remove` and `git branch -d` commands itself; one wrong flag deletes work that exists
nowhere else.
- [ ] A `kiln cleanup` command classifies each worktree and branch: `safe` (merged, clean,
  pushed), `review`, `protected` (dirty, unpushed commits, locked, current, in use by a session,
  an open pull request), with the disk space each one frees.
- [ ] It removes only `safe` ones, keeps what it removed for `kiln cleanup --undo`, and gives
  `--json` for the skill; `/kiln:cleanup` calls it instead of composing git commands.
- [ ] Both references and both READMEs updated in the same branch.
