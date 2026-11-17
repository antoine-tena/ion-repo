# ion-repo#T-275 · Sensitive data found by itself, encrypted, isolated per tenant
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Application security),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.45, "Personal data, the GDPR way": Personal fields found in the models and kept out
of logs, URLs, fixtures and model calls; the inventory and the subprocessors written by script;
retention and deletion.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A17** Domain facts from code and dependencies: money (Decimal fields named price, Stripe),
  personal data (user models, e-mail fields), uploads, e-mail sending, payments, LLM calls (the
  anthropic and openai SDKs). They switch on MONEY, PERSONAL-DATA, AI-FEATURES and their kin without
  a question.
- [ ] **AS10** `ENCRYPTION` (draft): sensitive fields encrypted at rest. L2≈ · fix J · assess.
- [ ] **AS11** `ROW-LEVEL-SECURITY` (draft, Postgres): RLS policies in migrations for multi-tenant
  tables. L2≈ · fix J · assess.
