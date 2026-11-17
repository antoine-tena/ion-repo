# ion-repo#T-422 · `/repo:release` checks the host's secrets against what the code reads
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, a site's session after its release (19:00)

Two variables the server code reads (`NUXT_*` in `.env.example`) had never been set as secrets of
the Cloudflare Worker: two features were down in production, before and after the release, and no
check saw it. Before promoting, list the names `.env.example` declares for production and the host's
secrets (`wrangler secret list`, the VPS's `.env` keys), names only, never values; a missing one
stops the release with the command that sets it (`/repo:token`, ion-repo#T-371).
- [ ] Names compared, values never read.
- [ ] A variable marked optional in `.env.example` only warns.
