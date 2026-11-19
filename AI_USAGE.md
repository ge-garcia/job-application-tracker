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
- Claude Code (CLI) with Claude Opus 5.5 (`claude-opus-5-5`, 1M context) for
  the jobs, applications, and contacts pages (in `templates/_stubs/`), the
  dashboard, Job Match, and 404/500 pages, `DashboardRepository`,
  `services/match.py`, the dashboard, match, and errors routes, and their
  tests. It checked each page against `assets/figma/` with headless Chrome
  screenshots on a separate Docker stack and ran the test suite.

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
4. "You are building the server-rendered Jinja page templates for `jot`, a
   Flask + MySQL job application tracker (COP-4751 final project). The routes,
   repositories and models already exist. Your job is the HTML that those
   routes render, matching the Figma wireframes." (Plus a read-first list with
   `companies.html` as the reference page, a per-page table for jobs,
   applications, contacts, dashboard, match, and errors, rules for styling,
   delete dialogs, enums, empty states, and forms, specs for the dashboard,
   match, and error routes and `rank_jobs` tests, the `jj` workflow,
   out-of-scope files, and done-when checks.)

## What Worked Well

- Clearly articulated, structured and documented _design_
  - Backend: the architecture and request flow clearly separate concerns, and
    it is all built around a validation core
  - Frontend: Figma design document in prompt links and screenshots in repo
- Core data models and setup done independently prior
- One end to end example prior to asking for generation (i.e. route, repositories, template)
- Original prompts were much longer (shortened here / summarized) and typically followed a structure of
  - Task: what we are doing
  - VCS ceremony: git worktree workflow (through jujutsu VCS)
  - Read first: list of files and documentation pertaining
  - Scope: what files to touch and why (as a table typically)
  - Rules: design ideas related to this task (ranges from typing and code design
    to overarching architecture)
  - Requirements: giving a verifiable goal is kind of critical. in CRUD work
    this is real tests, and in UI it is retaining human in the loop writeoffs
  - Out of scope: avoiding scope creep is huge with this kind of workflow, and
    it pays dividends when merging big worktrees or changes.

## What I Modified

To be honest on most of these the model was capable of doing the work. Followed
my day-to-day work workflow (largely systems and infra at the moment) for
agentic development so the results are the kind of thing I'm used to seeing in
diffs. That being said typical follow up prompts did exist (e.g. 'This test is
superflous' or 'This behavior is ommitted from testing'), and I retained my
typical review flow, steering where necessary.

## Lessons Learned

- Parallel work (even with good use of version control) can be a little tricky
- Glad I did the core data models myself, there was lots of times a prompt
  wanted to change something w.r.t. models and was steered away by strict scoping
- One end to end example prior to handoff was _really_ good, saved me so much
  reiterating of design
- Figma usage was amazing here, having prototypes and style thought through and
  wireframed before handing off dev prompts was great.
