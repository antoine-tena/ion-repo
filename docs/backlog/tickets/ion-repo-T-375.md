# ion-repo#T-375 · [CLOCK] names freezegun, which [NEW-DEPENDENCY] refuses
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: emberstudio session `feat/auth`, 30 October 2026

`django.md` [CLOCK] asks for `freezegun` (`@freeze_time`), whose last release (1.5.5) dates from
9 August 2025: more than a year, so [NEW-DEPENDENCY] forbids adding it. The session took
`time-machine` (3.6.0, 25 October 2026, MIT) instead. The rule names `time-machine`
(`time_machine.travel(..., tick=False)`), and the grid's check (`charter.toml`, ratchet
`clock-in-tests`) accepts both.
