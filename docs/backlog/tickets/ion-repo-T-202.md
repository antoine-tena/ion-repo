# ion-repo#T-202 · The roadmap as context packs: estimated, ordered, batched, budgeted
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-25
- **Effort**: L · **Owner**: — · **Due**: —
- **Origin**: kiln score ideas of 24 October 2026 (Outputs and integrations, The roadmap for
  Claude), made a ticket on 25 October 2026 at antoine's request

Planned in v0.5.15, "The roadmap Claude reads without exploring": The input of v0.6.0: each gap a
context pack with its recipe and its proof, ordered by points per token, cut into batches that fit a
session.

- [ ] **L18** `--for-claude`: the roadmap's context packs, token-counted, nothing decorative.
- [ ] **O01** A context pack per gap: the rule (why, recipe, a passing example), the places with
  five lines around each, the repo's own passing example when one exists ("this repo already does it
  right in `x.py`"), the proof command. Claude opens nothing else.
- [ ] **O02** Tokens and effort estimated per item; items ordered by points gained per token.
- [ ] **O03** Dependencies between items (tests before a refactor, types before the compressor, the
  lock before the audit) give a topological order.
- [ ] **O04** Batches: one rule with many places split into chunks of under an hour of session each.
- [ ] **O06** Risk tags: config only, pure refactor, behaviour change, product decision (the skill
  already stops on the last).
- [ ] **O07** Recipes as data for every judgment rule, so two sessions fix a gap the same way (and
  ion-repo#T-137 can turn the recipe into a converter).
- [ ] **O09** `--roadmap --budget 2h`: the best set of items for one session (a knapsack on points
  and effort).
- [ ] **O10** `--roadmap --json` with the packs inline: `/kiln:modernize` reads one document and
  explores nothing.
