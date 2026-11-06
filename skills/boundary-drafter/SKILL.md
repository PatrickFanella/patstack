---
name: boundary-drafter
description: "Use when deciding module boundaries, Clean/Hexagonal/DDD structure, CQRS, deep-module design, or a project's domain glossary and ADRs. Not for local cleanup (safe-refactor-pass), hunting shallow modules to refactor (module-deepener) or enforcing TS package boundaries (ts-type-design)."
---

# boundary-drafter

Choose a structure from the actual callers and invariants. Domain vocabulary, module design, and CQRS are separate modes: load only the mode needed. Produce design artifacts when design is requested; implement only within the requested scope.

## Select a mode

- Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Read [the procedure](references/modes/architecture-patterns/guide.md).
- Shared vocabulary for designing deep modules. Read [the procedure](references/modes/codebase-design/guide.md).
- Implement Command Query Responsibility Segregation for scalable architectures. Read [the procedure](references/modes/cqrs-implementation/guide.md).
- Build and sharpen a project's domain model. Read [the procedure](references/modes/domain-modeling/guide.md).
- Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Read [the procedure](references/modes/ubiquitous-language/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [boundary discipline](references/principles/boundary-discipline.md): read when adding, moving or removing input validation at a boundary.
- [exhaust the design space](references/principles/exhaust-the-design-space.md): read when a consequential design choice is still uncertain.
- [experience first](references/principles/experience-first.md): read when a structural choice changes the user journey or accessibility.
- [foundational thinking](references/principles/foundational-thinking.md): read before adding behavior that depends on unsettled data structures, ownership or invariants.
- [model the domain](references/principles/model-the-domain.md): read when the data model allows contradictory states.
- [redesign from first principles](references/principles/redesign-from-first-principles.md): read when a new requirement exposes a structural mismatch.
- [separate before serializing shared state](references/principles/separate-before-serializing-shared-state.md): read when several writers share one resource.
