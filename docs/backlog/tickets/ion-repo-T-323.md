# ion-repo#T-323 · The C# pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-311 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Stack packs)

Planned in v0.7.7, "The C# pack": NuGetAudit, lock files, warnings as errors and a pinned SDK, then
the rules of ASP.NET Core and Blazor, counted once ten corpus repos of C# were checked (B24).

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **SP17** C# · `CENTRAL-PACKAGES`: `Directory.Packages.props` and lock files
  (`RestorePackagesWithLockFile`). L1 · fix S · trial.
- [ ] **SP18** C# · `NUGET-AUDIT`: NuGetAudit on, transitive packages included, high findings as
  errors. L1 · fix S · adopt.
- [ ] **SP19** C# · `WARNINGS-AS-ERRORS`: `TreatWarningsAsErrors` and a current `AnalysisLevel` in
  `Directory.Build.props`. L1 · fix S · trial.
- [ ] **SP20** C# · `DOTNET-SUPPORTED`: the target framework on a supported .NET release. L1 · fix S
  · adopt.
- [ ] **SP21** C# · `GLOBAL-JSON`: the SDK pinned in `global.json` with a `rollForward` policy. L1 ·
  fix S · trial.
- [ ] Ten corpus repos of C# scored and their findings checked before the pack counts (B24), each
  false alarm fixed in the engine.
