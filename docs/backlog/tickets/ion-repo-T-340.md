# ion-repo#T-340 · Game repos: Unity, Godot, Unreal, Roblox, Lua
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: stack coverage review of 26 October 2026, at antoine's request ("sois sûr que kiln
  couvre bien tout"): Lua at 9 % of the 2025 Stack Overflow survey and game repos had two boxes in
  ion-repo#T-300, nothing that read them

Planned in v0.7.20, "Game repos, read and packed": Unity, Godot, Unreal and Roblox repos read on top
of the C# and C++ packs, with Lua and Luau: the engine's version pinned, assets in Git LFS, caches
and builds out of git, no store or signing credential committed.

One pack per ecosystem, each with its facts, rules and examples; they enter in the order the corpus
measures (Part I). Rules already listed in a theme (`GO-RACE`, `LOCKS-COMMITTED`,
`GRADLE-WRAPPER-VERIFIED`, `CSHARP-NULLABLE`, `PHPSTAN-LEVEL`…) aren't repeated.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B14** (Lua's part) Game repos read: Unity (`ProjectSettings/ProjectVersion.txt`,
  `Packages/manifest.json` and its lock), Godot (`project.godot`, GDScript with gdtoolkit's gdlint
  and gdformat, its C# projects), Unreal (`.uproject`, `.uplugin`, `Source/`, `Config/`), Roblox
  (Rojo's `default.project.json`, Wally, Rokit or Aftman), LÖVE; Lua and Luau with selene or
  luacheck, StyLua, Luau's type checker, busted, LuaRocks' rockspecs.
- [ ] **FP39** Unity · `UNITY-REPO`: `.meta` files committed with their assets, `Library/`, `Temp/`
  and builds ignored, large binaries in Git LFS. L0 · fix S · adopt.
- [ ] **FP40** Godot · `GODOT-REPO`: `.godot/` ignored, no signing credentials in
  `export_presets.cfg`. L0 · fix S · adopt.
- [ ] **SP43** Games · `ENGINE-VERSION-PINNED`: the engine's version recorded in the repo (Unity's
  `ProjectVersion.txt`, Godot's `config/features`, Unreal's `EngineAssociation`) and the same in
  CI. L0 · fix J · adopt.
- [ ] **FP41** Unreal · `UNREAL-REPO`: `Binaries/`, `Intermediate/`, `Saved/` and
  `DerivedDataCache/` ignored, `.uasset` and `.umap` in Git LFS. L0 · fix S · adopt.
- [ ] **FP42** Roblox · `LUAU-STRICT`: `--!strict` in Luau modules, selene and StyLua in CI. L1 ·
  fix S · trial.
- [ ] **SP44** Lua · `LUA-LINT`: selene or luacheck and StyLua in CI. L1 · fix S · trial.
- [ ] **AS01** (games' part) `SECRETS`: no keystore, `.p12`, Steamworks or store credential
  committed. L0 · fix J · adopt.
- [ ] The rules that span stacks (`TESTS-PRESENT`, `TESTS-IN-CI`, `LINT-IN-CI`,
  `LOCKED-DEPENDENCIES`, `DEPENDENCY-UPDATES`, `VULNERABILITY-AUDIT`, `SUPPORTED-RUNTIMES`) read
  game repos too, each with a passing and a failing example from Unity, Godot or Lua.
- [ ] Ten corpus repos of games scored and their findings checked before the pack counts (B24),
  each false alarm fixed in the engine.
