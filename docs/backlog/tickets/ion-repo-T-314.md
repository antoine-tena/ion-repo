# ion-repo#T-314 · iOS, Android and Flutter read: SwiftPM, the manifest, pubspec
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Application security), made a
  ticket on 25 October 2026 at antoine's request; one stack per ticket from the same day (Elixir in
  ion-repo#T-326, C and C++ in ion-repo#T-327, the long tail in ion-repo#T-329)

Planned in v0.7.18, "iOS, Android and Flutter repos, read": SwiftPM, CocoaPods, the Android manifest
and Flutter's pubspec read; App Transport Security and exported components checked.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B12** Swift (SwiftPM, CocoaPods, SwiftLint), Android (manifest, R8), Dart and Flutter
  (pubspec, analysis_options); React Native and Expo (`app.json`, `app.config.*`, `eas.json`);
  Kotlin Multiplatform, Ionic and Capacitor, .NET MAUI's mobile targets; Elixir's part is in ion-repo#T-326.
- [ ] **AS41** `ANDROID-MANIFEST`: not debuggable, no cleartext traffic, backups off, every
  component's `exported` explicit. L1 · fix S · adopt.
- [ ] **AS42** `IOS-ATS`: App Transport Security left on. L1 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  Swift, Android and Flutter repos too, each with a passing and a failing example from Swift,
  Android and Flutter.
