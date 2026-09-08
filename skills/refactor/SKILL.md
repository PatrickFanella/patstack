---
name: refactor
description: Behavior-preserving refactoring and code simplification; plan changes when requested and verify public contracts.
---

# refactor

Preserve observable behavior and existing repository conventions. Select cleanup or a refactor plan; planning does not authorize implementation or filing an issue. Use codemod-surgeon for repeated structural transformations.

## Select a mode

- Remove AI-generated code slop and clean up code style. Read [the procedure](references/modes/deslop/guide.md).
- Surgical code refactoring to improve maintainability without changing behavior. Read [the procedure](references/modes/refactor/guide.md).
- Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Read [the procedure](references/modes/request-refactor-plan/guide.md).
- Simplifies code for clarity without changing behavior. Read [the procedure](references/modes/simplify/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [laziness protocol](references/principles/laziness-protocol.md) — consult only for this specific design or execution concern.
- [migrate callers then delete legacy apis](references/principles/migrate-callers-then-delete-legacy-apis.md) — consult only for this specific design or execution concern.
- [minimize reader load](references/principles/minimize-reader-load.md) — consult only for this specific design or execution concern.
- [subtract before you add](references/principles/subtract-before-you-add.md) — consult only for this specific design or execution concern.
