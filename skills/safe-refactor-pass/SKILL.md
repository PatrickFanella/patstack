---
name: safe-refactor-pass
description: Use when restructuring or simplifying code without changing behavior, removing AI slop, or writing a refactor plan. Not for repeated mechanical edits across many files (sweep-rewriter).
---

# safe-refactor-pass

Preserve observable behavior and existing repository conventions. Select cleanup or a refactor plan; planning does not authorize implementation or filing an issue. Use sweep-rewriter for repeated structural transformations.

## Select a mode

- Remove AI-generated code slop and clean up code style. Read [the procedure](references/modes/deslop/guide.md).
- Surgical code refactoring to improve maintainability without changing behavior. Read [the procedure](references/modes/refactor/guide.md).
- Create a refactor plan of small verifiable units; file it as an issue on the repository's own forge (Gitea via `tea`, GitHub via `gh`) only when asked. Read [the procedure](references/modes/request-refactor-plan/guide.md).
- Simplifies code for clarity without changing behavior. Read [the procedure](references/modes/simplify/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [laziness protocol](references/principles/laziness-protocol.md): read when choosing how small the change can be, or before deleting an abstraction.
- [migrate callers then delete legacy apis](references/principles/migrate-callers-then-delete-legacy-apis.md): read when retiring an internal API that still has callers.
- [minimize reader load](references/principles/minimize-reader-load.md): read when indirection or hidden mutable state makes code hard to follow.
- [subtract before you add](references/principles/subtract-before-you-add.md): read when obsolete code or duplication sits in the path of the requested change.
