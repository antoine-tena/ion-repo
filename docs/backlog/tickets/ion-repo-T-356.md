# ion-repo#T-356 · Strangers may follow the candidates; kiln's `develop` gets a channel of its own
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q119: "yes, they can use the beta too"; Q131),
  decision 35

`develop` takes merges checked by linters only (CI runs at the release): a stranger should get
early releases that passed the whole CI, which the candidates are.
- [ ] `beta` = the candidates, open to anyone (today's `internal`); kiln's own development, the
  editable checkout, moves to `edge`; `kiln update` converts the setting.
- [ ] The reference and `kiln set channel=…`'s help say what each channel gets and risks.
