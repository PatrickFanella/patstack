---
name: codemod-surgeon
description: Use when one mechanical change must land across many files (renames, API migrations, import rewrites) with AST tools and leftover scans. Not for behavior changes or a one-file refactor.
compatibility: Requires Python 3 for the bundled leftover scanner; AST-aware rewrites require an available codemod or ast-grep runtime.
metadata:
  blacktower-pack: engineering
  blacktower-kind: tool-wrapper
  blacktower-tier: standard
  blacktower-capabilities: dev-workflows,codemod,surgeon
---

# Codemod Surgeon

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

- [build the lever](references/principles/build-the-lever.md) — consult only for this specific design or execution concern.
- [encode lessons in structure](references/principles/encode-lessons-in-structure.md) — consult only for this specific design or execution concern.
