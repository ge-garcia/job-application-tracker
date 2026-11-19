# AI Usage Documentation

## Tools Used

- Claude Code (CLI) with Claude Opus 5.5 (`claude-opus-5-5`) for sample data
  in `sql/02_seed.sql`
- Claude Code (CLI) with Claude Opus 5.5 (`claude-opus-5-5`, 1M context) for
  the UI component library: Jinja macros in `templates/partials/`, CSS in
  `static/`, `base.html`, and the `/_components` preview page. It read the
  Figma file through the Figma MCP server and checked the result with headless
  Chrome screenshots.
- Claude Code (CLI) with Claude Opus 5.5 (`claude-opus-5-5`, 1M context) for
  integrating the `feat/ui` macros into `templates/companies.html`, plus the
  shared page layout classes in `static/style.css`, in the merge of the tests
  setup and `feat/ui`. It checked the views against `assets/figma/companies.png`
  with headless Chrome screenshots and ran the existing test suite.

## Key Prompts

1. "Help me generate sample data. Want a reasonable distribution of average
   companies, jobs, and contacts. A good quantity of samples enabling ease in UI
   development convenience would be good, as well as handling edge cases and
   paving the road for tests on them. Write it into `sql/02_seed.sql`. Use
   `sqlfluff` for linting and formatting. Do not run stateful commands regarding
   the database, the user will run this on a fresh Docker volume at the end of
   the turn. Write it one, clean, descriptive `jj` change in the style of the
   rest of the repository. Make sure to do it on with `jj new` on the currently
   edited change (@), model refactoring."
2. "Goal: reusable Jinja macros + CSS for the Figma component library. Read
   first: assets/figma/components.png (look at it),
   src/jot/static/{theme,style}.css, src/jot/templates/base.html. Use only the
   variables in theme.css (Flexoki). No new hex colors, no inline styles, no JS
   beyond what `<dialog>` needs. base.html: nav for Dashboard, Companies, Jobs,
   Applications, Contacts, Job Match, flash area. templates/partials/: one macro
   file each for button, field (label + input + error), stat card, status chip,
   data table row with ⋯ menu, delete `<dialog>` posting to /x/<id>/delete,
   empty state, detail item, match result. Add a throwaway /_components page
   that renders every macro, so it can be compared against components.png. Out
   of scope: page templates, routes other than /_components, Python." (Plus the
   Figma links and `jj` workflow, commit, and file-ownership instructions.)
3. "In this merge commit, go ahead and integrate our components from the
   feat/ui bookmark into the new companies template. Update AI_USAGE.md
   accordingly."

## What Worked Well

## What I Modified

## Lessons Learned
