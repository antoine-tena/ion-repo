# ion-repo#T-412 · Dates and daylight saving: UTC stored, `Europe/Paris` calendar, times that do not exist
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `studio/docs/business/fabrication/reservation.md`, "Ce qui va dans un outil Ion" · `annski/CLAUDE.md` [FUSEAU]

annski's rule [FUSEAU]: store UTC, compute calendar notions (today, a departure date, a season)
in `Europe/Paris` with `timezone.localdate()`, never `.date()` on a UTC instant. Booking adds
the hard cases: 2:30 on the spring Sunday does not exist, 2:30 on the autumn Sunday exists twice.
- [ ] The rule in `django.md`, with the two cases written and tested (`zoneinfo`, `fold`).
- [ ] Helpers in the template for "a local time to an instant" that refuse the missing hour and
  pick the first occurrence of the doubled one. Score side: ion-repo#T-278.
