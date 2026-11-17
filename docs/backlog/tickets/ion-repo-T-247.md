# ion-repo#T-247 · API contracts: the schema committed and frozen, typed routes, pagination
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (API, contracts and typing), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.32, "API, contracts and typing": The schema committed and checked for breaking
changes, front types generated from it, typing read through its inheritance and counted as ratchets.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AT01** `OPENAPI-IN-REPO` (draft): the API's schema committed (`openapi.json` or `.yaml`)
  when an API framework is present (Django Ninja, DRF, FastAPI, NestJS). L0 · fix J · trial.
- [ ] **AT02** `FROZEN-CONTRACT` (draft): CI compares the schema with the integration branch's
  (oasdiff's breaking-change check). L1 · fix S (the CI step) · trial.
- [ ] **AT03** `CONTRACT-DRIFT` (draft): front types generated from the committed schema
  (openapi-typescript or the like) with a script to regenerate them; `--deep` proves there's no
  drift. L1 · fix J · trial.
- [ ] **AT04** `TYPED-API` (draft, Ninja): every route has typed input and output schemas. L2 · fix
  J · trial.
- [ ] **AT05** `PAGINATION` (draft): list endpoints paginated (`@paginate`, DRF's
  `DEFAULT_PAGINATION_CLASS`). L2 · fix J · trial.
- [ ] **AT06** `DEPRECATION-HEADERS` (draft): deprecated routes send `Deprecation` (RFC 9745) and
  `Sunset` (RFC 8594). L2≈ · fix J · assess.
- [ ] **AT07** `IDEMPOTENCY` (draft): payment and creation endpoints accept an `Idempotency-Key`.
  L2≈ · fix J · assess.
- [ ] **AT08** `STRICT-TYPING` and `STRICT-TS` (scored): config read with its inheritance (`extends`
  chains, `[tool.mypy]` anywhere), not by one regex.
- [ ] **AT09** `TYPE-CHECK-IN-CI`: a type checker runs in CI (mypy, pyright, ty or pyrefly; tsc,
  vue-tsc or `nuxi typecheck`). L1 · fix S · adopt.
