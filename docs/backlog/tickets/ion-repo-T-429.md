# ion-repo#T-429 · `/repo:release` readies its worktrees before pushing and deploying
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-03
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03, two releases of a Django + Nuxt
  production repo (16:09, 21:34–21:43)

Step 7 creates `.claude/worktrees/main` bare: no `node_modules`, no backend `.env`, no `.vercel/`
link (all outside git). The pre-push hooks then fail (eslint not found, `SECRET_KEY` missing),
and `vercel --prod` answers "Not authorized"; each time the session copied them by hand. The
release worktree hit the same wall at its first push.
- [ ] The release and `main` worktrees get what `/repo:worktree` gives a new worktree (frozen
  offline installs, the git-excluded local files the project lists), before the first push.
- [ ] Reproduced on a copy: a release of a generated Nuxt + Django repo pushes `main` and runs
  its deploy script without a manual copy.
- [ ] Seen again 2026-11-04 to 2026-11-08: seven commits or pushes failed for lack of `node_modules` in a release or hotfix worktree (`b9d8b288` 14:57), and after a merge adding a dependency the main tree's pre-push failed too (`three`, 19:42): reinstall there when the lockfile changed. The OpenAPI hook also needs `SECRET_KEY` (`d92265f7` 22:46).
