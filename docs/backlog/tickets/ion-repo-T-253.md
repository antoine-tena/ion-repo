# ion-repo#T-253 · Migrations safe and reversible, linted in CI
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors, Data
  and migrations), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.34, "Data and migrations": Migrations reversible, safe on a live table, linted in
CI, run on the production engine; dumps out of git; invariants held by the database.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B16** SQL as code: sqlfluff, squawk for Postgres migrations, dbt projects.
- [ ] **F18** squawk and django-migration-linter for migrations, sqlfluff for SQL.
- [ ] **DM01** `MIGRATIONS` (scored): apps with an empty `models.py`, and apps under `tests/`, no
  longer asked for migrations.
- [ ] **DM02** `COMMON-FIELDS` (draft, Django): models inherit a base carrying `created_at` and
  `updated_at`. L2 · fix J · trial.
- [ ] **DM03** `INDEXES` (draft, Postgres): fields filtered or ordered on in querysets have an
  index. L3≈ · fix J · assess.
- [ ] **DM04** `TRANSACTIONS` (draft): views writing several rows do it in `transaction.atomic` (or
  `ATOMIC_REQUESTS`). L2≈ · fix J · trial.
- [ ] **DM05** `USE-TZ` (Django): `USE_TZ = True`. L2 · fix S · adopt.
- [ ] **DM06** `REVERSIBLE-MIGRATIONS`: `RunPython` with `reverse_code`, `RunSQL` with
  `reverse_sql`. L2 · fix J · adopt.
- [ ] **DM07** `SAFE-MIGRATIONS`: no NOT NULL column added without a default to an existing table;
  indexes built concurrently on Postgres (`AddIndexConcurrently`, `atomic = False`). L2≈ · fix J ·
  trial.
- [ ] **DM08** `SCHEMA-AND-DATA-APART`: data migrations (`RunPython`) in their own files. L2 · fix J
  · trial.
- [ ] **DM09** `MIGRATION-LINT-IN-CI`: django-migration-linter or squawk in CI. L1 · fix S · trial.
- [ ] **DM10** `MIGRATION-NAMES`: no `00xx_auto_<date>`: a migration's name says what it changes. L0
  · fix J · trial.
