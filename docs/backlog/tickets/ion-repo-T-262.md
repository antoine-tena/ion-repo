# ion-repo#T-262 · An accessible front: names, alt text, focus, motion, ARIA
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Front, accessibility and i18n), made a ticket on
  25 October 2026 at antoine's request

Planned in v0.6.38, "An accessible front, in every language": Labels, alt texts, focus, contrast and
motion checked in templates and by axe; the European Accessibility Act's profile; every locale
complete.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **FA01** `ACCESSIBILITY` (draft): labels and accessible names checked in templates by
  eslint-plugin-vuejs-accessibility or jsx-a11y, run as mapped tools (F). L2 · fix J · adopt.
- [ ] **FA02** `AUTOMATED-ACCESSIBILITY` (draft): axe in Playwright tests (`@axe-core/playwright`)
  or pa11y-ci on the main pages. L1 · fix S · trial.
- [ ] **FA06** `IMG-ALT`: every image has `alt`, empty for decoration. L2 · fix J · adopt.
- [ ] **FA07** `CLICKABLE-ELEMENTS`: no click handler on a `div` or `span` without a role and a
  keyboard handler: a button or a link instead. L2 · fix J · adopt.
- [ ] **FA08** `FOCUS-VISIBLE`: no `outline: none` or `outline-0` without a `:focus-visible` style.
  L2 · fix J · adopt.
- [ ] **FA09** `REDUCED-MOTION`: animations respect `prefers-reduced-motion` (Tailwind's
  `motion-safe:`). L2 · fix S · trial.
- [ ] **FA10** `VIEWPORT-META`: `width=device-width`, never `user-scalable=no` or `maximum-scale=1`.
  L2 · fix S · adopt.
- [ ] **FA11** `NO-AUTOPLAY`: no media that plays sound by itself. L2 · fix S · adopt.
- [ ] **FA12** `SKIP-LINK`: a skip-to-content link in layouts. L2≈ · fix S · trial.
- [ ] **FA13** `ARIA-VALID`: ARIA roles and attributes valid and not redundant. L2 · fix J · adopt.
