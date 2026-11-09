---
name: safe-refactor-pass
description: Refactor without changing behavior or perform a requested mechanical
  change across many files.
---

# safe-refactor-pass

Choose semantic restructuring or mechanical rewriting. Establish a baseline and scan for leftovers; preserve unrelated work.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **safe refactor pass**: Use when restructuring or simplifying code without changing behavior, removing AI slop, or writing a refactor plan. Read [the procedure](references/base-workflow.md).
- **sweep rewriter**: Use when one mechanical change must land across many files (renames, API migrations, import rewrites) with AST tools and leftover scans. Read [the procedure](references/modes/sweep-rewriter/guide.md).
