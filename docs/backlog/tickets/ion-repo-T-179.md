# ion-repo#T-179 · A new Django repo's tests start without warnings
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-24
- **Effort**: S · **Owner**: @antoine-tena · **Due**: —
- **Origin**: recording the `kiln new` demo (24 October 2026): `kiln check --all --tests` on a
  fresh Django + Nuxt repo passes with 6 warnings

`UserWarning: No directory at: …/backend/staticfiles/`, raised by WhiteNoise's middleware
(`django/core/handlers/base.py:63`) in each test that builds a request: `STATIC_ROOT` does not
exist before `collectstatic`. A repo kiln has just made should run its tests clean; settle it in
the template (the test settings, or the folder created), not by silencing the warning.
