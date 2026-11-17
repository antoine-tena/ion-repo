# ion-repo#T-240 · A report you can share: every format, HTML, `--quiet`, `--porcelain`
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, Trust, privacy and
  safety), made a ticket on 25 October 2026 at antoine's request

Planned in v0.6.28, "A report you can share": Every format a CI or a tool reads, a one-file HTML
report, links to each rule's page and to the line on the forge, nothing personal left in it.

- [ ] **L01** `--format`: text, json, sarif, junit, markdown, html, csv, gitlab-codequality,
  github-annotations, checkstyle.
- [ ] **L04** JUnit XML, each rule a test case, for Jenkins, Azure and any CI's test tab.
- [ ] **L06** A self-contained HTML report in one file: the score, the pillars with their weakest
  themes, findings with snippets, filters, the potential bar, the history curve.
- [ ] **L14** `--quiet` (the number only) and `--porcelain` (stable lines for scripts).
- [ ] **L15** `kiln grid --json`: the whole catalogue for other tools.
- [ ] **L17** `--open`: the HTML report in the browser.
- [ ] **L19** The report's absolute `root` left out by default: it names the user's home when
  shared.
- [ ] **L21** A finding links to its rule's page and to the line on the forge when the remote is
  known (`https://github.com/o/r/blob/<sha>/path#L12`).
- [ ] **S04** Shareable reports: no absolute paths, user names or e-mail addresses.
