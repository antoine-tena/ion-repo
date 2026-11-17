# ion-repo#T-276 · Personal data the GDPR way
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Personal data, AI-assisted development), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.45, "Personal data, the GDPR way": Personal fields found in the models and kept out
of logs, URLs, fixtures and model calls; the inventory and the subprocessors written by script;
retention and deletion.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PD01** `PERSONAL-DATA` (draft): fields holding personal data (e-mail, phone, address, birth
  date, IBAN, IP) marked as the charter marks them; unmarked ones listed. L2 · fix J · trial.
- [ ] **PD02** `PII-INVENTORY`: an inventory of personal-data fields written from the models
  (`docs/personal-data.md`) and kept current by a script. L2 · fix S · trial.
- [ ] **PD03** `NO-REAL-PII-IN-FIXTURES`: fixtures and seeds hold fake data (real-looking e-mails on
  real domains, phone numbers flagged). L2 · fix J · adopt.
- [ ] **PD04** `NO-PII-IN-URLS`: no e-mail or name in query strings. L2≈ · fix J · trial.
- [ ] **PD05** `NO-PII-IN-LOGS`: personal fields passed to log calls (the charter's ban, promoted).
  L2 · fix J · adopt.
- [ ] **PD06** `RETENTION`: a job deletes or anonymizes data past its retention period. L2≈ · fix J
  · assess.
- [ ] **PD07** `DATA-EXPORT` and `ACCOUNT-DELETION`: users can get and delete their data (GDPR
  articles 15, 17 and 20), for profiles holding accounts in the EU. L2≈ · fix J · assess.
- [ ] **PD08** `CONSENT-BEFORE-TRACKING`: analytics and trackers load after consent, or are
  cookieless (Plausible, Matomo set so). L2 · fix J · trial.
- [ ] **PD09** `SELF-HOSTED-FONTS`: no fonts from Google's CDN (a German court awarded damages over
  it under the GDPR in 2022); `@nuxt/fonts` or local files. L2 · fix S · adopt (EU).
- [ ] **PD10** `SUBPROCESSORS-LISTED`: the third parties receiving data (Sentry, Stripe, a mail
  provider) listed from dependencies and settings, ready for the privacy policy. L1 · fix S ·
  assess.
- [ ] **PD11** `MINIMIZATION`: personal fields read nowhere flagged for removal. L3≈ · fix J ·
  assess.
- [ ] **AI17** `PII-TO-LLM`: personal fields sent to a model's API flagged (PD). L3≈ · fix J ·
  trial.
