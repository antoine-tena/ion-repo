# ion-repo#T-246 · TypeScript and Vue standards from the syntax tree
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Code standards), made a ticket on 25 October 2026
  at antoine's request

Planned in v0.6.31, "Code standards from the syntax tree": What a regex can't tell: modern Vue,
explicit imports, floating promises, debug prints, TODOs without a ticket, barrel files, with oxlint
or Biome where they decide.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **CS07** `MODERN-VUE` (draft): `<script setup>`, no Options API in new files, `defineModel`,
  no `this.$`. L2 · fix J · trial.
- [ ] **CS10** `EXPLICIT-IMPORTS` (draft, Nuxt): auto-imported composables used without an import,
  counted. L2 · fix S · assess.
- [ ] **CS12** `ASYNC-AWAIT` (draft, TS): `.then()` chains where `await` reads better; floating
  promises with `--deep`, since they need types. L2 · fix J · assess.
- [ ] **CS19** `NO-PRINT-DEBUG`: no `print()` or `console.log` in shipped code (ruff's T20,
  no-console), command-line tools aside. L2 · fix J · adopt.
- [ ] **CS20** `TODO-WITH-TICKET`: each TODO or FIXME cites a ticket (`ion-repo#T-12`, `#123`); the backlog
  is the only list. L2 · ratchet · trial.
- [ ] **CS32** `NO-GLOBAL-MUTATION`: no `global` statements, no module-level state changed by
  functions. L2 · fix J · trial.
- [ ] **CS35** `VUE-MULTI-WORD-COMPONENTS`: component names of two words or more (Vue's style guide,
  essential). L0 · fix J · adopt.
- [ ] **CS36** `TS-NO-NON-NULL-ASSERTION`: `!` assertions counted. L2 · ratchet · trial.
- [ ] **CS37** `TS-NO-ENUMS`: `as const` unions rather than `enum` (erasable syntax, which Node's
  type stripping runs). L2 · fix S · assess.
- [ ] **CS38** `ESM`: `"type": "module"` and no `require()` in TypeScript. L1 · fix J · trial.
- [ ] **CS39** `NO-VAR` and `STRICT-EQUALITY` (JS): `let` and `const`, `===`. L2 · fix S · adopt.
- [ ] **CS44** `NO-NESTED-TERNARY`. L2 · fix J · trial.
