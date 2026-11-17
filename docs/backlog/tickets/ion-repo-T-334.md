# ion-repo#T-334 · A million files: sampling, Rust where a profile points, the speed published
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-317 on 25 October 2026 (kiln score ideas of 24 October 2026: Speed)

Planned in v0.8.6, "A million files": Sampling with a stated margin, Rust only where a profile
points, then the speed published as uv and ruff publish theirs.

- [ ] **J14** A resident process only if measurements demand it, as language servers do; never by
  default.
- [ ] **J15** Rust only where a profile points: the walker, glob matching and the multi-pattern scan
  are the candidates (a `kiln-core` wheel through PyO3), or ripgrep's engine through `rg --json`
  when installed.
- [ ] **J18** Metrics sampled on huge repos with a stated margin (sizes, complexity); security rules
  always exhaustive.
- [ ] **J20** Speed published as uv and ruff publish theirs: "0.3 s on Django's own repo, 4 s on a
  million files". Speed is part of the pitch.
