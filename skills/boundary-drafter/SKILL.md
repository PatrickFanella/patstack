---
name: boundary-drafter
description: Design or critique architecture and module boundaries, compare interface
  alternatives, or plan deeper modules.
---

# boundary-drafter

Keep design and implementation separate when the user asks for design only. Parallel alternatives require an explicit delegation request or applicable authorization.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **boundary drafter**: Use when deciding module boundaries, Clean/Hexagonal/DDD structure, CQRS, deep-module design, or a project's domain glossary and ADRs. Read [the procedure](references/base-workflow.md).
- **module deepener**: Architecture deepening: find shallow modules and refactors that improve testability, guided by CONTEXT.md and ADRs. Read [the procedure](references/modes/module-deepener/guide.md).
- **interface design twice**: Interface alternatives: design a module or API several radically different ways in parallel and compare them, for 'design it twice'. Read [the procedure](references/modes/interface-design-twice/guide.md).
- **sketch first design**: Use for /architect or architect this: sketch types, signatures and module boundaries with parallel candidates before writing code, then implement against the chosen sketch. Read [the procedure](references/modes/sketch-first-design/guide.md).
