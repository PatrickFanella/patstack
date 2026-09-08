---
name: typescript-pro
description: TypeScript type design, compiler configuration, and migrations; load framework guidance only for framework-specific work.
---

# typescript-pro

Respect the existing module system and compiler configuration. Model external values at boundaries; justify assertions rather than treating every cast as a defect. Module-boundary enforcement and shoehorn migrations run only when explicitly requested.

## Select a mode

- Migrate test files from `as` type assertions to @total-typescript/shoehorn. Read [the procedure](references/modes/migrate-to-shoehorn/guide.md).
- Only when explicitly requested: Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. Read [the procedure](references/modes/setup-ts-deep-modules/guide.md).
- TypeScript best practices. Read [the procedure](references/modes/typescript-best-practices/guide.md).
- TypeScript-first JavaScript/Node development skill. Read [the procedure](references/modes/typescript-pro/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [type system discipline](references/principles/type-system-discipline.md) — consult only for this specific design or execution concern.
