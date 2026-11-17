# ion-repo#T-423 · `/nuxt:preview` needs `@playwright/test`, which a generated site lacks
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, two sessions on a Nuxt site (18:05, 18:18)

`node plugins/nuxt/scripts/preview.mjs` fails with "Cannot find module '@playwright/test'": the
generated Nuxt project does not depend on it, so each session falls back on the Playwright MCP by
hand. Either the template adds `@playwright/test` to the dev dependencies, or the script runs from
the plugin's own install (`npx -y`), without touching the project.
- [ ] `/nuxt:preview` works on a fresh `ion repo new` Nuxt site.
- [ ] The skill says where the Playwright MCP may write: `.playwright/captures/` of the project; it
  refuses `/tmp` ("outside allowed roots"), which sessions tried each time.
- [ ] Seen again: twelve `Read` calls failed on `.playwright/captures/` because the MCP writes under the main tree while the session sits in a worktree (`a23abff9` 22:06, `8b76df77` 13:23); the skill says which absolute path to read.
