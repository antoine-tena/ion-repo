# ion-repo#T-03 · Public launch: date to set, 16:00 Paris, every forum at once
- **Type**: task
- **Priority**: 🟠 important
- **Status**: blocked — waiting for antoine's date (11 November 2026 cancelled by him
  on 30 October 2026: a few more months of work on his machine first)
- **Opened**: 2026-10-15
- **Effort**: M · **Owner**: antoine for Hacker News and Reddit, Claude for the rest ·
  **Due**: —
- **Origin**: GitHub showcase, 15 October 2026; date and gate fixed on 17 October 2026 at
  antoine's request ("a date when I publish on every forum at once, only after a version you
  define")

One launch, everywhere the same afternoon: stars come in a burst, and the launch happens once.
Nothing is posted on a forum before it (ion-repo#T-118 starts after).

**Awaiting antoine's decision** (26 October 2026, decision 1): Hacker News restricts Show HN from
new accounts since March 2026 (https://news.ycombinator.com/showlim) and antoine has no HN
account and no Reddit karma. Proposal: the launch date for the forums that need no history (dev.to,
Bluesky, X, Mastodon, LinkedIn, the university mail, awesome-claude-code), HN and Reddit on the
first Wednesday his accounts are accepted, at the latest v0.6.0. Either way, both accounts are
opened at once and used for real, never about kiln (`urgent.md`).

**The version it waits for: v0.5.0**, and what it has to prove:
- [ ] `kiln-cli` 0.5.0 or later promoted on PyPI; `uvx kiln-cli score` works from an empty
  cache on Linux and macOS, on a repo kiln never saw (ion-repo#T-142).
- [ ] `kiln score` deterministic, offline, without a token, under 5 seconds on a 50,000-line
  repo (ion-repo#T-46); `kiln fix` closes every scriptable gap of `kiln-demo-legacy`, its checks
  still green (ion-repo#T-126 to ion-repo#T-128); kiln-bot runs on a test repo (ion-repo#T-59).
- [ ] `kiln score` on ten known public repos of other stacks (Go, Rust, Ruby, Java, PHP,
  TypeScript) says nothing false about tests, CI and linters, and names at the top the language it
  doesn't score yet: a launch's visitors run it on their own repos, not on Django ones. Measured on
  26 October 2026: 8 false alarms in 6 of 10 such repos (no tests found in a Rust and a Ruby repo,
  no linter in CI where clippy, golangci-lint and RuboCop ran), fixed the same day; one class left,
  a linter run by `npm test`'s script, for ion-repo#T-190.
- [ ] The README's first screen and the docs done, with the demos already recorded (ion-repo#T-30, ion-repo#T-33).
- [ ] kiln passes its own grid, its CI green on `main` (ion-repo#T-90).
- [ ] No open 🔴 ticket.
- [ ] The Hacker News title, text and every answer written by antoine, by hand: HN's
  guidelines say "Please don't put generated text in HN posts" and, for comments, "Don't
  post generated text or AI-edited text"; Claude hands over raw facts only (numbers, links).
  No upvotes asked, no booster comments from friends.
- [ ] Gate checked at 20:00 on the Monday before. One box empty: the launch moves a week, same
  hour. The date moves, never the gate.

**Choosing the date.** A Wednesday: Hacker News readers are there from Tuesday to Thursday. A day
antoine is free to post at 16:00 and answer until midnight (a public holiday in France, if one
fits), away from an election or a big conference, with his Pro quota fresh and a whole week after it
for fixes and answers. 16:00 in Paris is 10:00 in New York and 7:00 in San Francisco: Europe still
at work, the US East Coast in its morning, the West Coast waking up.

**The day** (Paris time; every text written the week before, each in its forum's format):
- [ ] 15:30: last check, `uvx kiln-cli score` on a fresh clone of a public repo; README and
  links.
- [ ] 16:00: Show HN, by antoine: https://news.ycombinator.com/submit (rules:
  https://news.ycombinator.com/showhn.html). The title is antoine's (he
  declined the Dependabot one on 26 October), `kiln score` first. Then antoine's first comment: why, how it works, the
  method of the study.
- [ ] 16:05: the study as a dev.to article and a thread on Bluesky, X and Mastodon, posted by
  Claude (`.devto/`, `.bluesky/`, `.x/`, `.mastodon/`), the AI disclosure only where the platform
  asks (decision 3).
- [ ] The same day, by antoine: a LinkedIn post written by Claude, and a mail to his university's
  students; Discussions' categories ready (ion-repo#T-58).
- [ ] 16:15 to 17:15, a quarter of an hour apart (identical posts at once trip Reddit's spam
  filters), by antoine: https://www.reddit.com/r/ClaudeAI/submit,
  https://www.reddit.com/r/ClaudeCode/submit, https://www.reddit.com/r/django/submit,
  https://www.reddit.com/r/Python/submit (its "Showcase" format: what it does, target audience,
  comparison), https://www.reddit.com/r/Nuxt/submit.
- [ ] The same day, by Claude: awesome-claude-code, through its issue form only, one
  recommendation: https://github.com/hesreallyhim/awesome-claude-code/issues/new/choose
- [ ] Until midnight: every comment answered by antoine, with facts from the study, never an
  argument over taste; pull requests through `/kiln:contribution`; three good first issues open
  (ion-repo#T-98, ion-repo#T-116, a grid rule to add) by `/kiln:good-first-issues`.
- [ ] A week later, with the first numbers: Anthropic's plugin directory, one plugin, `kiln`
  (decision 27): https://clau.de/plugin-directory-submission
- [ ] Never: asking for votes, posting from several accounts, the same text twice without a
  canonical URL.
