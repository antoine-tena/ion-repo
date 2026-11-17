# ion-repo#T-338 · The ASP.NET Core and Blazor pack
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: framework coverage review of 26 October 2026 at antoine's request: the most used
  frameworks of the 2025 surveys checked against the plan; the pack of its language held only the
  language's rules

Planned in v0.7.7, "The C# pack": NuGetAudit, lock files, warnings as errors and a pinned SDK, then
the rules of ASP.NET Core and Blazor, counted once ten corpus repos of C# were checked (B24).

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **AS07** (ASP.NET Core's part) `PUBLIC-ROUTES`: a fallback authorization policy that requires
  an authenticated user, every `[AllowAnonymous]` deliberate. L2 · fix J · adopt.
- [ ] **AS22** (ASP.NET Core's part) `CSRF-ON`: antiforgery on for forms and Blazor, each
  `[IgnoreAntiforgeryToken]` with a justification marker. L2 · fix J · adopt.
- [ ] **AS20** (ASP.NET Core's part) `NO-HARDCODED-PASSWORDS`: no password in a connection string of
  `appsettings*.json`; user secrets in development, the environment or a vault in production. L1 ·
  fix J · adopt.
- [ ] **AS45** (ASP.NET Core's part) `FRAMEWORK-DEBUG-OFF`: `UseDeveloperExceptionPage` only in the
  Development environment. L2 · fix S · adopt.
- [ ] **AS35** (ASP.NET Core's part) `HTTPS-ONLY`: `UseHttpsRedirection` and `UseHsts` outside
  development. L2 · fix S · adopt.
- [ ] **AS36** (Blazor's part) `NO-SECRETS-IN-FRONT`: nothing secret in the
  `wwwroot/appsettings*.json` of a Blazor WebAssembly client, which every visitor downloads. L1 ·
  fix J · adopt.
- [ ] **AS48** (EF Core's part) `NO-SQL-INJECTION`: `FromSqlRaw` and `ExecuteSqlRaw` never given an
  interpolated string (`FromSql` takes one safely). L2 · fix S · adopt.
- [ ] **DM18** (EF Core's part) `ORM-MIGRATIONS-COMMITTED`: EF Core migrations committed. L0 · fix J
  · adopt.
- [ ] Ten corpus repos of ASP.NET Core and Blazor scored and their findings checked before the pack
  counts (B24), each false alarm fixed in the engine.
