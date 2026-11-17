# ion-repo#T-327 · C and C++ read: CMake, Meson, Bazel, Conan, vcpkg
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-314 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem)

Planned in v0.7.10, "C and C++ repos, read": CMake, Meson, Bazel, Conan and vcpkg read, with
clang-format, clang-tidy, sanitizers and fuzzing.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B13** C and C++: CMake, Meson, Bazel, Conan and vcpkg manifests, clang-format, clang-tidy,
  sanitizers and fuzzing in CI, warnings as errors. Firmware too: PlatformIO, Arduino, ESP-IDF and
  Zephyr projects, their board and toolchain pinned.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read C
  and C++ repos too, each with a passing and a failing example from C and C++.
