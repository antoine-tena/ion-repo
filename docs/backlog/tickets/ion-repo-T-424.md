# ion-repo#T-424 · `/repo:merge` stops the worktree's servers and leaves it before removing it
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, ion-repo (18:10) and a Nuxt site (22:15)

Two endings went wrong: removing the worktree that was still the shell's directory ("The current
working directory was deleted"), and removing one where a dev server still ran ("Directory not
empty", processes killed by hand, then `rm -rf` and `git worktree prune`). Before `git worktree
remove`: stop what `ion repo dev` started from that worktree, and run the removal from the main
tree.
- [ ] Both cases reproduced on a copy, then gone.
