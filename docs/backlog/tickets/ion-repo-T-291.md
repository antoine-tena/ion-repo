# ion-repo#T-291 · Framework packs: Next.js, React, Angular, Svelte, Astro
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Framework packs), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.6.56, "JavaScript beyond Nuxt: the fronts": Every JS framework and package manager
read; Next.js, React, React Router, Angular, Vue without Nuxt, Svelte and Astro each with its pack,
Electron and Tauri locked down.

The `NOTABLE_PACKAGES` of `score.py` already name what the gap report sees; a pack turns one of them
into rules.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FP07** Next.js · `NEXT-SERVER-ONLY`: secrets and database access in `server-only` modules,
  never imported by a `"use client"` file. L2 · fix J · adopt.
- [ ] **FP08** Next.js · `NEXT-AUTH-IN-DATA-LAYER`: authorization checked where data is read, not
  only in middleware (CVE-2025-29927 let a header skip middleware). L2≈ · fix J · adopt.
- [ ] **FP09** React · `REACT-HOOKS-RULES`: eslint-plugin-react-hooks on (`rules-of-hooks`,
  `exhaustive-deps`). L1 · fix S · adopt.
- [ ] **FP10** React · `REACT-KEYS`: keys on list items (`jsx-key`). L2 · fix J · adopt.
- [ ] **FP11** Angular · `ANGULAR-STRICT`: `strict` and `strictTemplates` on. L1 · fix S · adopt.
- [ ] **FP12** Angular · `ANGULAR-NO-SANITIZER-BYPASS`: `bypassSecurityTrust*` counted, each with
  its reason. L2 · fix J · adopt.
- [ ] **FP13** Angular · `MODERN-ANGULAR`: standalone components, signals and the built-in control
  flow; Angular's own schematics migrate. L2 · fix S · trial.
- [ ] **FP14** Svelte · `SVELTE-RUNES`: Svelte 5 runes in new files (`npx sv migrate svelte-5` for
  the rest). L2 · fix S · trial.
- [ ] **FP15** SvelteKit · `SVELTEKIT-CSRF`: `csrf.checkOrigin` never turned off. L1 · fix S ·
  adopt.
- [ ] **FP21** Next.js · `NEXT-SERVER-ACTIONS-AUTH`: every Server Action checks authorization and
  validates its input, since each one is a public endpoint. L2≈ · fix J · adopt.
- [ ] **FP22** React Router · `ROUTER-LOADER-AUTH`: the loaders and actions of React Router 7
  (formerly Remix) check authorization themselves, like the data layer of Next.js. L2≈ · fix J ·
  trial.
- [ ] **FP23** Astro · `ASTRO-CHECK`: `astro check` in CI. L1 · fix S · adopt.
- [ ] **AS33** (Svelte's part) `AUTOESCAPE`: `{@html}` on variables, like `v-html`. L2 · fix J ·
  adopt.
- [ ] **AS36** (SvelteKit's and Astro's part) `NO-SECRETS-IN-FRONT`: their `PUBLIC_*` variables too.
  L2 · fix J · adopt.
- [ ] Vue's rules (`VUE-MULTI-WORD-COMPONENTS`, `API-CALLS`, `STATE-IN-STORES` and the rest) read a
  Vite + Vue repo as they read Nuxt, each with a passing and a failing example without Nuxt.
