# ion-repo#T-437 · `/repo:release`: a documented path to ship without CI, on the owner's explicit order
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-09
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `/learn:distill` of the sessions of 2026-11-03 to 2026-11-09, three releases of a production repo (10:36, 14:21, 15:58 on 2026-11-04)

- [ ] `--urgent` still requires a green CI, and the rule says a red is fixed first; the owner ordered a deploy without CI three times and each session found the project's bypass by reading its deploy scripts.
- [ ] A flag or step in the skill, only on an explicit order in the conversation, never proposed by Claude.
- [ ] The tag message and the release note record that CI was skipped, and why.
- [ ] The next `/repo:release` runs the skipped CI on that commit.
