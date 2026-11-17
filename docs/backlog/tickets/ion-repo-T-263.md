# ion-repo#T-263 · Accessible and translated: headings, contrast, the EU Accessibility Act, i18n keys
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

- [ ] **FA14** `HEADINGS-ORDER`: one `h1` per page, no skipped level. L3≈ · fix J · trial.
- [ ] **FA15** `FORM-AUTOCOMPLETE`: `autocomplete` on identity and address fields (WCAG 2.2, 1.3.5).
  L2 · fix S · trial.
- [ ] **FA16** `TOUCH-TARGETS`: targets of 24 by 24 CSS pixels at least (WCAG 2.2, 2.5.8), read from
  utility classes. L3≈ · fix J · assess.
- [ ] **FA17** `COLOR-CONTRAST`: the theme's text and background pairs computed from its tokens; axe
  for the rendered rest. L3≈ · fix J · trial.
- [ ] **FA18** `EU-ACCESSIBILITY-ACT`: for businesses selling to consumers in the EU, the European
  Accessibility Act applies since 28 June 2025: in that profile the accessibility rules move to
  `adopt`, and an accessibility statement exists. L0 · fix J · adopt (profile).
- [ ] **FA27** `I18N-KEYS-COMPLETE`: every locale has every key and no key is unused
  (vue-i18n-extract, `makemessages` compared). L3 · fix S · adopt.
- [ ] **FA28** `I18N-NO-BARE-TEXT`: user-facing text in templates goes through the i18n layer once
  one is configured (`@intlify/vue-i18n/no-raw-text`). L2 · ratchet · trial.
- [ ] **FA29** `LOCALE-FORMATTING`: dates, numbers and currencies through `Intl` or the framework's
  filters, never concatenated by hand. L2≈ · fix J · assess.
- [ ] **FA30** `RTL-READY`: logical CSS properties once a right-to-left locale is configured. L2 ·
  fix S · assess.
