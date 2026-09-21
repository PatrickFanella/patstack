---
name: implementation-plan
description: Plan or implement a bounded feature from a spec; map acceptance criteria to changes and executable verification.
---

# Implementation Plan

Turn a feature request into an executable change sequence. Follow the user's requested stopping point: a planning request produces a plan; an implementation request continues through verification.

Inspect existing interfaces, repository instructions, relevant tests, and current changes. Resolve facts from those sources before asking about a material product choice. Preserve the user's stack and existing work.

For each acceptance criterion, identify the affected boundary, expected behavior, and smallest check that could disprove it. Separate required behavior from optional improvements. If the change is small, keep this mapping in the response rather than creating a planning file.

For larger changes, use the repository's existing plan location and record:

- Ordered implementation units, their dependencies, and affected files.
- Concrete verification commands or a named check to implement when none exists.
- Compatibility, migration, and rollback requirements only where the change needs them.
- Unresolved decisions with their impact and enough evidence to resolve them.

Prefer units that leave a working, verifiable result. Do not invent code before inspecting the relevant interfaces or require a commit after each trivial step.

When implementation is requested, execute the units using the relevant language or framework guidance. Update the plan after new evidence changes the approach. Run focused checks as each unit lands and broader checks when shared contracts or integration paths changed. Complete the user-visible flow when it is part of acceptance.

Report which acceptance criteria are verified, which remain unverified, and why. A request to plan or implement does not by itself authorize publishing, deployment, messages, or unrelated repository changes.

## Conditional design notes

- [guard the context window](references/principles/guard-the-context-window.md) — consult only for this specific design or execution concern.
- [never block on the human](references/principles/never-block-on-the-human.md) — consult only for this specific design or execution concern.
- [outcome oriented execution](references/principles/outcome-oriented-execution.md) — consult only for this specific design or execution concern.
- [sequence verifiable units](references/principles/sequence-verifiable-units.md) — consult only for this specific design or execution concern.

For requested “show me your work” or a long unattended effort, use the [decision trail](references/decision-trail.md) beside the existing plan.
