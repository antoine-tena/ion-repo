# ion-repo#T-332 · Every machine and every network: macOS, WSL, ARM64, musl, offline, proxies
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-316 on 25 October 2026 (kiln score ideas of 24 October 2026: Every forge,
  CI, host and machine)

Planned in v0.8.3, "Every machine, every network": macOS and WSL tested beside Linux, ARM64 and
musl, air-gapped and corporate networks; native Windows only if ion-repo#T-94 reopens.

- [ ] **C14** kiln score runs on Linux, macOS, WSL and native Windows (it is Python and git) ⚠ ion-repo#T-94
  declined Windows without WSL for kiln as a whole; the score alone may cost little, tested in CI if
  taken.
- [ ] **C15** x86-64 and ARM64 (Apple Silicon, Graviton, Raspberry Pi), glibc and musl (Alpine):
  every bundled tool shipped as a wheel for each, or its rules say "unknown" there.
- [ ] **C18** Air-gapped and corporate networks: offline by default; `--online` honours
  `HTTPS_PROXY` and custom certificate authorities (`SSL_CERT_FILE`); the data bundle downloadable
  as one file (`--data bundle.tar.zst`).
