# ion-repo#T-348 · Opt-in telemetry: which commands run, and how they end
- **Type**: idea
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-26
- **Effort**: M · **Owner**: — · **Due**: —
- **Origin**: antoine's answers of 26 October 2026 (Q96: "yes, we need telemetry!"), reversing
  S05; decision 19

Which commands strangers run, and where they fail, decides what to merge or drop (ion-repo#T-10). Go chose
opt-in after its 2023 debate, and HN's readers judge a launch on it: opt-in it is.
- [ ] Asked once, at install or at the first command, answer "no" by default; `kiln set
  telemetry=on|off`; `KILN_NO_TELEMETRY=1` and CI (`CI=true`) never send.
- [ ] Sent: kiln's version, the command, its outcome and duration, the OS family, the stack; never
  a path, a repo name, a file's content, an identity. A page of the reference lists every field.
- [ ] An existing service with an EU region and a free tier (to choose with sources), no server
  of kiln's (decision 20).
