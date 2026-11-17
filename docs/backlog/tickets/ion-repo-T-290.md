# ion-repo#T-290 · JavaScript beyond Nuxt: every framework and package manager
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Application security), made a
  ticket on 25 October 2026 at antoine's request

Planned in v0.6.56, "JavaScript beyond Nuxt: the fronts": Every JS framework and package manager
read; Next.js, React, React Router, Angular, Vue without Nuxt, Svelte and Astro each with its pack,
Electron and Tauri locked down.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B04** JavaScript and TypeScript beyond Nuxt: Next.js, React Router 7, Astro, SvelteKit,
  SolidStart, Angular, Vite with React or Vue, Express, Fastify, NestJS, Hono, Koa, Electron, Tauri,
  React Native and Expo.
- [ ] **B05** Every JS package manager read: npm, Yarn classic and Berry (PnP, `.yarnrc.yml`), pnpm,
  Bun, Deno (deno.json, deno.lock, JSR), corepack's `packageManager`.
- [ ] **AS43** `ELECTRON-SAFE`: `contextIsolation` on, `nodeIntegration` off, `sandbox` on. L2 · fix
  S · adopt.
- [ ] **FP27** Tauri · `TAURI-CAPABILITIES`: the capabilities of Tauri 2 grant each window only the
  commands it uses, and a CSP is set. L1 · fix J · adopt.
