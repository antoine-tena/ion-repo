# ion-repo#T-254 · Data modelled right: constraints, public IDs, connections, seeds, the real engine in tests
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Data and migrations, Tests), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.34, "Data and migrations": Migrations reversible, safe on a live table, linted in
CI, run on the production engine; dumps out of git; invariants held by the database.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **DM11** `SQUASH-WHEN-LONG`: an app past about 100 migrations gets them squashed. L0 · fix J ·
  assess.
- [ ] **DM12** `ALEMBIC-ONE-HEAD`: a single head in Alembic's history. L2 · fix J · adopt.
- [ ] **DM13** `NO-DUMPS`: no `.sql`, `.dump` or `.sqlite3` holding real data committed. L0 · fix S
  (untracked) · adopt.
- [ ] **DM14** `DB-CONSTRAINTS`: invariants enforced by the database (`UniqueConstraint`,
  `CheckConstraint`), not only in code. L2≈ · fix J · trial.
- [ ] **DM15** `PUBLIC-IDS`: public identifiers that aren't sequential integers (UUIDv7, ULID), so
  nobody can enumerate them. L2≈ · fix J · assess.
- [ ] **DM16** `CONN-REUSE` (Django): `CONN_MAX_AGE` and `CONN_HEALTH_CHECKS` set, or a pooler. L2 ·
  fix S · trial.
- [ ] **DM17** `SUPPORTED-DATABASES`: Postgres, MySQL, Redis and MongoDB versions in compose and
  manifests still supported. L1 · fix S · adopt.
- [ ] **DM18** `ORM-MIGRATIONS-COMMITTED` (JS, Ruby): Prisma, Drizzle, Knex, TypeORM and Rails
  migrations (and `schema.rb`) committed. L0 · fix J · adopt.
- [ ] **DM19** `SEED-DATA`: a seed command or fixtures with fake data for local development. L0≈ ·
  fix J · trial.
- [ ] **DM20** `QUERIES-OUT-OF-VIEWS`: raw SQL lives in a query module, not in views. L2 · fix J ·
  assess.
- [ ] **TE22** `PROD-ENGINE-IN-TESTS`: tests run on the production database engine (a Postgres
  service in CI, Testcontainers), not SQLite. L1 · fix J · trial.
- [ ] **TE23** `MIGRATIONS-CHECKED`: `makemigrations --check --dry-run` in CI, and a migration from
  an empty database. L1 · fix S · adopt.
