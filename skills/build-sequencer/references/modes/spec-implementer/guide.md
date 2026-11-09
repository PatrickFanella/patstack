# spec-implementer procedure

Invoke this mode only on an explicit request for this procedure.

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
