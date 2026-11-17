# ion-repo#T-411 · Django template: export and erasure of a person's data (GDPR)
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `studio/docs/business/fabrication/reservation.md` · `annski/backend/accounts/gdpr.py`

Split decided on 2026-11-02: the code goes to the template, the rules, the audit and the record of
processing to ion-secure (ion-secure#T-05, ion-secure#T-06).
- [ ] An export of everything stored about one person (JSON), and an erasure that anonymises what
  must stay (orders, invoices) instead of failing on a protected foreign key, as
  `annski/backend/accounts/gdpr.py` does.
- [ ] A registry of personal fields per model, so a new field without export and anonymisation is
  seen (rule [DONNEES-PERSO] of annski).
- [ ] The scheduled anonymisation at the end of the retention period (booking: customers seen
  long ago), on the queue of ion-repo#T-374. Score side: ion-repo#T-276.
