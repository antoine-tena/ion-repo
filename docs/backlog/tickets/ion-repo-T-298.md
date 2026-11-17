# ion-repo#T-298 · Infrastructure as code: Terraform locked, scanned, private, encrypted
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Every ecosystem, Mature tools as detectors,
  Infrastructure as code), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.61, "Infrastructure as code": Terraform and OpenTofu, Kubernetes and Helm, Ansible:
state out of git, versions pinned, buckets private, pods restricted.

Rule notation: the detector's rung (`L0` to `L7`; `≈` when Claude confirms), `fix S` when a
converter closes the gap or `fix J` when it takes judgment, then the radar level it enters at. Each
rule ships with its passing and failing examples.

- [ ] **B17** Infrastructure as code: Terraform and OpenTofu, Pulumi, CDK, CloudFormation, Bicep,
  Ansible, Helm, Kustomize, Nix (rule ideas, IN).
- [ ] **F11** trivy's config mode or checkov for Terraform, Kubernetes, Helm and Dockerfiles, mapped
  onto the containers and infrastructure rules.
- [ ] **F12** kube-linter or kubeconform for Kubernetes manifests.
- [ ] **IN01** `TF-LOCK`: `.terraform.lock.hcl` committed. L0 · fix S · adopt.
- [ ] **IN03** `TF-VERSIONS-PINNED`: `required_version` and provider constraints set; registry
  modules pinned to versions, git modules to commits. L1 · fix S · adopt.
- [ ] **IN04** `TF-CHECKED`: `fmt -check`, `validate` and tflint in CI (Terraform or OpenTofu). L1 ·
  fix S · trial.
- [ ] **IN05** `IAC-SCANNED`: checkov, Trivy's config scan or KICS in CI. L1 · fix S · trial.
- [ ] **IN06** `NO-PUBLIC-BUCKETS`: storage buckets private unless declared public with a reason;
  public access blocked by default. L1 · fix J · adopt.
- [ ] **IN07** `ENCRYPTED-AT-REST`: databases, volumes and buckets encrypted in the IaC. L1 · fix S
  · trial.
- [ ] **IN08** `K8S-SECURITY-CONTEXT`: `runAsNonRoot`, `readOnlyRootFilesystem`,
  `allowPrivilegeEscalation: false`, capabilities dropped (the restricted Pod Security Standard). L1
  · fix S · adopt.
- [ ] **IN09** `K8S-RESOURCES`: memory requests and limits, CPU requests. L1 · fix S · adopt.
