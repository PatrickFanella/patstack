---
name: architecture-patterns
description: 'Architecture and domain modeling: module boundaries, dependency cycles, CQRS, and domain vocabulary.'
---

# architecture-patterns

Choose a structure from the actual callers and invariants. Domain vocabulary, module design, and CQRS are separate modes: load only the mode needed. Produce design artifacts when design is requested; implement only within the requested scope.

## Select a mode

- Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Read [the procedure](references/modes/architecture-patterns/guide.md).
- Shared vocabulary for designing deep modules. Read [the procedure](references/modes/codebase-design/guide.md).
- Implement Command Query Responsibility Segregation for scalable architectures. Read [the procedure](references/modes/cqrs-implementation/guide.md).
- Build and sharpen a project's domain model. Read [the procedure](references/modes/domain-modeling/guide.md).
- Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Read [the procedure](references/modes/ubiquitous-language/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [boundary discipline](references/principles/boundary-discipline.md) — consult only for this specific design or execution concern.
- [exhaust the design space](references/principles/exhaust-the-design-space.md) — consult only for this specific design or execution concern.
- [experience first](references/principles/experience-first.md) — consult only for this specific design or execution concern.
- [foundational thinking](references/principles/foundational-thinking.md) — consult only for this specific design or execution concern.
- [model the domain](references/principles/model-the-domain.md) — consult only for this specific design or execution concern.
- [redesign from first principles](references/principles/redesign-from-first-principles.md) — consult only for this specific design or execution concern.
- [separate before serializing shared state](references/principles/separate-before-serializing-shared-state.md) — consult only for this specific design or execution concern.
