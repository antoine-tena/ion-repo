# ion-repo#T-414 · Django template: payments behind a provider switch, through the Outbox
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/backend/core/stripe_client.py`, `annski/backend/core/helloasso_client.py`

annski takes payments with Stripe or HelloAsso, chosen by `PAYMENT_PROVIDER`
(`annski/backend/core/settings.py`), the other kept in reserve.
- [ ] Amounts in integer cents everywhere ([ARGENT]), helpers in `annski/backend/core/money.py`.
- [ ] Webhooks verified, recorded then handled in the Outbox, idempotent:
  `annski/backend/core/outbox/stripe_handlers.py`, refunds in
  `annski/backend/core/outbox/refunds.py` and `helloasso_refunds.py`.
- [ ] An optional module of the template (`ion repo set payments=…`), off by default.
  Score side: ion-repo#T-277.
