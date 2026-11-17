# ion-repo#T-322 · C# and .NET read: projects, central packages, nullable, supported lines
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: split from ion-repo#T-310 on 25 October 2026, one stack per ticket (kiln score ideas of 24
  October 2026: Every ecosystem, API, contracts and typing, Supply chain)

Planned in v0.7.6, "C# and .NET repos, read": Projects, solutions and central package management
read, with nullable references and the supported .NET lines.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B09** C# and .NET: .csproj, .sln and .slnx, central package management,
  `packages.lock.json`, `<Nullable>enable`, analyzers, `dotnet format`, `global.json`, supported
  .NET lines. ASP.NET Core (`Program.cs`, minimal APIs or controllers), Blazor Server and
  WebAssembly, EF Core, user secrets. Visual Basic and F# projects read alike; WPF, WinForms and
  .NET MAUI recognised.
- [ ] **AT25** `CSHARP-NULLABLE`: `<Nullable>enable</Nullable>` in every project. L1 · fix S ·
  adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read C#
  repos too, each with a passing and a failing example from C#.
