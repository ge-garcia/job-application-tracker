# AI Usage Documentation

## Tools Used

- Claude Code (CLI) with Claude Opus 5.5 (`claude-opus-5-5`) for sample data
  in `sql/02_seed.sql`

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

## What Worked Well

## What I Modified

## Lessons Learned
