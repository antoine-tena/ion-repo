# ion-repo#T-308 · Go read: modules, toolchains, race tests, errors
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors,
  Concurrency, Errors and logs, Supply chain), made a ticket on 25 October 2026 at antoine's
  request; one stack per ticket from the same day (Rust in ion-repo#T-320)

Planned in v0.7.12, "Go repos, read": go.mod, go.sum and the toolchain read, with golangci-lint,
govulncheck, race tests and wrapped errors, `go.sum` held to the rules that span stacks.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B06** Go: go.mod and go.sum, the `go` and `toolchain` directives, golangci-lint, gofmt,
  govulncheck, `go vet`, `-race` in CI, vendoring. Gin, Echo, Fiber and chi recognised.
- [ ] **F10** govulncheck for Go (reachable vulnerabilities only); cargo-deny, `composer audit` and
  bundler-audit come with their stacks (ion-repo#T-320, ion-repo#T-312, ion-repo#T-324).
- [ ] **CC09** `GO-RACE`: `go test -race` in CI. L1 · fix S · adopt.
- [ ] **EL12** `GO-ERROR-WRAPPING`: `fmt.Errorf("…: %w", err)`. L2 · fix J · trial.
- [ ] **SU33** `LOCKS-COMMITTED`: `go.sum` committed (`Cargo.lock` comes with Rust, ion-repo#T-320). L0 · fix
  J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read Go
  repos too, each with a passing and a failing example from Go.
