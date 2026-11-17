# ion-repo#T-339 · The Laravel, Symfony and WordPress pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.9, "The PHP pack": Strict types, `composer audit` in CI, a supported PHP and no
`phpinfo()` left, then the rules of Laravel, Symfony and WordPress, counted once ten corpus repos of
PHP were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS32** (Laravel's part) `NO-MASS-ASSIGNMENT`: no `$guarded = []` nor `Model::unguard()`, a
  `$fillable` list instead. L2 · fix J · adopt.
- [ ] **FP33** Laravel · `LARAVEL-ENV-IN-CONFIG`: `env()` called only in `config/`, which
  `config:cache` would otherwise break; `.env` untracked and `.env.example` committed. L2 · fix J ·
  adopt.
- [ ] **AT26** (Laravel's part) `PHPSTAN-LEVEL`: Larastan loaded, so PHPStan understands facades and
  Eloquent. L1 · fix S · trial.
- [ ] **AS22** (Laravel's part) `CSRF-ON`: each route left out of CSRF checks
  (`validateCsrfTokens(except: …)`) with a justification marker. L2 · fix J · adopt.
- [ ] **AS48** (the part of Laravel, Doctrine and WordPress) `NO-SQL-INJECTION`: `whereRaw`,
  `DB::raw`, DQL and `$wpdb->query` never built from a variable, `$wpdb->prepare` for WordPress. L2
  · fix J · adopt.
- [ ] **AS01** (Symfony's part) `SECRETS`: a real `APP_SECRET` never in a committed `.env`,
  Symfony's secrets vault or the environment instead. L1 · fix J · adopt.
- [ ] **AS45** (the part of Symfony and WordPress) `FRAMEWORK-DEBUG-OFF`: `APP_ENV=prod` with
  `APP_DEBUG=0`, `WP_DEBUG` and `WP_DEBUG_DISPLAY` off in production. L2 · fix S · adopt.
- [ ] **FP34** WordPress · `WP-NONCES`: every admin, AJAX and REST handler checks a nonce and a
  capability (`check_ajax_referer`, `current_user_can`, a `permission_callback`). L2 · fix J ·
  adopt.
- [ ] **FP35** WordPress · `WP-CODING-STANDARDS`: PHPCS with the WordPress Coding Standards in CI,
  whose sniffs check escaping and sanitizing. L1 · fix S · adopt.
- [ ] Ten corpus repos of Laravel, Symfony and WordPress scored and their findings checked before
  the pack counts (B24), each false alarm fixed in the engine.
