# ion-repo#T-249 · Clients and schemas generated, not copied: OpenAPI lint, GraphQL, Protobuf, settings
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

- [ ] **AT19** `OPENAPI-LINT`: the committed schema passes Spectral or Redocly's lint. L4 · fix J ·
  trial.
- [ ] **AT20** `GENERATED-CLIENT`: the front reaches the API through generated types, never
  hand-copied ones. L2≈ · fix J · trial.
- [ ] **AT21** `TYPED-PROPS`: `defineProps<…>()` and `defineEmits<…>()` typed. L2 · fix J · adopt.
- [ ] **AT22** `RUNTIME-SCHEMAS`: outside data parsed by a schema library (Pydantic, Zod, Valibot)
  at the edge. L2≈ · fix J · trial.
- [ ] **AT23** `GRAPHQL-SCHEMA`: the GraphQL schema committed and checked for breaking changes. L1 ·
  fix J · trial.
- [ ] **AT24** `PROTO-LINT`: `buf lint` and `buf breaking` for Protobuf APIs. L1 · fix S · trial.
- [ ] **AT29** `SETTINGS-TYPED`: application settings parsed into a typed object (pydantic-settings,
  a schema-checked runtime config). L2≈ · fix J · trial.
