# ion-repo#T-425 · `ion repo dev status|stop` miss the server they started on an Astro site
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, ion-deal session on a copy in `ion-repo-sandbox` (18:24)

On an Astro site made by `ion repo new`, `ion repo dev` started the server (HTTP 200 on 4321), yet
`status` said stopped and `stop` said "nothing was running"; it was killed by hand. Reproduce on a
fresh Astro site in `ion-repo-sandbox`, find why the process is not recorded.
- [ ] `status` and `stop` see the Astro server.
