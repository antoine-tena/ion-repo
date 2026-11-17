# ion-repo#T-160 · A front with no backend ships a smoke test
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-20
- **Effort**: M · **Owner**: @antoine-tena · **Due**: —
- **Origin**: training on the fleet (2026-10-20): a new `none` + Nuxt, Next or Astro project
  misses TESTS-PRESENT, the only gap left on a fresh repo (`test_template.py` exempts it)

Its only code is constants: a test of them would be filler. The test worth having is a smoke
test of the built site, the home page carrying the site title, through `node --test` (no
dependency): Astro's `dist/index.html`, Next's prerendered `.next/server/app/index.html`, Nuxt
prerendering `/` or its server started. Run after `build` in `ci.yml` and in `kiln check`; then
drop the exemption.
