# ion-repo#T-455 · [CONSTANTS]: one naming rule for constants, checked
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-23
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: naming review, 23 November 2026

Principle: a constant's name is understood where it is read, without opening its definition; the
further away it is read, the more it says.

1. **Constant or not.** `UPPER_SNAKE_CASE` for a module value fixed when written and never
   changed, objects and regexes included. Normal case: state, a value computed at run time, a
   function, a service instance, a name imposed by a framework. Generated code is exempt.
2. **Worth naming.** Only if the name teaches something (`TWO = 2` is banned). A closed set of
   codes is an enum; what varies per environment is a setting.
3. **Scope decides the length.** Read in its own file: subject + qualifier (`SWIPE_MIN_PX`; private
   Python: `_PAGE_SIZE`). Read by other files: domain first (`RANKING_PODIUM_SIZE`). Front and
   back: same name, one source, carried by the API or the generated contract. Two private
   `PAGE_SIZE` are fine, two exported ones are not.
4. **Word order.** `DOMAIN_SUBJECT_BOUND_UNIT` (`CART_HOLD_MAX_MINUTES`); bounds `MIN`, `MAX`,
   `DEFAULT`, `FALLBACK` after the subject. Except imposed keys and `…_MAX_LENGTH`. New code
   only: old code converges when touched.
5. **Unit last, unless the type carries it** (`timedelta`). `_MS _SECONDS _MINUTES _DAYS`,
   `_CENTS`, `_PX _PT _BYTES`, `_PERCENT` (0-100) or `_RATIO` (0-1), `_AT` instant, `_DATE` day,
   `_TIME` hour, `_COUNT`. `PAGE_SIZE` stays.
6. **Suffix tells the shape.** Plural for a collection, `X_BY_Y` for a table, `_PATTERN` regex,
   `_PATH` relative, `_URL` absolute, `_KEY`, `_CLASS`, `_MESSAGE`, `_LABEL`. Never the technical
   type (`_LIST`, `_DICT`, `_STR`).
7. **Role, not value.** `ERROR_COLOR`, not `RED`; except palettes and physical facts (`DAY_MS`).
8. **No bare word, even private.** `LABEL`, `VALUE`, `OPTIONS`, `TITLE`, `W` need a subject.
9. **A switch says what it switches.** `IS_…`, `…_STARTS_AT`, `…_ENDS_AT`, named after its effect.
10. **Same meaning, one definition; different meanings, different names.** Values equal by chance
    stay apart.

Final test: "What is ___?" has one answer, file closed.

- [ ] Write it in the charter as `[CONSTANTS]`, reconciled with `[CASE]` and `[NO-MAGIC-VALUES]`.
- [ ] Checked, strict once the debt is zero: 1 and 8.
- [ ] Ratchet: 3 (exported duplicates), 5 (numeric durations without a unit); 4 (leading `MAX_`,
  `DEFAULT_`) and 6 (`_LIST`, `_DICT`) on recognisable cases, 4 on new code only.
- [ ] Review regime: 2, 7, 9, 10.
- [ ] Python (`ast`) and TypeScript/Vue, migrations, generated and vendored code left out; domain
  words stay in each project.
