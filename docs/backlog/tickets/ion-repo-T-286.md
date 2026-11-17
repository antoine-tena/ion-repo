# ion-repo#T-286 · `--deep`: the app built, served and probed
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Deep checks, opt-in and sandboxed, Performance),
  made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.52, "`--deep`: the app built and probed": Images built and scanned, migrations
applied and reversed, the API fuzzed, the front rendered for axe and Lighthouse, the app served and
probed, a deployed URL on request.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **N02** Images built: size, final user, a shell or not, packages with known vulnerabilities
  (trivy or grype on the image), the health check passing.
- [ ] **N09** Migrations applied to a fresh Postgres container, then reversed; their SQL linted by
  squawk (through `sqlmigrate`).
- [ ] **N10** The OpenAPI schema generated and compared with the committed one (CONTRACT-DRIFT),
  then a short Schemathesis run (API-FUZZING).
- [ ] **N11** The front built: bundle sizes (JS-BUDGET), `nuxi typecheck`, pages rendered by
  Playwright for axe (ACCESSIBILITY) and for Lighthouse's lab metrics (CORE-WEB-VITALS).
- [ ] **N12** The app served locally and probed: security headers, cookie flags, CORS, error pages
  leaking a stack trace, `/admin` exposed, directory listings, server banners.
- [ ] **N13** A deployed URL scored too (`--url https://…`, opt-in): TLS, headers, `security.txt`,
  redirects; the production that the repo describes.
- [ ] **N14** N+1 queries caught while the tests run (nplusone, django-zeal), query counts per view.
- [ ] **N18** The backup script run against a throwaway database and restored (TESTED-BACKUPS
  proven) for repos whose scripts kiln knows.
- [ ] **N19** `kiln dev`'s own launch reused as a probe: if the stack starts with `kiln dev`, its
  servers are probed while they run, with no second setup.
- [ ] **PE18** `IMAGE-SIZE-BUDGET`: the final container image's size tracked; `--deep` builds it. L7
  · ratchet · assess.
