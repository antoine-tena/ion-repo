# ion-repo#T-211 · Rules that say what they mean: applicability as an expression, `any_of`, `unknown`
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, The detection engine, Rule
  format v2 and authoring), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.8, "Rules that say what they mean": Applicability as an expression, several ways to
meet one practice, conditions across files, evidence for passes, an honest `unknown`.

- [ ] **A23** Applicability as an expression over the model (`component.role == "backend" and django
  >= 4.2`) instead of the flat `applies` list.
- [ ] **E08** Combinators (`all`, `any`, `not`) and conditions ("if a Dockerfile `EXPOSE`s a port,
  compose or the Dockerfile has a health check").
- [ ] **E18** Equivalence lists as data (Python linters: ruff, flake8, pylint; dependency bots:
  Dependabot, Renovate…): a practice met by any, with "met; kiln recommends ruff" as a gentle
  `trial` note.
- [ ] **E19** Evidence for passes too: "met by `renovate.json`", "met: `USER app` in the final stage
  of `Dockerfile`". `--all` says why each rule passed.
- [ ] **E20** A third outcome, `unknown`: the detector couldn't decide (a config written as code, a
  tool missing, a file too big). Listed apart, never a pass, never a fail.
- [ ] **E33** A rule's condition can read the model (`component.frameworks.django.version`), so
  Django 4.2 and 5.2 can have different detectors.
- [ ] **E34** Inline justifications in the charter's style (`# kiln: allow NAIVE-DATETIMES,
  reason`): counted, shown, gone when the code they sit on goes.
- [ ] **E35** A detector can ask for several files at once (compose, Dockerfile and CI together):
  the engine hands it the set, each file read once.
- [ ] **G03** `applies` as an expression over the repo model (A).
- [ ] **G04** `any_of`: the ways one practice can be met, each with its own detector.
- [ ] **G20** One practice, several languages, one ID: `[detector.python]`, `[detector.typescript]`,
  `[detector.java]`.
- [ ] **G24** Typed settings with defaults, for project data only (time zone, currency, integration
  branch): never a knob that weakens a rule (doctrine 1).
