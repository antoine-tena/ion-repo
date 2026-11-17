# ion-repo#T-217 · Secrets in the tree cap the score; session cookies, headers, CSRF
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Application security), made
  a ticket on 25 October 2026 at antoine's request

Planned in v0.6.13, "Secrets and the settings that leak": The secrets themselves, checksum-verified,
and the production settings read as they resolve (v0.6.9): cookies, headers, HTTPS, debug flags,
keys in the front.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E28** A secrets engine: provider patterns (gitleaks' rules as data), checksum-verified
  tokens (GitHub's `ghp_` and `github_pat_` tokens carry a CRC32, so zero false positives), entropy
  last; documented sample keys and placeholders (`AKIAIOSFODNN7EXAMPLE`, `changeme`, `<your-token>`)
  left out.
- [ ] **AS01** `SECRETS` (draft): the secrets themselves in tracked files (provider patterns,
  checksum-verified tokens, entropy last), where `SECRET-SCAN` checks that a scan runs and
  `NO-TRACKED-ENV` that no `.env` is tracked; critical: it caps the score at 49. L2 · fix J (rotate,
  then remove) · adopt.
- [ ] **AS02** `SESSION-COOKIES` (draft, Django): `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  `SESSION_COOKIE_HTTPONLY` and `SAMESITE` in the production settings, evaluated statically. L2 ·
  fix S · adopt.
- [ ] **AS03** `SECURITY-HEADERS` (draft): HSTS of a year or more, `nosniff`, frames denied, a
  referrer policy; in Django's settings, the reverse proxy (Caddy, nginx) or Nuxt (nuxt-security).
  L2 · fix S · adopt.
- [ ] **AS04** `CSP-NONCE` (draft): a Content Security Policy with nonces (Django 6.0's built-in
  CSP, django-csp, nuxt-security), no `unsafe-inline` for scripts. L2 · fix J · trial.
- [ ] **AS05** `CONSTANT-TIME` (draft): secrets compared with `hmac.compare_digest` or
  `crypto.timingSafeEqual`, never `==` on names like token, signature or digest; the charter's ban
  promoted. L2 · fix S · adopt.
- [ ] **AS09** `SUBRESOURCE-INTEGRITY` (draft): `<script>` and `<link>` from another origin carry
  `integrity`. L2 · fix S (hash computed online) · adopt.
- [ ] **AS20** `NO-HARDCODED-PASSWORDS`: S105 to S107 and their JS counterparts. L4 · fix J · adopt.
- [ ] **AS21** `TLS-VERIFIED`: no `verify=False`, `rejectUnauthorized: false`,
  `NODE_TLS_REJECT_UNAUTHORIZED=0` or `InsecureSkipVerify: true`. L2 · fix S · adopt.
- [ ] **AS22** `CSRF-ON`: CSRF middleware on; `@csrf_exempt` only with a justification marker. L2 ·
  fix J · adopt.
