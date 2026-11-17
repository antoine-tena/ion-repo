# ion-repo#T-421 · `/repo:release` proves the deployment started, not only the merge into `main`
- **Type**: bug
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-02, a site's release v0.4.0 (18:23–18:34)

After the merge into `main` and the tag, the release waited ten minutes before seeing that the host
had built nothing: the repo had moved to an organisation and the host's Git build was still tied to
the old repo, so a push to `main` triggered nothing, silently. Within a minute of the push, the
skill reads the host's last deployment (Cloudflare Workers: `wrangler deployments list`; VPS: the
running image's tag) and stops on "no deployment started", naming the likely cause (Git build
disconnected, wrong production branch) and the direct link to its settings.
- [ ] A deployment older than the tag after one minute is reported, not waited on.
- [ ] Reproduced on a copy with the Git build disconnected.
