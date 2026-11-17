# ion-repo#T-278 · People's data as given: phones, names, dates, invoices, mail that arrives
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Business domain), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.46, "Money, time, accounts and mail": Amounts in the smallest unit with their
currency, dates in UTC, webhooks verified, cards never on the server, passkeys and rate limits, bulk
mail that can be unsubscribed from.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **BD09** `PHONES-E164`: phone numbers stored in E.164 (phonenumbers, libphonenumber). L2≈ ·
  fix J · assess.
- [ ] **BD10** `NAMES-AS-GIVEN`: no forced first and last name split, no ASCII-only or short-capped
  names. L2≈ · fix J · assess.
- [ ] **BD11** `DATES-NOT-DATETIMES`: birthdays and due dates stored as dates. L2≈ · fix J · assess.
- [ ] **BD12** `INVOICE-NUMBERING`: invoice numbers in one continuous chronological sequence where
  the law asks for it (France among others), taken inside a transaction. L2≈ · fix J · assess.
- [ ] **BD13** `TAX-RATES-AS-DATA`: VAT rates and thresholds held as dated data, not in code. L2≈ ·
  fix J · assess.
- [ ] **BD14** `ONE-CLICK-UNSUBSCRIBE`: bulk mail with `List-Unsubscribe` and one-click unsubscribe
  (RFC 8058, required by Gmail and Yahoo for bulk senders since 2024). L2≈ · fix J · trial.
- [ ] **BD15** `MAIL-AUTHENTICATED`: SPF, DKIM and DMARC for the sending domain, checked in DNS with
  `--online`. L6 · fix J · trial.
