# ion-repo#T-313 · The PHP pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (Ruby in ion-repo#T-325, Elixir in ion-repo#T-326)

Planned in v0.7.9, "The PHP pack": Strict types, `composer audit` in CI, a supported PHP and no
`phpinfo()` left, then the rules of Laravel, Symfony and WordPress, counted once ten corpus repos of
PHP were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP22** PHP · `COMPOSER-AUDIT`: `composer audit` in CI, `composer.lock` committed for
  applications. L1 · fix S · adopt.
- [ ] **SP23** PHP · `STRICT-TYPES`: `declare(strict_types=1);` in every file. L2 · fix S · adopt.
- [ ] **SP24** PHP · `PHP-SUPPORTED`: `require.php` on a supported PHP line. L1 · fix S · adopt.
- [ ] **SP25** PHP · `NO-PHPINFO`: no `phpinfo()` reachable. L2 · fix S · adopt.
- [ ] Ten corpus repos of PHP scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
