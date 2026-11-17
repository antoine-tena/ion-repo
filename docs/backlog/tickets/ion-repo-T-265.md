# ion-repo#T-265 · A front that renders safely: UI states, SSR and hydration, SEO, error pages
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Front, accessibility and i18n), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.39, "A fast, SSR-safe front": Hydration and SSR safety, keys and loading states
handled, bundle and image budgets, scripts and fonts that don't block, SEO basics.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FA03** `UI-STATES` (draft): results of `useFetch` and `useAsyncData` whose `status` and
  `error` the template never reads. L2 · fix J · trial.
- [ ] **FA04** `UTILITY-CSS-FIRST` (draft): Tailwind or UnoCSS configured; `<style scoped>` blocks
  counted as a ratchet. L1 · ratchet · trial.
- [ ] **FA20** `VUE-NO-V-IF-WITH-V-FOR`. L2 · fix J · adopt.
- [ ] **FA21** `SSR-SAFE`: no `window`, `document` or `localStorage` at setup outside `onMounted`,
  `import.meta.client` or `<ClientOnly>`. L2 · fix J · adopt.
- [ ] **FA22** `HYDRATION-SAFE`: no `Math.random()`, `Date.now()` or locale formatting rendered on
  both sides without a stable value (`useState`, `useId`). L2≈ · fix J · trial.
- [ ] **FA23** `SEO-BASICS`: title, description, canonical URL, `robots.txt` and a sitemap on public
  sites (`useSeoMeta`, `@nuxtjs/sitemap`). L2 · fix S · trial.
- [ ] **FA24** `SOCIAL-CARDS`: Open Graph title and image on the pages people share. L2 · fix S ·
  assess.
- [ ] **FA25** `CSS-LINT`: Stylelint where CSS is written by hand. L1 · fix S · trial.
- [ ] **FA26** `ERROR-PAGES`: designed 404 and 500 pages (Nuxt's `error.vue`, Django's `404.html`
  and `500.html`). L0 · fix S · trial.
- [ ] **FA31** `WEB-MANIFEST`: icons and a web manifest for installable apps. L0 · fix S · assess.
