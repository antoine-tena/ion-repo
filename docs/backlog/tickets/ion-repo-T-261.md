# ion-repo#T-261 · Requests traced: request IDs, OpenTelemetry, front errors, an audit trail
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Observability), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.37, "Errors and logs you can follow": Structured logs to stdout, no secret in them
and no stack trace shown, errors tracked with their release, a request ID and traces from the front
to the back.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **OB01** `REQUEST-ID` (draft): a request-ID middleware (django-guid, asgi-correlation-id) with
  the ID in the log format and the response headers. L2 · fix S · trial.
- [ ] **OB02** `OPENTELEMETRY` (draft): the OpenTelemetry SDK configured from `OTEL_*` variables,
  the framework and HTTP clients instrumented, `traceparent` forwarded from the front. L2 · fix S ·
  trial.
- [ ] **OB06** `FRONT-ERRORS-CAPTURED`: browser errors reported (Sentry for Vue and Nuxt), source
  maps uploaded privately. L1 · fix S · trial.
- [ ] **OB07** `RELEASE-IN-EVENTS`: errors and traces carry the release (the commit SHA), so a
  regression points to a deploy. L2 · fix S · trial.
- [ ] **OB09** `AUDIT-TRAIL`: security-relevant actions (login, role change, export, deletion)
  written to an append-only log. L2≈ · fix J · trial.
