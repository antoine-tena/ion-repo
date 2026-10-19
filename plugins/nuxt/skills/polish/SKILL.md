---
name: polish
description: Visual audit of a page of the site with screenshots (desktop and mobile), a list of finish defects, then fixes. To make a page worthy of a high-end site.
disable-model-invocation: true
argument-hint: "<page path, e.g. /events>"
---

Page: `$ARGUMENTS`. Apply the project's visual direction skill if it has one (`design-system`
or equivalent) and the frontend rules (`.claude/rules/`, `CLAUDE.md` of the frontend).
Project skills: !`ls .claude/skills 2>/dev/null | tr '\n' ' '`

1. **Prepare**: work on a dedicated `style/…` branch, in its worktree (skill `/kiln:worktree`).
   Start the frontend with the project's dev skill (`dev`) if nothing listens on its port.
2. **Capture** with this plugin's Playwright MCP server (configurable through `/mcp`), or the
   `/nuxt:preview` skill, screenshots in the scratchpad: the page at 1440 px and 375 px, at the
   top then scrolling, plus reachable states (button hover, open menu, empty form, validation
   error, loading if it can be triggered).
3. **Critique like an art director**: a table of defects, from most to least visible, in these
   families: hierarchy and typography, alignment and spacing, colors and contrast, consistency
   with the rest of the site, images, missing states (empty, loading, error), motion and
   micro-interactions, mobile, accessibility. For each: what is wrong, why it looks "cheap",
   the fix.
4. **Suggest** 1 to 3 "wow effect" ideas suited to the page (reveal on scroll, animated
   figures, light parallax, video header…), without hurting performance.
5. **Fix** directly: Tailwind in the components, following the frontend style rules, reusing
   the existing UI components.
6. **Recapture** the same views and show before/after. Commit on the work branch.
