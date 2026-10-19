---
name: adopt
description: Bring a repo that kiln did not generate under kiln (kiln adopt) - charter checked after each edit, docs/backlog/ tracking, repo visible in kiln status - on a branch merged afterwards into the integration branch. Use when the user asks to adopt kiln in an existing repo.
---

Talk to the user in their language.

1. The open repo does not follow kiln yet: neither `.copier-answers.yml` (generated: skill
   `/kiln:update`) nor `charter.toml` / `charte.toml` (already adopted); otherwise say so and
   stop. The `kiln` command is installed (`kiln --version`); otherwise give
   `uv tool install kiln-cli` and stop.
2. Ask for the size with the AskUserQuestion tool: `spark` (script, personal tool), `ember` (small
   app, low stakes, the default), `flame` (production, real users), `blaze` (several teams, high
   stakes).
3. Branch `chore/kiln-adopt` in a worktree (skill `/kiln:worktree`), then
   `kiln adopt --size <size>` in that worktree. It adds `charter.toml` (rules that hold anywhere)
   and `docs/backlog/` (kept if it exists), without touching the code.
4. The debt the charter finds (a `Dockerfile`, a `pip install`…): show it and let the user choose,
   rule by rule, between fixing it now, removing the rule from `charter.toml`, or writing the fix
   down as a ticket (skill `/kiln:backlog`). Fix nothing without agreement.
5. Commit (`chore: adopt kiln`), then merge (skill `/kiln:merge`).

## Sum up

Files added, size, debt found and what was done about it. What adoption does not bring yet: the
full template (CI, pre-commit, `.claude/rules/kiln/`), which assumes the layout of `kiln new`;
`kiln update` does not touch an adopted repo.
