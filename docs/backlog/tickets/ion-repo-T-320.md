# ion-repo#T-320 · Rust read: Cargo, clippy, editions, `unsafe`, locks
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-308 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, Mature tools as detectors, Concurrency, Supply chain)

Planned in v0.7.14, "Rust repos, read": Cargo, clippy, the edition and `unsafe` read, `Cargo.lock`
held to the rules that span stacks.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B07** Rust: Cargo.lock committed, clippy, rustfmt, cargo-deny or cargo-audit,
  `rust-version`, the edition, `unsafe` justified, cargo-semver-checks for libraries. Axum and Actix
  Web recognised.
- [ ] **F10** (Rust's part) cargo-deny for Rust.
- [ ] **CC11** `RUST-NO-STATIC-MUT`: no `static mut`. L2 · fix J · adopt.
- [ ] **SU33** (Rust's part) `LOCKS-COMMITTED`: `Cargo.lock` committed. L0 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Rust repos too, each with a passing and a failing example from Rust.
