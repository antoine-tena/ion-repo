# ion-repo#T-438 · `ion repo dev` sees the servers of every worktree
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, about twenty requests in one week (`c2c71dc7` 23:09, `782aab61` 22:18, `84c464f5` 22:35, `c32f0fa0` 17:03)

- [ ] `ion repo dev status --all`: port, worktree, RAM, age, for this repo's worktrees.
- [ ] `ion repo dev stop --others`, and `--port` to choose a port.
- [ ] The preview and `.playwright/config` take the port of this worktree's server: a capture was taken on another worktree's server.
- [ ] A server that stopped by itself is said so, instead of `ERR_CONNECTION_REFUSED` in the middle of a capture.
- [ ] Seen again: port 3000 changes hands between worktrees and no one knows which serves it (`e1809a16` 22:21, `0552c55c` 18:41); servers left running 24 h pushed the load to 22 on 16 cores (`7abae8b7` 20:41).
