# sweep-rewriter procedure

Reviewed source clients: codex, claude. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# sweep-rewriter

Use this skill for broad mechanical edits where consistency matters more than
local cleverness.

## Procedure

1. **Define the invariant**
   - What exact old pattern must disappear?
   - What exact new pattern replaces it?
   - Which files are excluded?

2. **Inventory before editing**
   - Search by filename and content.
   - Use AST-aware tools where syntax matters.
   - Save a migration plan using `templates/migration-plan.md` for risky edits.

3. **Edit in narrow passes**
   - Prefer one transformation per commit.
   - Regenerate indexes after moving generated/catalog content.
   - Do not mix behavior changes with mechanical rewrites unless approved.

4. **Prove completion**
   - Search for old names/patterns.
   - Run formatting/lint/typecheck/tests.
   - Document intentional leftovers.

Read `references/codemod-playbook.md` for AST/rewrite strategy. Use
`scripts/find_leftovers.py <pattern> <paths...>` to print remaining literal
matches after a migration.

## Conditional design notes

- [build the lever](references/principles/build-the-lever.md): read when deciding between a script or codemod and direct edits.
- [encode lessons in structure](references/principles/encode-lessons-in-structure.md): read when a recurring failure has a precise invariant that a check could enforce.
