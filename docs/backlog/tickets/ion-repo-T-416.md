# ion-repo#T-416 · Django template: Cloudflare Turnstile that fails open
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/backend/core/captcha.py`

An anti-bot check without friction or ad tracking on public forms (contact, sign-up, booking),
active only when `TURNSTILE_SECRET_KEY` is set; a Cloudflare outage never blocks a form.
Taken from `annski/backend/core/captcha.py`.
