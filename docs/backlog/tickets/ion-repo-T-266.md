# ion-repo#T-266 · Where it deploys: services and deploy configs read, compression, static files
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (One model of the repo, Every forge, CI, host and
  machine, Performance), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.40, "Deploys you can undo": Services and hosts read from every deploy config; health
probes that exist, config that fails fast, OIDC instead of keys, rollbacks, certificates renewed.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **A15** Services read from compose, Kubernetes, Procfile, fly.toml, render.yaml, app.json,
  vercel.json, netlify.toml, wrangler.toml, serverless.yml: databases, caches, queues, search,
  object storage, with their versions.
- [ ] **A16** Where it deploys (a VPS by script, Fly, Render, Railway, Heroku, Vercel, Netlify,
  Cloudflare, Cloud Run, AWS, Azure, Kubernetes, GitHub Pages), which switches the operations rules
  on.
- [ ] **C11** Deploy configs read: Dockerfile, Containerfile, compose, Kubernetes manifests (any
  YAML with `apiVersion` and `kind`), Helm, Kustomize, Skaffold, Tilt, Nomad, systemd units,
  Caddyfile, nginx, Traefik, Fly, Render, Railway, Heroku, Vercel, Netlify, Cloudflare, Firebase,
  App Engine, Serverless, SAM.
- [ ] **PE07** `COMPRESSION`: responses compressed (Caddy's `encode zstd gzip`, nginx's `gzip on`,
  the platform's). L1 · fix S · adopt.
- [ ] **PE08** `STATIC-BY-PROXY`: static files hashed and served by the proxy, WhiteNoise or a CDN
  (`ManifestStaticFilesStorage`), never by the framework's dev server. L2 · fix S · adopt.
