# ion-repo#T-264 · A fast front: Core Web Vitals, budgets, images, fonts, lazy loading
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Performance), made a ticket on 25 October 2026 at
  antoine's request

Planned in v0.6.39, "A fast, SSR-safe front": Hydration and SSR safety, keys and loading states
handled, bundle and image budgets, scripts and fonts that don't block, SEO basics.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **PE02** `CORE-WEB-VITALS` (draft): Lighthouse CI with assertions (`lighthouserc`); field data
  from the Chrome UX Report's API with `--online`. L1 · fix S · trial.
- [ ] **PE03** `JS-BUDGET` (draft): size-limit or bundle budgets checked at build. L1 · fix S ·
  trial.
- [ ] **PE04** `MODERN-IMAGES` (draft): committed JPEG and PNG over about 200 KB listed with their
  savings; `@nuxt/image` or `<picture>` present; `width`, `height` and `loading="lazy"` set below
  the fold. L2 · fix S (conversion) · trial.
- [ ] **PE09** `NO-SYNC-SCRIPTS`: third-party scripts `async` or `defer`, or loaded through Nuxt
  Scripts. L2 · fix S · adopt.
- [ ] **PE10** `FONT-LOADING`: `font-display` set, fonts subset and preloaded (`@nuxt/fonts` does
  all three). L2 · fix S · trial.
- [ ] **PE11** `TREE-SHAKEN-IMPORTS`: no whole-library imports (`import _ from "lodash"`, `import *
  as icons`). L2 · fix S · adopt.
- [ ] **PE12** `HEAVY-DEPENDENCIES`: moment, full lodash or `core-js` for modern targets, listed
  with lighter options (with `NO-DEPRECATED-PACKAGES`). L1 · fix J · trial.
- [ ] **PE13** `LAZY-COMPONENTS`: heavy components and routes loaded on demand
  (`defineAsyncComponent`, Nuxt's `Lazy` prefix, `React.lazy`). L2≈ · fix J · assess.
- [ ] **PE15** `CACHEABLE-PUBLIC-PAGES`: anonymous pages cacheable (Nuxt's `routeRules` with `swr`
  or `isr`, `Cache-Control` on public views). L2≈ · fix J · trial.
