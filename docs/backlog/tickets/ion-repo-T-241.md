# ion-repo#T-241 · Code that can be attacked: taint, permissions, uploads, injections, crypto
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (The detection engine, Application security), made
  a ticket on 25 October 2026 at antoine's request

Planned in v0.6.29, "Code that can be attacked": Injection, unsafe deserialization, weak crypto,
open redirects, SSRF and the rest, with taint followed inside a function.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **E11** Taint inside one function: a request value (`request.GET`, `request.data`, route
  parameters, `req.query`) reaching a sink (`execute`, `os.system`, `open`, `redirect`,
  `subprocess`, `eval`) without a known sanitizer.
- [ ] **AS06** `EXPLICIT-PERMISSIONS` (draft): every route states its authentication (Ninja's
  `auth=`, DRF's `permission_classes`), and the default isn't `AllowAny`. L2 · fix J · adopt.
- [ ] **AS07** `PUBLIC-ROUTES` (draft): public routes listed in one place, everything else
  authenticated by default. L2≈ · fix J · trial.
- [ ] **AS08** `UPLOADS` (draft): uploads validated (size limits, type by content, storage outside
  the web root, random names). L2≈ · fix J · trial.
- [ ] **AS13** `VALIDATE-AT-BOUNDARIES` (draft): request data parsed by a schema before use. L2≈ ·
  fix J · trial.
- [ ] **AS14** `NO-EVAL`: no `eval`, `exec`, `new Function` or string `setTimeout`. L2 · fix J ·
  adopt.
- [ ] **AS15** `NO-SHELL-INJECTION`: no `shell=True` or `os.system` on non-literal input, no
  `child_process.exec` with template strings (S602 to S605). L2 · fix J · adopt.
- [ ] **AS16** `NO-UNSAFE-DESERIALIZATION`: no pickle, marshal, `yaml.load`, `ObjectInputStream` or
  `unserialize` on outside data (S301, S506). L2 · fix S (`yaml.safe_load`) · adopt.
- [ ] **AS17** `NO-XXE`: XML parsed with defusedxml or safe defaults (S313 to S320). L4 · fix S ·
  adopt.
- [ ] **AS18** `NO-WEAK-CRYPTO`: no MD5 or SHA-1 for security, no DES, RC4 or ECB (S324, S303 to
  S305). L4 · fix J · adopt.
- [ ] **AS48** `NO-SQL-INJECTION`: no query built from a variable by concatenation, `%` or an
  f-string: `raw`, `extra` and `RawSQL` of Django, `text` of SQLAlchemy, a DB-API `execute`; each
  stack's pack adds its own APIs (ion-repo#T-336, ion-repo#T-337, ion-repo#T-338, ion-repo#T-339). L2 · fix J · adopt.
