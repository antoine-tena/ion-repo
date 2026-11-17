# 🧭 Vision

Why the tickets above exist and how they are judged. Drafted in French on 17 October 2026 from a
long research conversation, two real repos measured that day (the reference repo and a
university repo; the details stay private, see "Repos d'entraînement" in `CLAUDE.md`) and web
research; moved here and condensed on 24 October 2026. What the vision planned became tickets
(the grid as data ion-repo#T-123, `kiln score` ion-repo#T-46, `kiln fix` ion-repo#T-126 to ion-repo#T-128, the roadmap ion-repo#T-129, gap
reports ion-repo#T-38, profiles ion-repo#T-39, the A/B test ion-repo#T-53, tests at the lowest cost ion-repo#T-135
and ion-repo#T-136, the compressor ion-repo#T-138 and ion-repo#T-139, the benchmark ion-repo#T-145); its ideas in reserve and the
paths it dropped are in [rejected.md](rejected.md).

## In one sentence

**kiln keeps a repo up to date with the best of the world (methods, structure, tools,
containers, security, code standards) and easy for Claude to read.** Version numbers matter, but
Dependabot and Renovate already handle them: kiln does the rest. It picks the best tools and
methods, checks they work together, and moves every repo to the next release (the Ubuntu image
stays out of public texts: too abstract, decision 5 of 26 October). The goal: kiln becomes the
reference tool for this problem, measured by adoption (stars, installs), and never something
the next release of an agent makes useless (antoine, 26 October 2026): agent-neutral, scripted,
sourced.

## The problem

1. **The world moves faster than repos.** uv replaced pip, ruff replaced flake8, black and
   isort; containers went rootless, dependency cooldowns appeared in 2025, passkeys took over.
   Nobody tells a repo that a better method exists.
2. **Existing tools stop at versions** (Dependabot, Renovate) **or serve large companies** (AWS
   Transform, Moderne).
3. **Agent-written code speeds up debt.** 90 % of professional developers use an agent every
   week, and about 47 % of their code is written entirely by one (JetBrains, 2026); refactoring
   fell from 21 % of changed lines in 2022 to 3.8 % in 2026 (GitClear).
4. **Nobody has time to review everything.** Code output per developer doubled, reviewers only
   grew 1.5× (CMU and Stanford, 196,000 PRs); PRs with a real human comment fell from 39 % to
   21 %, median review time rose 441 % (Faros); 96 % of developers don't fully trust generated
   code but only 48 % always check it; teams *feel* 20 % faster while being 19 % slower
   (LinearB). Hence "nothing without proof".
5. **Small structures have nobody to keep watch**: an association, a 50-person company, a
   university course whose student team changes every year.
6. **Repos are not laid out for an agent to read.** Every badly split or badly named file is paid
   in tokens, re-reads and mistakes.

## The five pillars

1. **Methods and tools up to date**: a reference grid kept current and applied to the repo
   (tooling, supply chain, containers and operations, tests, application security,
   observability and delivery).
2. **Code standards**: naming, typing, sizes and the rest, enforced rather than advised, in three
   regimes (strict, ratchet, review); the reference repo's charter is the starting base.
3. **Readable by Claude**: a folder per feature, a file per idea (about 50 to 300 lines), names
   that serve as a table of contents, few levels of indirection, the repo map in `CLAUDE.md`,
   tools that read function by function (Serena, LSP). The small-files hypothesis is not proven
   yet (ion-repo#T-53).
4. **Slim down** (a lead): remove unused dependencies and code with a proof that behaviour does
   not change (ion-repo#T-138, ion-repo#T-139). Writing code costs almost nothing now; its mass is the problem.
   The true measure is the surface to review, not the line count; typing helps (the cheapest
   proof, and it removes defensive code): type first, compress after.
5. **Versions**: delegated to Dependabot or Renovate; kiln checks they are set, with a cooldown.

## For whom, and where it starts

- **First** small structures without a platform team: associations, companies of about
  50 people, startups, universities (students, teachers, labs), freelancers, and people who
  build with an agent without knowing how to code: they should code well without knowing it.
  They come to learn to run a project, or to bring an old repo up (`kiln adopt`). **Not at
  first** large companies: AWS and Moderne serve them.
- **Django and Nuxt first**, the reference repo's stacks, brought to the top of the grid; each
  stack counts alone (a Django repo with a React front still gets the Django profile). The
  reference repo is the training ground (its score at every release, ion-repo#T-134); the university repo
  and other ordinary repos are the test for repos kiln did not create, always on local copies.
- **The other templates are frozen** (ion-repo#T-133): generated and tested, no new grid work for them;
  scoring opens stack by stack after the launch (decision 1 of the
  [kiln score ideas](#-kiln-score-the-thesis)).

## The doctrine

There is one way to code, run a repo and run a project: the one kiln holds to be the best
possible, and it is followed. The reference repo's charter is the starting base; after that, the
reference is what comes out in the world, sorted by these principles. gofmt ("nobody's favourite
style, everyone's favourite tool"), Black, Prettier and Rails won this way; create-react-app,
frozen then abandoned in 2025, shows what happens when the one way stops moving.

1. **One way per profile.** For each stack and size of structure, kiln picks one way and holds
   it: an association does not need a large company's SLOs. Where the community is split at
   equal quality, the other way is accepted, never scored down (podman recommended, Docker
   accepted: decision 17 of 26 October). kiln's way is the world's best, not its author's.
2. **The best, not the newest.** A practice enters only once mature (maintained, adopted,
   compatible with the rest of the stack), through four levels: assess, trial, adopt, hold.
3. **Every rule has its why, source and date.** Sources weigh in this order: official docs and
   maintainers' release notes; security advisories (OWASP, OpenSSF, CVE); measured studies;
   adoption data; blogs.
4. **Every rule sits on two axes**: its theme and its scope (universal, language, framework,
   tool, business domain, project). A universal rule may take a project setting: "store dates in
   UTC" is universal, "Europe/Paris" is the project's.
5. **The script first, Claude next.** Whatever a program can check or fix, a program does: exact,
   reproducible, no tokens. Claude gets only what needs judgment, with the exact place and the
   rule; it never walks the repo looking for problems.
6. **Claude invents, the script repeats.** A fix Claude makes twice the same way becomes a rule
   or a converter (ion-repo#T-137): paid once per rule, not once per repo.
7. **A vague rule is worse than none.** A rule that flags wrongly costs tokens and trust; it goes
   strict only once its false positives are under control.
8. **Nothing without proof**: tests, types and CI green, measured before and after.
9. **Explicit exceptions, a gradual path**: a waiver is dated and justified (`kiln waive`); an
   existing repo converges by ratchets, without breaking everything at once.
10. **Readable by Claude** (pillar 3).
11. **The fastest, at equal precision.** A slow check stops being run: the fastest tools among
    those precise and mature enough, only what changed rechecked (cache, changed files,
    parallelism), our own rules declarative for a fast engine such as ast-grep; Rust of our own
    only where a measurement shows our code is the slow part (ion-repo#T-144).
12. **A living choice is never a finding.** The one way governs how a stack is run, never which
    living stack a repo picked: a Django repo is held to Django at its best, never told to become
    FastAPI, since each fits its own job (`kiln new` picks one per job: Django for a full app,
    FastAPI for an API alone). A choice becomes a finding only on dated, sourced facts: its line
    is past its end (`SUPPORTED-FRAMEWORKS`), its maintainers deprecated it and name a successor
    (the `hold` rules), or it is abandoned with open advisories (`ABANDONED-DEPENDENCIES`). kiln
    then names the successor its maintainers name, never one of its own taste, and splits the
    move into steps the score proves, never a rewrite in one go (ion-repo#T-225; antoine's question of
    26 October 2026).
13. **Breadth costs data, not weight.** `kiln new` keeps few complete stacks (decision 1); the
    grid reads every stack, and a stack is mostly facts for the rules that span stacks (about
    four planned rules in five on 26 October 2026; 5 of the grid's 138 rules belong to a
    framework), its own rules a thin layer, its mature tools (Brakeman, Sobelow, SpotBugs…) run
    rather than rewritten. A repo loads only its stacks' rules (ion-repo#T-214), and a rule nobody re-read
    for a year leaves the score (ion-repo#T-140): a pack nobody keeps goes quiet rather than wrong.
14. **No tool invented.** As many tools as possible that spend no tokens, the fastest, and
    existing ones: where a maintained open-source tool does the job, kiln runs it; kiln's own
    code is the glue, the standard and what nobody else does (antoine, 26 October 2026: "invent no
    tool, go find existing repos on GitHub"; ion-repo#T-359).

## How it works: the script finds, Claude judges

Not everything can be checked by a program (whether a name says what it holds, whether an
architecture fits the domain; Rice's theorem), and handing everything to Claude would cost a
fortune: reading the reference repo's Python once (48,616 lines outside tests) is about
500,000 tokens. So five steps, most of them free:
1. **Deterministic audit, no tokens** (`kiln score`): scripts, linters and public APIs measure the
   repo against the grid; a score per pillar and the list of gaps, each with its why, for whom
   and its effort.
2. **Mechanical fixes, no tokens** (`kiln fix`, `kiln update`'s conversions), on a branch.
3. **A roadmap for Claude, targeted tokens** (`kiln score --roadmap`, `/kiln:modernize`): only
   what needs judgment (split a 3,000-line file, rename with meaning, write tests, strict
   typing), each item with its place, rule and why. Most of an agent's tokens go into
   exploring; the roadmap removes that: Claude pays to think, not to search.
4. **Checked by the script** (`kiln score --rule`): a gap is closed only when it leaves the
   measure and tests, types and CI stay green.
5. **Continuously**: each release updates the grid and `kiln update` brings the repos to it,
   candidates first on the `internal` channel.

A repo kiln did not create gets `kiln adopt`, then a test net freezing today's behaviour before
any modernization.

**The circuit.** Updates go down through `kiln update`; gaps come up: where kiln runs, the score
notices what the grid does not know and the rules that get in the way wrongly, and Claude drafts
the report to kiln (ion-repo#T-38). Its rules: never without consent (the user sees exactly what leaves);
anonymised (no code, paths, internal names or secrets, only the gap's signature); one issue per
gap, not per user (a further report adds a voice), a PR only when the fix is obvious and local,
any outside PR through `/kiln:contribution`; a signal, not a decision (the doctrine decides, so
the grid cannot be poisoned by fake reports); the most frequent gaps become tickets first.

**Tests, the most for the fewest tokens**: generators without a model first (Schemathesis,
Hypothesis and CrossHair, snapshots, the Playwright recorder: ion-repo#T-136), holes measured by coverage
and mutation (mutmut, Stryker), Claude on the holes only, a test kept only if it passes five
times and kills a mutant or adds coverage, then ratchets (ion-repo#T-135). Meta's mutation-guided ACH saw
73 % of its generated tests accepted; CoverUp reaches 89 % line and branch coverage on its
benchmark. No tool lifts the last limit: a generated test checks what the code *does*, not what
it *should* do, which is why property tests and killed mutants are worth more than coverage.

## The market (October 2026)

| Player | What it does | What it lacks for our target |
|---|---|---|
| Dependabot, Renovate | Versions, optional cooldown | Neither methods nor standards |
| Copier, cruft (and Renovate's Copier manager) | Template updates | No grid, no method conversions |
| AWS Transform "Continuous Modernization" (preview since 17 June 2026) | Debt, end-of-life dependencies, outdated frameworks across thousands of repos | Large companies, AWS ecosystem |
| Moderne / OpenRewrite ($30M raised) | Recipe migrations, paid multi-repo | Large companies, Java first |
| GitHub Copilot app modernization | Java and .NET upgrades | Two ecosystems |
| Claude Code (`/doctor`, `/skill-doctor`, `claude-code-setup`) | Health of the Claude configuration | Not the rest of the repo |
| sp-repo-review (Scientific Python) | A checklist of scientific Python practices | Checks without applying |
| libyear, depwatch | Dependency lag | Versions only |
| deptry, FawltyDeps, knip, vulture | Unused dependencies and code | Detection only |
| ponytail | Tells agents to write less code | At writing time, not on existing code |
| ECC, Superpowers | Configuration packs for agents | Frozen at install |
| Thoughtworks Technology Radar | Opinions twice a year | Not executable |

**What is missing**: an open, free tool with a grid of methods and standards kept current,
applied with proof to small structures' repos, making them readable by Claude.

**What protects us** is where the big players cannot go, because of their own interests:
Anthropic (outside Claude Code, tedious stack by stack, and a script spends no tokens; only the
Claude configuration's health is its ground), Dependabot and Renovate (their job is raising
versions), AWS, Moderne and GitHub (they sell to large companies: an association never calls
their sales team), hosts (they host, they don't maintain code), funded startups (small
structures don't pay). A chore everyone suffers and nobody wants to own, as with Stripe and
payments; the demand is measured (the university repo). The real risk is a funded startup on the
same angle: speed and open source answer it, and a big player more often buys than rebuilds
(OpenAI bought Astral in March 2026, Anthropic Bun's team in December 2025).

**What makes a tool break out.** uv was no new idea (Poetry, pip-tools, pipx, pyenv, rye): it won
on execution (10 to 100× faster, one tool instead of several, `uv pip` adoptable without
migrating, ruff's credibility), and speed changed habits. The Claude Code projects that exploded
in 2026 share a one-line install, a number in the tagline and a pain felt in the first session.
For kiln: unify scattered tools (Dependabot, linters, templates, checkers like sp-repo-review)
and show a striking number, a before and after score. Distribution weighs as much as the idea
(ECC broke out after a hackathon win, Superpowers on its author's name): hence the launch (ion-repo#T-03).

**What Claude users need** (17 October 2026; JetBrains' survey the soundest source): Claude Code
is used at work by 39 % of professional developers; the needs, strongest first: checking agents'
code; controlling tokens (the category with the most stars: ponytail, cc-switch, caveman, rtk,
headroom); imposing a method (Superpowers, ECC, though ETH Zurich finds context files don't raise
success and cost 20 to 23 % more tokens); securing the agent chain (Clinejection, 1,184 malicious
skills on ClawHub, a quarter of MCP servers unpinned, mods not sandboxed); stability and the
freedom to pick one's agent (AGENTS.md in 60,000+ projects, SKILL.md read by 32+ tools, paths
that differ); understanding and remembering. The grid takes from it: pin MCP servers, avoid
broad permissions, keep context files short and hand-written, keep repos readable by any agent.
The background trend is harness engineering (OpenAI, February 2026): a harness improved from
measurements gains 7 points of success and saves 12 % of tokens.

## Decisions of 26 October 2026

antoine answered 220 questions offline (the file names people and private repos: it lives in
`kiln-measures`). Below, what changes; where he wrote "decide", Claude settled it, with the
reason. ion-repo#T-342 to ion-repo#T-358 come from here; "Q" numbers are the file's.

**Launch (ion-repo#T-03).**
1. Hacker News restricts Show HN from new accounts since March 2026
   (https://news.ycombinator.com/showlim: "take some time to get to know the community",
   criteria vague on purpose), and antoine has no HN account and no Reddit karma (Q11, Q12).
   Proposed to him, his call (the date is his; 11 November cancelled on 30 October 2026): the
   launch date stays for what needs no history
   (dev.to, Bluesky, X, Mastodon, LinkedIn, a mail to his university's students,
   awesome-claude-code); HN and Reddit on the first Wednesday his accounts are accepted, at the
   latest v0.6.0 (a stronger story); both accounts opened at once and used for
   real, never about kiln. Moving everything to v1.0 (Q8) is advised against: seven months without
   strangers' repos to calibrate on, and the name left to whoever ships first.
2. The HN title stays antoine's (he dislikes "Dependabot for your methods"), `kiln score` first.
   LinkedIn: a post the day kiln takes off, written by Claude, posted by antoine. About ten
   people around antoine use kiln, four of them often: ion-repo#T-142 starts with them.
3. Claude never adds "written with Claude" on its own (Q129: "never"); where a platform asks
   (dev.to's AI disclosure tier) the true answer is given, or the post is not made. HN stays
   antoine's words only. The video is silent.

**Promise and README (ion-repo#T-30, ion-repo#T-33).**
4. `kiln score` first, then `adopt` and `new`, which stand on it (Q20, Q21, Q192): the trio is the
   promise. Draft tagline: "Make any repo production-grade: score it, raise it, keep it there".
   antoine wants the best README in the world.
5. The Ubuntu image goes from public texts (too abstract). The grid is called **the kiln
   standard** wherever a user reads it (ion-repo#T-346). The standard is the grid, not the score:
   `kiln score` keeps its name, beside `kiln check` and `kiln ci` (Q113, antoine is fine with
   the three).
6. The score: a number out of 100 in Lighthouse's bands (0-49 red, 50-89 orange, 90-100 green;
   the cap at 49 lands in red by construction), no letter; colourful in the terminal, a Markdown
   page of Mermaid charts on request (ion-repo#T-352).
7. English only for kiln's own docs: ion-repo#T-177 stands (Q27, "do as you like").
8. A sourced why for the README: output per developer doubled while reviewers grew 1.5× (CMU and
   Stanford, in the sources below); "right first costs fewer tokens than refactoring later" only
   with a measure (ion-repo#T-145), otherwise left out.
9. A logo, still and animated, and a mascot to discuss (ion-repo#T-347).

**The study (ion-repo#T-131, ion-repo#T-132, dropped by antoine on 30 October 2026).**
10. Calibration before conclusions: a standard that finds nothing well made is worthless
    (antoine, Q30). Repos known for their quality are scored before the launch; every point they
    lose is a gap their maintainers would recognize, with its source, or a defect fixed first.
11. Scores are reproducible by anyone (as with Scorecard or best-of-python): the article names the
    reference repos and gives the hundred as aggregates, never a list of the worst.
12. A vulnerability found is reported privately (the project's SECURITY.md, GitHub's private
    reporting), never as a public PR first; the credit in the published advisory is the
    publicity antoine wants (Q31). Other PRs: a few, by hand, where CONTRIBUTING welcomes them,
    never in bulk.
13. The university repo is never cited by kiln, not even as aggregates (Q34; one day kiln runs on
    it and a PR goes to its teacher). The association's site is never named (Q35).
14. ion-repo#T-53 before the launch, run once; ion-repo#T-145 matters.

**The standard and the score.**
15. The six decisions of 24 October stand, re-read; the cap at 49 too (SSL Labs' logic: a tracked
    `.env` is an incident, not a style point).
16. Not using an agent is not a fault (Q42, ion-repo#T-342).
17. One recommended way per profile, and an accepted other where the community is split at equal
    quality (Q40, Q41: podman recommended, Docker accepted). Every question kiln asks offers
    "I don't know: choose for me", the recommended answer.
18. Tools move from trial to adopt on Claude's call, with sources (Q43). More profiles (ion-repo#T-39):
    student project, teacher, startup, small company, freelance delivery, open-source project,
    personal project.
19. Telemetry: S05 ("no telemetry, ever") reversed by antoine (Q96): opt-in, anonymous,
    documented (ion-repo#T-348). Gap reports, issues and PRs reach him as a daily mail (ion-repo#T-349).

**kiln fix and kiln-bot (ion-repo#T-59, ion-repo#T-170).**
20. kiln-bot is a workflow each repo installs (free, no server); a hosted App later if kiln grows,
    the association's server lending a little meanwhile. It never breaks production: each commit
    proven (ion-repo#T-170), the PR a proposal the repo's CI judges.
21. `kiln fix --pr` allowed. A fix that turns the repo's tests red leaves the batch, kept on its own
    branch with its log and handed to Claude: never merged red, never dropped silently.

**kiln new and adopt (ion-repo#T-169, ion-repo#T-184, ion-repo#T-188).**
22. Two doors, quick or tailored; the long questionnaire (the machine profile) is asked once at
    install, and at `kiln new` only if never answered. Three concrete questions replace the
    sizes. The frozen templates stay offered, marked frozen with their score; FastAPI at the
    launch: "not yet, report it".

**Plan to 1.0.**
23. Numbering (Q58): antoine wants small patch numbers. antoine said yes the same day to a minor
    every ten releases or so, each a themed milestone holding its breaking changes, as uv and
    ruff do; the plan is renumbered by ion-repo#T-360.
24. The best on every stack (Q59, unchanged); someone antoine knows waits for GitLab; the
    compressor uses proven tools only (vulture, knip), Q62.

**Claude Code, agents, plugins.**
25. kiln's way is the world's best, not antoine's (Q67): the generated flow follows the evidence
    (ion-repo#T-358). Its tools too: token-free, the fastest, existing ones first (Q5, doctrine 14,
    ion-repo#T-359). His own habits (one session, no subagents, CI only at the release) stay his; the
    first two are not generated (checked).
26. Every agent, and none (Q22, Q72, ion-repo#T-357); Claude Code first at the launch, where the audience
    is.
27. The plugin directory lists one plugin, `kiln`; the stack plugins come with `kiln new` and
    `kiln adopt`. Serena stays opt-in (it is), context7 stays (current library docs serve "the most
    up to date"), rtk stays on. Pro plan only.

**Community and money.**
28. Free forever; Sponsors still to open (ion-repo#T-119); no maintainer rights to anyone; Discussions are
    enabled, their categories in ion-repo#T-58. Licence `MIT OR Apache-2.0` (ion-repo#T-345): antoine asked for
    Apache-2.0 as "the best"; the pair keeps Apache's patent grant and MIT's reach, as uv does;
    he said yes to it.
29. Contact: security through GitHub's private reporting (SECURITY.md has it); companies through
    antoine's GitHub and LinkedIn. A kiln page on the association's site is declined (it would
    name it): GitHub Pages, with the docs site after the launch. The site is static (docs, rule
    pages, the leaderboard drawn at build): Pages serves it from the repo, built by a workflow,
    with no other account; Vercel, antoine's first idea, only if a server part comes (ion-repo#T-348's
    collector).
30. antoine can take about 50 issues or PRs a day; each is answered in its own language.

**Way of working.**
31. The backlog is for Claude alone (Q82, Q214): condensed (ion-repo#T-163). It stays in `docs/backlog/`
    (ripgrep skips dot-folders by default; contributors and good first issues read it), with
    `ROADMAP.md` as the human view; launch texts, contacts and metrics go to `kiln-measures`
    (ion-repo#T-350). The plan stays public (contributors, trust, building in public); antoine may still
    ask for it private (Q138).
32. Estimates are ceilings: antoine always goes faster (Q84).
33. CI only at the release stays (nothing slipped through, Q86), as complete and fast as possible
    (Q85, ion-repo#T-354).
34. annway stays off limits, its copy `annway-copie` may serve kiln (the Java pack, ion-repo#T-310); kiln
    trains on sweep and polytech-vision up to 100, in their own sessions (Q91, Q92).
35. Two habits of antoine's global instructions go to every repo (ion-repo#T-343). The repo's update is
    offered outside Claude Code too (ion-repo#T-355); strangers may follow the candidates (ion-repo#T-356). A
    session paused in seconds is found again at the next start (Q6, ion-repo#T-344). The session messages
    stay as they are (Q7): the logo only comes with an update on offer, as a message that costs
    no tokens.
36. The questions file: offered again before big milestones, not every time.

**Security, ideas, commands.**
37. What `kiln score` reads from GitHub's settings stays on the owner's machine; what leaves it
    (badge, report to kiln, a public CI summary) carries the score and rule IDs alone (ion-repo#T-158).
38. Score by URL (ion-repo#T-191); a leaderboard of the best only (ion-repo#T-353); the VS Code extension reopened
    (ion-repo#T-117, free on the Marketplace and Open VSX); Windows without WSL stays declined (ion-repo#T-94), but
    `kiln score` says what to do there instead of failing (ion-repo#T-189); a teacher is ready to try the
    teacher mode (ion-repo#T-87).
39. A quiet launch: same plan, measure, ask the testers, fix the first minute, launch again at the
    next milestone. A loud one: the digest, Discussions, a pinned issue of known problems.
40. `kiln check` (seconds, while coding), `kiln ci` (the whole CI on the machine, before a
    release) and `kiln score` (the repo against the standard), one line each in the README and
    `--help` (ion-repo#T-30): antoine did not know the first two apart (Q113). Merging two waits for
    telemetry (ion-repo#T-10). `kiln dev` must run any repo without being told (Q111, ion-repo#T-351).
41. Waivers keep their expiry (already by tiers); reminders weekly, security at once (ion-repo#T-45).
    Announcements: milestones only, on Bluesky, dev.to, X and Mastodon (ion-repo#T-118); no newsletter
    before 1,000 stars.

**Technical choices** left to "the best in the world" (Q145 to Q180): the standard settles them
rule by rule with dated sources. Held today: Django Ninja for new apps (DRF scored fairly); Celery
until Django 6's `django.tasks` has a mature production backend; Tailwind with tokens (Nuxt UI
weighed as a rule); pnpm; Vitest and Playwright; coverage as a ratchet with profile floors
(Google's 60, 75, 90 %); mutation tests at the release on critical code; strict types for new code,
a ratchet for old; 300 lines a file, strict when new, a ratchet when adopted; no `utils` nor
`helpers`; showcase files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) for public repos only, none
generated today (with the community rules, CM); pre-commit kept; Conventional Commits; semver
after 1.0; `uvx` first; kiln's CLI in English until 1.0; Django with HTMX as a later frozen template.

## Risks and open questions

1. The giants hold the top of the market (AWS made the same promise in June, for large
   companies).
2. The grid is endless work: the starting scope keeps it tractable, the gap circuit feeds it.
3. Agents make applying a change easy for everyone: the value is in the choice and the proof.
4. "The best" depends on the context: profiles of structure (ion-repo#T-39).
5. Old repos without tests break when modernized blind: a test net first.
6. Upkeep tools earn few stars (deptry about 1,000): a striking number is needed (ion-repo#T-145).
7. The small-files hypothesis is not proven (ion-repo#T-53).
8. Gap reports raise privacy, noise and grid poisoning: the circuit's rules above.

## Sources

- Market and usage: [JetBrains, agent adoption 2026](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/) ·
  [GitClear (LeadDev)](https://leaddev.com/ai/code-maintainability-plummets-in-the-ai-coding-era) ·
  [the review bottleneck in numbers](https://www.flowverify.co/blog/ai-code-review-bottleneck-2026-data) ·
  [CMU and Stanford](https://www.matthewswong.com/en/blog/ai-code-review-bottleneck-cmu-stanford-silent-approvals/) ·
  [Pragmatic Engineer, AI tooling 2026](https://newsletter.pragmaticengineer.com/p/ai-tooling-2026) ·
  [Claude Code repos by stars](https://githublb.vercel.app/topic/claude-code) ·
  [agent configuration exposures](https://arxiv.org/abs/2609.07360) ·
  [mods not sandboxed](https://www.dsebastien.net/2026-10-04-claude-code-mods-claude-code-is-now-programmable-and-mods-arent-sandboxed/) ·
  [skill portability](https://codemyspec.com/blog/skill-portability) ·
  [harness engineering](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) ·
  [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)
- Modernization: [AWS Transform](https://aws.amazon.com/blogs/migration-and-modernization/aws-transform-from-migration-to-continuous-modernization/) ·
  [Moderne raises $30M](https://refreshmiami.com/news/moderne-raises-30m-to-continue-driving-mass-scale-code-modernization/) ·
  [OpenRewrite and Moderne](https://moderne.ai/blog/overview-of-openrewrite-and-moderne) ·
  [Copilot modernization](https://theaieconomy.substack.com/p/github-copilot-modernizes-java-dotnet) ·
  [Renovate's Copier manager](https://docs.renovatebot.com/modules/manager/copier/) ·
  [Technology Radar](https://www.thoughtworks.com/radar) ·
  [`/doctor`](https://improveandrepeat.com/2026/10/keep-your-claude-code-configuration-healthy/) ·
  [`/skill-doctor`](https://www.implicator.ai/anthropic-claude-code-skill-doctor-context-audit/) ·
  [OpenAI acquires Astral](https://simonwillison.net/2026/Mar/19/openai-acquiring-astral)
- Readability: [Sonar's study](https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents) ·
  [ETH Zurich, AGENTS.md](https://iclr.cc/virtual/2026/10021142) ·
  [vertical slices and AI](https://jeremydmiller.com/2026/06/04/the-codebase-is-the-prompt-wolverine-vertical-slices-and-ai-assisted-development/) ·
  [an agent-friendly codebase](https://deska.dev/blog/agent-friendly-codebase)
- Slimming: [Meta's SCARF](https://engineering.fb.com/2023/10/24/developer-tools/automating-dead-code-cleanup/) ·
  [TRIM](https://arxiv.org/abs/2607.18161) ·
  ["Software Supply Chains are Dead"](https://arxiv.org/abs/2607.13021) ·
  [Lexo](https://arxiv.org/abs/2510.14522) ·
  [build once, maintain forever](https://expressionsofchange.org/build-once-maintain-forever)
- Tests: [CoverUp](https://dl.acm.org/doi/10.1145/3729398) ·
  [Meta, mutation-guided tests](https://arxiv.org/pdf/2501.12862) ·
  [`hypothesis write`](https://hypothesis.readthedocs.io/en/latest/ghostwriter.html) ·
  [a study of Hypothesis' tests](https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf) ·
  [hypothesis-crosshair](https://github.com/pschanely/hypothesis-crosshair) ·
  [Pynguin](https://arxiv.org/pdf/2007.14049) ·
  [Keploy](https://keploy.io/docs/concepts/what-is-keploy.md)
- Neighbouring tools: [sp-repo-review](https://pypi.org/project/sp-repo-review) ·
  [libyear](https://www.npmjs.com/package/libyear) ·
  [deptry](https://github.com/osprey-oss/deptry) ·
  [FawltyDeps](https://github.com/tweag/FawltyDeps) ·
  [ponytail](https://www.mindstudio.ai/blog/ponytail-ai-coding-minimalism-plugin)
