# ion-repo#T-321 · The Rust pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-309 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.15, "The Rust pack": Rust's own rules, from clippy with warnings as errors to a
declared MSRV, counted once ten corpus repos of Rust were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP07** Rust · `CLIPPY-CLEAN`: clippy with warnings as errors in CI, a `[lints]` table in
  `Cargo.toml`. L1 · fix S · adopt.
- [ ] **SP08** Rust · `CARGO-DENY`: cargo-deny (advisories, licences, bans, sources) or cargo-audit
  in CI. L1 · fix S · adopt.
- [ ] **SP09** Rust · `RUST-EDITION-CURRENT`: edition 2024 (stable since Rust 1.85, February 2025).
  L1 · fix J · trial.
- [ ] **SP10** Rust · `RUST-MSRV`: `rust-version` declared and tested. L1 · fix S · trial.
- [ ] **SP11** Rust · `UNSAFE-JUSTIFIED`: every `unsafe` block with a `// SAFETY:` comment (clippy's
  `undocumented_unsafe_blocks`). L2 · fix J · adopt.
- [ ] **SP12** Rust · `NO-UNWRAP-IN-LIBS`: `unwrap` and `expect` counted in library code (clippy's
  `unwrap_used`). L2 · ratchet · trial.
- [ ] Ten corpus repos of Rust scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
