# ion-repo#T-226 · Dockerfiles built right: digests, base images, non-root, stages
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every forge, CI, host and machine, Mature tools
  as detectors, Supply chain, Containers), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.19, "Containers built right": Dockerfiles read stage by stage (v0.6.9): the final
user, multi-stage builds, secrets at build time, exec form, images by tag and digest everywhere.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **C12** Neutral to container engines (Docker, Podman, Buildah, Kaniko, BuildKit): `# syntax=`,
  `--mount=type=secret` and `type=cache`, Bake files, devcontainer.json read.
- [ ] **F08** hadolint's most useful checks rewritten on the parsed Dockerfile (latest tag, root
  user, pipefail, apt hygiene, `ADD` of a URL, exec form) rather than shipping a Haskell binary.
- [ ] **SU04** `IMAGES-BY-DIGEST` (scored): extended to compose, Kubernetes, Helm values and CI
  images, with `ARG` defaults resolved.
- [ ] **SU28** `SUPPORTED-BASE-IMAGES`: Alpine, Debian, Ubuntu and language images on supported
  versions (CURRENT-DEBIAN generalized). L1 · fix S · adopt.
- [ ] **CO01** `NON-ROOT-CONTAINERS` (scored): the final stage's `USER`, not the file's last one; a
  numeric UID so Kubernetes' `runAsNonRoot` can check it; compose's `user:` counted.
- [ ] **CO03** `CURRENT-DEBIAN` (scored): folded into `SUPPORTED-BASE-IMAGES` (SU), the Debian line
  read from the tag or the digest, Alpine and Ubuntu too.
- [ ] **CO05** `MULTI-STAGE`: compilers and dev dependencies left in a builder stage. L2 · fix J ·
  trial.
- [ ] **CO06** `MINIMAL-FINAL-STAGE`: a slim or distroless final image, no shell where none is
  needed. L2 · fix J · trial.
- [ ] **CO07** `TAG-AND-DIGEST`: `image:tag@sha256:…`, the tag kept for humans and update bots. L2 ·
  fix S · adopt.
- [ ] **CO08** `COPY-NOT-ADD`: `COPY` rather than `ADD`, never `ADD` of a URL (hadolint's DL3020).
  L2 · fix S · adopt.
- [ ] **CO09** `APT-HYGIENE`: `--no-install-recommends`, lists removed or a cache mount (DL3015,
  DL3009). L2 · fix S · adopt.
- [ ] **CO10** `CACHE-MOUNTS`: `RUN --mount=type=cache` for uv, pnpm, pip and apt. L2 · fix S ·
  trial.
