# ion-repo#T-415 · Django template: error reporting off by default, nothing personal sent
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/backend/core/observability.py`

Sentry (or GlitchTip, self-hostable, same protocol) inactive while `SENTRY_DSN` is empty: no
network call; when on, no cookie, header or personal field sent. Taken from
`annski/backend/core/observability.py` into the template's settings.
