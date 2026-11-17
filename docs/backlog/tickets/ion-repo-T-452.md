# ion-repo#T-452 · Nuxt template: images and code split that do not eat a free quota
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, `fae710d4` 23:22, `abd9bcc1` 19:53

- [ ] `sizes="100vw"` is read by `@nuxt/image` as a small fixed width: photos blurred on a large screen; rule or lint on it.
- [ ] Group the small chunks at build: 207 requests per home visit became about 110 with the same weight.
- [ ] Document the option of static files on object storage (`cdnURL`, CSP, CORS).
