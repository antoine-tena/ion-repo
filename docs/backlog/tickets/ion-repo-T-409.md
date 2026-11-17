# ion-repo#T-409 · Django template: a `.ics` attached to a mail, with a display alarm
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `studio/docs/business/fabrication/reservation.md`, "Ce qui va dans un outil Ion" (booking) · `annski/backend/events/ics.py`

A confirmation that lands in the customer's calendar: an RFC 5545 event attached
(`text/calendar; method=PUBLISH`), with a `VALARM` `ACTION:DISPLAY` reminder, a stable `UID` so an
update or a cancellation replaces it, times in UTC with the `Europe/Paris` zone. annski serves a
`.ics` per trip (`annski/backend/events/ics.py`), without alarm and never attached to a mail: a
starting point. The texts of the mails: ion-words#T-03.
