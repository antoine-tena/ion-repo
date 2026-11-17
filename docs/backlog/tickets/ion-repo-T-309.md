# ion-repo#T-309 · The Go pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (Rust in ion-repo#T-321)

Planned in v0.7.13, "The Go pack": Go's own rules with their examples and converters, from a tidy
`go.mod` to no `panic` in a library, counted once ten corpus repos of Go were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP01** Go · `GO-MOD-TIDY`: `go mod tidy` would change nothing. L4 · fix S · adopt.
- [ ] **SP02** Go · `GO-LINT`: `go vet` and golangci-lint (its v2 config) in CI. L1 · fix S · adopt.
- [ ] **SP03** Go · `GOVULNCHECK`: govulncheck in CI, which reports only the vulnerable code a
  program reaches. L1 · fix S · adopt.
- [ ] **SP04** Go · `GO-TOOLCHAIN-SUPPORTED`: the `go` directive and `toolchain` on one of the two
  supported releases. L1 · fix S · adopt.
- [ ] **SP05** Go · `GO-CONTEXT-FIRST`: `context.Context` as first parameter, never stored in a
  struct. L2 · fix J · trial.
- [ ] **SP06** Go · `GO-NO-PANIC-IN-LIBS`: no `panic` on a library's ordinary paths. L2 · fix J ·
  trial.
- [ ] Ten corpus repos of Go scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
- [ ] **FP28** Go · `GO-HTTP-TIMEOUTS`: an `http.Server` with `ReadHeaderTimeout`, never a bare
  `http.ListenAndServe` in a server (gosec G112, G114). L2 · fix J · adopt.
