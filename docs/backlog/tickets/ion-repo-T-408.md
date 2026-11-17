# ion-repo#T-408 · Django template: outgoing mail that arrives (fallback relay, quota, bounces, unsubscribe)
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/backend/core/mail/`

The template sends mail with Django's bare SMTP backend. annski learned in production what it
takes for mail to arrive; booking (TM Coiffure) sends confirmations and reminders from day one.
- [ ] A fallback relay when the main one's daily quota is spent (Brevo free: 300 a day):
  `annski/backend/core/mail/fallback.py`, counter per relay and per Paris day in
  `annski/backend/core/mail/quota.py`.
- [ ] A `List-Unsubscribe` of the site on every mail, before the relay adds its own:
  `annski/backend/core/mail/smtp.py`.
- [ ] A permanent 5xx refusal marks the address and stops the retries:
  `annski/backend/emails/bounces.py`.
- [ ] HTML written in a back office goes through an allow-list: `annski/backend/emails/sanitize.py`
  (the rule and its audit: ion-secure#T-04).
- [ ] DNS side (SPF, DKIM, DMARC): ion-host#T-03. Score side: ion-repo#T-278.
