# ion-repo#T-305 · Compliance views: Scorecard, ASVS, SLSA, the CRA and the EAA
- **Type**: improvement
- **Priority**: ⚪ background
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Mature tools as detectors, Rule format v2 and
  authoring, A grid that stays current, Packs, local rules, standards), made a ticket on 25 October
  2026 at antoine's request

Planned in v0.7.1, "Compliance views": What a company has to show: Scorecard, ASVS, SLSA, CIS, WCAG,
the Cyber Resilience Act and the Accessibility Act, each control covered or honestly listed as not
checkable.

- [ ] **F19** OpenSSF Scorecard's checks redone locally where possible (they need its API
  otherwise): "kiln score covers Scorecard" is a claim worth making (appendix C).
- [ ] **F20** Semgrep-compatible rules ⚠ licences first: the Semgrep registry's rules have their own
  licence, the opengrep engine is LGPL. kiln's own rules stay in ast-grep.
- [ ] **G10** A `standards` table: CWE, OWASP Top 10 and ASVS, OpenSSF Scorecard, SLSA, NIST SSDF,
  CIS benchmarks, WCAG, the EU Cyber Resilience Act, twelve-factor.
- [ ] **Q08** Standards coverage: the share of Scorecard, ASVS level 1, CIS Docker, SLSA build level
  2 and WCAG AA controls that a grid rule covers.
- [ ] **R06** Compliance views (`kiln score --standard scorecard | asvs-l1 | slsa | cis-docker |
  owasp-top10 | wcag-aa | cra | gdpr`): what passes, what fails, and what can't be checked
  statically, honestly listed.
- [ ] **R07** EU Cyber Resilience Act readiness for companies selling software in Europe (reporting
  duties from September 2026, the rest from December 2027): SBOM, a vulnerability policy, security
  updates, a contact.
- [ ] **R08** European Accessibility Act (applied since June 2025): the front-accessibility rules as
  a company's evidence.
- [ ] **R09** The OpenSSF Best Practices badge's questionnaire pre-filled from the findings.
- [ ] **R10** Each security rule traced to its OWASP cheat sheet, so a reviewer can follow every
  rule to its source.
