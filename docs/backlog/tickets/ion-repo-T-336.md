# ion-repo#T-336 · Node back ends: Express, Fastify, NestJS, Hono
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-291 by the framework coverage review of 26 October 2026, at antoine's
  request (the most used frameworks of the 2025 surveys checked against the plan): the Node back
  ends get their own release instead of a share of the fronts'

Planned in v0.6.57, "JavaScript beyond Nuxt: the Node back ends": Express, Fastify, NestJS and Hono,
the most used back ends after Django's peers, each with its own release's worth of rules rather than
a share of the fronts' (framework coverage review of 26 October 2026).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP16** Express · `EXPRESS-5`: Express 5, whose router passes rejected promises to the error
  handler. L1 · fix J · trial.
- [ ] **FP17** NestJS · `NEST-VALIDATION-PIPE`: a global `ValidationPipe` with `whitelist` and
  `forbidNonWhitelisted`. L2 · fix S · adopt.
- [ ] **FP18** NestJS · `NEST-GUARD-BY-DEFAULT`: a global authentication guard, public routes marked
  one by one. L2 · fix J · trial.
- [ ] **FP24** Express · `EXPRESS-TRUST-PROXY`: `trust proxy` set to the proxies in front when the
  app runs behind one, so `req.ip` and rate limits see the real client. L2≈ · fix J · trial.
- [ ] **FP25** Fastify · `FASTIFY-SCHEMAS`: a schema on every route's body, query and response, in
  JSON Schema or through a type provider (TypeBox, Zod). L2 · fix J · adopt.
- [ ] **FP26** Hono · `HONO-VALIDATOR`: request input through a validator (`@hono/zod-validator`,
  `@hono/standard-validator`). L2 · fix J · trial.
- [ ] **AS48** (the Node ORMs' part) `NO-SQL-INJECTION`: `$queryRawUnsafe` and `$executeRawUnsafe`
  of Prisma, `raw` of Knex, `query` of TypeORM and `sql.raw` of Drizzle never built from a variable.
  L2 · fix J · adopt.
