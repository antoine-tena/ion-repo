# ion-repo#T-315 · The mobile pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Stack packs), made a ticket on 25 October 2026 at
  antoine's request; one stack per ticket from the same day (C and C++ in ion-repo#T-328)

Planned in v0.7.19, "The mobile pack": What the stores require and what an app bundle gives away:
the privacy manifest, the target SDK, no server secret in the app, signing keys out of git, counted
once ten corpus repos of apps were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP30** Mobile · `IOS-PRIVACY-MANIFEST`: `PrivacyInfo.xcprivacy` declaring the
  required-reason APIs (required by Apple since May 2024). L1 · fix J · adopt.
- [ ] **SP31** Mobile · `ANDROID-TARGET-SDK`: `targetSdkVersion` meets Google Play's current
  requirement, from a dated calendar. L1 · fix S · adopt.
- [ ] **SP32** Mobile · `NO-SERVER-SECRETS-IN-APP`: nothing secret in an app bundle (everything in
  it is public); client keys restricted instead. L2 · fix J · adopt.
- [ ] **SP33** Mobile · `SIGNING-OUT-OF-GIT`: no keystore, `.p12` or provisioning profile committed.
  L0 · fix J · adopt.
- [ ] **SP34** Mobile · `FLUTTER-STRICT`: `analysis_options.yaml` with the strict modes. L1 · fix S
  · trial.
- [ ] Ten corpus repos of apps (iOS, Android, Flutter) scored and their findings checked before the
  pack counts (B24), each false alarm fixed in the engine.
- [ ] **FP37** Expo · `EXPO-SDK-SUPPORTED`: one of the Expo SDKs still supported. L1 · fix J ·
  adopt.
- [ ] **AS36** (Expo's part) `NO-SECRETS-IN-FRONT`: `EXPO_PUBLIC_*` variables too, compiled into the
  app. L2 · fix J · adopt.
