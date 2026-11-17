# ion-repo#T-345 · The licence: `MIT OR Apache-2.0`, the template's output free of attribution
- **Type**: task
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: S · **Owner**: — · **Due**: before the v0.5.0 candidate
- **Origin**: antoine's answers of 26 October 2026 (Q76: "Apache 2.0 then, I want the best licence
  possible"), decision 28

Apache-2.0 brings a patent grant MIT lacks; offered side by side with MIT, as uv does
(https://docs.astral.sh/uv/reference/policies/license/), it keeps MIT's reach (GPLv2 projects
can take MIT code, not Apache-2.0 code). The cheapest moment is before the launch, while few
outside contributors have code in kiln. antoine said yes to the pair (26 October, follow-up).
- [ ] The three outside authors of kiln's code (@NathanBarrachin: #33, #45, #46, #54 to #56;
  @HarshRajSinghania: #41; @SakarPaisen: #39) are not asked (antoine, 26 October 2026): their
  contributions stay under MIT, as they were given, which the pair allows; `LICENSE-MIT` keeps
  their notice and `CONTRIBUTING.md` says new contributions come under the pair.
- [ ] `LICENSE-MIT`, `LICENSE-APACHE`, `license = "MIT OR Apache-2.0"` in `pyproject.toml` (PEP
  639), the READMEs' licence lines, `CONTRIBUTING.md` (contributions under the same terms).
- [ ] What `kiln new` and `kiln adopt` lay in a repo is the user's: the template's files under
  MIT-0 (no notice to keep), said in the README, so a generated repo carries no kiln licence.
