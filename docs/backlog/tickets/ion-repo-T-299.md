# ion-repo#T-299 · Kubernetes, Helm and Ansible by the book
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Infrastructure as code), made a ticket on 25
  October 2026 at antoine's request

Planned in v0.6.61, "Infrastructure as code": Terraform and OpenTofu, Kubernetes and Helm, Ansible:
state out of git, versions pinned, buckets private, pods restricted.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **IN10** `K8S-PROBES`: readiness and liveness probes on different endpoints. L1 · fix S ·
  adopt.
- [ ] **IN11** `K8S-NO-LATEST`: no `:latest` or untagged image (`IMAGES-BY-DIGEST` reads manifests
  too). L1 · fix S · adopt.
- [ ] **IN12** `K8S-NETWORK-POLICIES`: a default-deny NetworkPolicy per namespace. L1 · fix J ·
  trial.
- [ ] **IN13** `K8S-SECRETS-EXTERNAL`: no Secret manifest holding real data; External Secrets,
  Sealed Secrets or sops instead. L1 · fix J · adopt.
- [ ] **IN14** `K8S-SUPPORTED-APIS`: no API version Kubernetes has removed (`extensions/v1beta1`,
  `policy/v1beta1`), from pluto's data. L1 · fix S · adopt.
- [ ] **IN15** `HELM-CHARTS`: `values.schema.json` present, `Chart.lock` committed. L0 · fix J ·
  trial.
- [ ] **IN16** `ANSIBLE-LINT`: ansible-lint clean, secrets in Vault rather than plain variables. L4
  · fix J · trial.
- [ ] **IN17** `IAC-TAGS`: resources tagged with an owner and a cost centre, for company profiles.
  L1 · fix S · assess.
