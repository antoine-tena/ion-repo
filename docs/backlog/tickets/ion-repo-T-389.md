# ion-repo#T-389 · The server leaves ion-repo for ion-host
- **Type**: task
- **Priority**: 🟠 important
- **Status**: blocked — waiting for ion-host#T-07 and ion-host's repo made public (antoine)
- **Opened**: 2026-10-30
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: ion-repo#T-387. ⚠ breaking: the generated tree, the `deploy` question of `copier.yml`,
  `--vps`, the `vps` plugin's skill names; its conversion ships in `kiln update`

- [x] Remove the `vps` plugin (`deploy`, `prod-dump`, `prod-logs`): its skills are ion-host's
  `host` plugin, which the template enables for `deploy=vps`; no forward, `ion repo update`
  rewrites `/vps:…` into `/host:…` (2026-11-02).
- [ ] Remove `config/vps/`, `scripts/ops/` and `docs/operations/` from the template, once ion-host's
  piece renders them byte for byte and ion-host's repo is public (docs/reference.md, "Pieces of
  other Ion tools"). The `frontend_deploy == "vercel"` script of `scripts/ops/` is decided there too.
- [ ] Split `production.md`: it is also generated without a VPS (`podman`, any size above `tiny`),
  so only the server part leaves.
- [ ] Step 8 "Deploy" of `/kiln:release` calls hearth.
- [ ] Decide what becomes of `kiln new --vps` and the `deploy` question.
- [ ] Until then, new server know-how goes to hearth, not here.
