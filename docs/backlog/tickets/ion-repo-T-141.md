# ion-repo#T-141 · Grid v2: the themes after the launch
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-17
- **Effort**: L · **Owner**: @antoine-tena · **Due**: —
- **Origin**: vision of 17 October 2026 (the 23 themes); ion-repo#T-52, ion-repo#T-78, ion-repo#T-92, ion-repo#T-93, ion-repo#T-101, ion-repo#T-102,
  ion-repo#T-103 and ion-repo#T-105 merged here, as rules

Planned box by box: the three new themes in v0.5.13, every other box with its theme's release
in [🚀 Releases](../README.md#releases), as the ideas that carry it.

- [ ] Tests: property tests, mutation testing, API fuzzing, end-to-end journeys (with ion-repo#T-136).
- [ ] Data and migrations: migrations linted before merge (django-migration-linter, squawk),
  seed data, anonymised dumps.
- [ ] Front, accessibility and performance: axe checks, Lighthouse budgets, Core Web Vitals.
- [ ] Operations and observability: backups with a tested restore, health checks, alerts on
  symptoms; OpenTelemetry and SLO by profile (ion-repo#T-39).
- [ ] Git and docs: issue and pull request templates, CODEOWNERS, a licence and the
  dependencies' licences checked, release notes written from the commits.
- [ ] AI-assisted development: `AGENTS.md` for every agent, the context loaded at session start
  measured and capped, MCP servers pinned, narrow permissions, a tool that reads code symbol
  by symbol (Serena, an LSP) so a file's size matters less.
- [ ] Business domain, as universal rules with project settings: money in cents, dates stored
  in UTC, personal data out of the logs.
- [ ] Three new themes, each entering `THEMES` with its first rule: `licensing`,
  `infrastructure`, `data-science` (`MODEL-TRACED` moves there); decision 3 of 24 October
  2026 in the [kiln score ideas](../kiln-score-the-thesis.md).
