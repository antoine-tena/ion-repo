# ion-repo#T-369 · Worktrees ready however they are made: a `WorktreeCreate` hook, a port per worktree
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026
  (`tfriedel/claude-worktree-hooks`)

Planned in v0.5.17, "Strangers' repos run as they are". Only `/kiln:worktree` runs
`prepare-worktree.sh`; a worktree made by `claude --worktree` starts empty, and two `kiln dev` in
two worktrees ask for the same ports.
- [ ] A `WorktreeCreate` hook creates the worktree the way `/kiln:worktree` does and prepares it
  (ignored `.env*` copied, dependencies installed, `.claude/worktree-setup.sh`); `WorktreeRemove`
  undoes what it laid.
- [ ] A port offset per worktree, derived from its name, so the same worktree always gets the
  same ports; `kiln dev` and the copied `.env*` use it.
