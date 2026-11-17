# ion-repo#T-450 · Django dev server without persistent connections, watcher limited to the apps
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, `0c146271` 15:34, `68ba0f22` 23:33, `59e47f9e` 23:32 (`too many clients`), `7abae8b7` 20:46 (68% CPU)

- [ ] `ion repo dev` runs `runserver` with `DATABASE_CONN_MAX_AGE=0`: one thread per request otherwise fills Postgres.
- [ ] The worker's `watchfiles` watches the app folders, not all of `backend/` (caches, media); `--ignore-paths` does not reduce the load: about 12% instead of 68%.
