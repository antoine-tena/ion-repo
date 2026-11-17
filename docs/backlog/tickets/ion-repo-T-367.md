# ion-repo#T-367 · No bulk staging: `git add -A`, `git add .` and `git commit -a` refused
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-27
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: review of similar public projects, 26 October 2026
  (`tillmeier/claude-code-guardrails`'s staging guard)

Planned in v0.5.14, "Repos safe to hand to an agent". "Commit only the task's files" is an
instruction today; the branch guard can make it mechanical.
- [ ] `branch_guard.py` refuses `git add -A`, `git add --all`, `git add .`, `git commit -a` and
  `git commit --all`, and says to name the files; with ion-repo#T-167, judged in the repo the command
  runs in.
- [ ] A test per form, and the forms that stay allowed (`git add -p`, a named path, `git add -u
  <path>`).
