# ion-repo#T-377 · An agent cannot document a new variable: `.env.example` is under the `.env*` deny
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: emberstudio session `feat/auth`, 30 October 2026 (see also AI02, ion-repo#T-369)

The permission rules deny reading and editing `.env*`; `.env.example` matches, though it holds no
secret by design ([SECRETS]) and the generated README sends people to it. The session added
`DJANGO_JWT_SIGNING_KEY` and `DJANGO_FRONTEND_URL` and could neither copy the example to a local
`.env` (`cp` refused) nor add the two lines to it: they ended up in `production.md` only, and the
user has to add them by hand.
- [ ] The deny excludes `*.example` (and `.env.sample`), in kiln's settings and in AI02's check.
- [ ] OP07 `ENV-EXAMPLE-COMPLETE` would then be reachable by an agent.
