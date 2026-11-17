# ion-repo#T-242 · Code that can be attacked: redirects, SSRF, paths, escaping, JWT, SAST
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.29, "Code that can be attacked": Injection, unsafe deserialization, weak crypto,
open redirects, SSRF and the rest, with taint followed inside a function.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS19** `SECURE-RANDOM`: tokens from `secrets` or `crypto.randomUUID`, never `random` or
  `Math.random` (S311). L2 · fix S · adopt.
- [ ] **AS29** `NO-OPEN-REDIRECT`: redirects to a request value checked
  (`url_has_allowed_host_and_scheme`). L2 · fix J · adopt.
- [ ] **AS30** `NO-SSRF`: outgoing requests to user-given URLs pass an allowlist. L2≈ · fix J ·
  trial.
- [ ] **AS31** `NO-PATH-TRAVERSAL`: files opened from request values resolved and confined. L2≈ ·
  fix J · trial.
- [ ] **AS33** `AUTOESCAPE`: no `|safe`, `mark_safe`, `{% autoescape off %}`, `v-html` or
  `dangerouslySetInnerHTML` on variables (with NO-V-HTML). L2 · fix J · adopt.
- [ ] **AS34** `JWT-SAFE`: algorithms pinned (never `none`), signature and expiry checked. L2 · fix
  J · adopt.
- [ ] **AS40** `SAST-IN-CI`: CodeQL, semgrep or the language's security linter in CI. L1 · fix S ·
  adopt.
- [ ] **AS46** `GRAPHQL-LIMITS`: depth and cost limits, introspection off in production. L2≈ · fix J
  · trial.
- [ ] **AS47** `EXPRESS-HARDENED`: Helmet or equivalent headers, `x-powered-by` off. L2 · fix S ·
  trial.
