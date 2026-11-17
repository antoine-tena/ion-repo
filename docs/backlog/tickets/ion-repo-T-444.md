# ion-repo#T-444 · Optional files make worktree and merge steps look failed
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, every worktree created or merged on 2026-11-08 (`93e47f94` 10:59, 11:00, `589b4e45` 11:21)

- [ ] `ls .claude/worktree-setup.sh` and `ls .claude-plugin` exit 2 when absent, so a good step reads as an error: the skills test with `[ -e ]`.
