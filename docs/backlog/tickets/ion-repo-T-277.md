# ion-repo#T-277 · Money, payments and webhooks done right, accounts protected
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Application security, Business domain), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.46, "Money, time, accounts and mail": Amounts in the smallest unit with their
currency, dates in UTC, webhooks verified, cards never on the server, passkeys and rate limits, bulk
mail that can be unsubscribed from.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS26** `PASSKEYS`: WebAuthn offered for accounts (allauth's MFA, SimpleWebAuthn). L2≈ · fix
  J · assess.
- [ ] **AS27** `ADMIN-MFA`: the admin asks for a second factor. L2≈ · fix J · trial.
- [ ] **AS28** `RATE-LIMITS`: login, password reset and the API rate-limited, in the app or the
  proxy. L2≈ · fix J · trial.
- [ ] **BD01** `MONEY` (draft): `FloatField`, `float` or JS `number` arithmetic on names like price,
  amount, total, fee or balance; integers of the smallest unit stay the grid's way. L2≈ · fix J ·
  trial.
- [ ] **BD02** `TIME-ZONE` (draft): naive datetimes, `TIME_ZONE` set, calendar computations through
  `zoneinfo` (with `NAIVE-DATETIMES` and `USE-TZ`). L2 · fix J · trial.
- [ ] **BD03** `WEBHOOKS-VERIFIED`: incoming webhooks check their signature (Stripe's
  `construct_event`, GitHub's `X-Hub-Signature-256` compared in constant time). L2 · fix J · adopt.
- [ ] **BD04** `WEBHOOKS-DEDUPLICATED`: events stored by ID before they're handled. L2≈ · fix J ·
  trial.
- [ ] **BD05** `PAYMENTS-BY-PROVIDER`: card numbers never reach the server (Checkout or Elements),
  no `card_number` field anywhere; critical. L2 · fix J · adopt.
- [ ] **BD06** `CURRENCY-WITH-AMOUNT`: every amount carries its ISO 4217 currency. L2≈ · fix J ·
  assess.
- [ ] **BD07** `EXPLICIT-ROUNDING`: the rounding mode stated wherever amounts are divided (taxes,
  splits). L2≈ · fix J · trial.
- [ ] **BD08** `EMAILS-CASE-INSENSITIVE`: e-mail uniqueness ignores case (a `Lower()` unique
  constraint, `citext`). L2 · fix J · trial.
