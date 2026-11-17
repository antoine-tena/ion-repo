# ion-repo#T-260 · Errors and logs you can follow
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Errors and logs), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.37, "Errors and logs you can follow": Structured logs to stdout, no secret in them
and no stack trace shown, errors tracked with their release, a request ID and traces from the front
to the back.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **EL01** `STRUCTURED-LOGGING` (draft): structlog or a JSON formatter configured; the charter's
  `logging` ban promoted. L1 · fix J · trial.
- [ ] **EL02** `DOMAIN-ERRORS` (draft): an exception hierarchy per domain, mapped to HTTP in one
  place. L2≈ · fix J · assess.
- [ ] **EL03** `ERROR-TRACKING`: Sentry, GlitchTip, Rollbar or Honeybadger configured, for
  production profiles. L1 · fix J · trial.
- [ ] **EL04** `NO-PII-TO-TRACKER`: `send_default_pii=False` and scrubbing configured. L2 · fix S ·
  adopt.
- [ ] **EL05** `LOGS-TO-STDOUT`: in containers, logs go to stdout, no file handler. L2 · fix J ·
  adopt.
- [ ] **EL06** `LOG-LEVEL-FROM-ENV`. L2 · fix S · trial.
- [ ] **EL07** `LOG-EXCEPTIONS-WITH-TRACE`: `logger.exception` in handlers rather than
  `logger.error(str(e))` (TRY400). L4 · fix S · adopt.
- [ ] **EL08** `LAZY-LOG-FORMAT`: no f-strings in log calls (G004); key-value pairs with structlog.
  L4 · fix S · trial.
- [ ] **EL09** `NO-SECRETS-IN-LOGS`: no `password`, `token`, `secret` or `authorization` values
  passed to a log call. L2 · fix J · adopt.
- [ ] **EL10** `NO-STACK-TRACES-SHOWN`: production error pages hide internals (Django's `DEBUG`,
  Express's `NODE_ENV`, Nuxt's error page, Spring's `include-stacktrace`). L2 · fix J · adopt.
- [ ] **EL11** `UNHANDLED-REJECTIONS` (Node): a process-level handler that logs and exits. L2 · fix
  J · trial.
