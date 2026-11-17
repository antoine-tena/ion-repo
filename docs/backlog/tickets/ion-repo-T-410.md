# ion-repo#T-410 · Restore test that proves the backup: missing migrations, business rows
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: adoption of annski by ion-repo, 2026-11-02 · `annski/config/vps/annski-restore-test.sh`

The template's `restore-test.sh` only counts tables. annski's restores the latest dump into a
throwaway PostgreSQL, then has the running image check that no migration is missing and count
the rows that matter (members, orders, tickets); a failure fails the unit and alerts. Brought
into the template now, while `config/vps/` still lives here; it moves to ion-host with the rest
(ion-host#T-07, ion-repo#T-389).
