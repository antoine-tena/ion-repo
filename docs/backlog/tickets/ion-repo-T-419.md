# ion-repo#T-419 · Astro without a backend: `constants.ts` keeps the backend messages
- **Type**: bug
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: XS · **Owner**: — · **Due**: —
- **Origin**: rehearsal of the Ion family on a made-up salon, `ion-repo-sandbox/neufs/salon/ciseaux-de-lorvane`, 2026-11-02

A `--type site --frontend astro` project (backend `none`) gets five `BACKEND_*` constants in
`frontend/src/constants.ts` ("Le backend ne répond pas : lancez-le avec ion repo dev."), used by
nothing (`grep -rn BACKEND_ frontend/src`). A defect of a generated file, to fix in the template
under `{% if backend != "none" %}`.

Reproduce: `ion repo new /tmp/x --type site --frontend astro --size small --language fr
--no-github`, then read `/tmp/x/frontend/src/constants.ts`.
