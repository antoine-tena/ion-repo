# ion-repo#T-218 · Settings that leak: CORS, passwords, HTTPS, front secrets, debug modes
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.13, "Secrets and the settings that leak": The secrets themselves, checksum-verified,
and the production settings read as they resolve (v0.6.9): cookies, headers, HTTPS, debug flags,
keys in the front.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS23** `CORS-STRICT`: no allow-all origins with credentials (`CORS_ALLOW_ALL_ORIGINS`,
  `Access-Control-Allow-Origin: *`). L2 · fix J · adopt.
- [ ] **AS24** `PASSWORD-HASHING`: Argon2 or the framework's default first, never MD5, SHA-1 or
  unsalted hashers. L2 · fix S · adopt.
- [ ] **AS25** `PASSWORD-VALIDATORS`: `AUTH_PASSWORD_VALIDATORS` set, or a passkey-first login. L2 ·
  fix S · adopt.
- [ ] **AS35** `HTTPS-ONLY`: `SECURE_SSL_REDIRECT`, Caddy's automatic HTTPS, `force_ssl`. L2 · fix S
  · adopt.
- [ ] **AS36** `NO-SECRETS-IN-FRONT`: no secret-looking key under Nuxt's `runtimeConfig.public`,
  `NUXT_PUBLIC_*`, `VITE_*` or `NEXT_PUBLIC_*`. L2 · fix J · adopt.
- [ ] **AS49** `BAAS-ACCESS-RULES`: Firebase's `firestore.rules`, `storage.rules` and
  `database.rules.json` never open to everyone (`allow read, write: if true`, or the test mode's
  `request.time <` date left in), and every Supabase table of an exposed schema under row-level
  security in its migrations, the `service_role` key never in front code; the anon key is public
  by design, so these rules are the only lock (170 generated apps found readable and writable by
  anyone in 2025, CVE-2025-48757). L1 · fix J · adopt.
- [ ] **AS37** `PRIVATE-SOURCEMAPS`: production source maps not served publicly. L2 · fix S · trial.
- [ ] **AS38** `DEV-TOOLS-DEV-ONLY`: debug toolbars and devtools only in development settings and
  dependency groups. L2 · fix S · adopt.
- [ ] **AS39** `SECURITY-TXT`: production web apps serve `/.well-known/security.txt` (RFC 9116). L0
  · fix S · trial.
- [ ] **AS45** `FRAMEWORK-DEBUG-OFF`: `DJANGO-DEBUG-OFF` for the other frameworks: Laravel's
  `APP_DEBUG`, Rails' `consider_all_requests_local`, Flask's `debug=True`, Spring's Actuator
  exposing more than health and info. L2 · fix S · adopt.
