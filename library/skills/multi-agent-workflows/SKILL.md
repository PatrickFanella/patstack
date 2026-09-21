---
name: multi-agent-workflows
description: Coordinate bounded OpenCode or Blacktower subagents with explicit ownership, dependency-aware sequencing, result handoffs, and integration checks. Use for genuinely parallel work or specialist review; avoid it when one agent can finish the task more cheaply and safely.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: parallel delegation,subagent coordination,file ownership,agent handoff,integration sequencing
  author: blacktower
  version: '2.0'
---

# Multi-Agent Workflows

Delegate only independent, concrete work that benefits from parallelism or a
specialist perspective. The coordinating agent remains responsible for scope,
integration, verification, and the final answer.

## Workflow

1. Split the goal into bounded tasks with explicit outputs and dependencies.
2. Assign each task an owner, allowed files or read-only scope, and acceptance
   criteria. Avoid overlapping write ownership.
3. Pass only the context needed to complete the assignment, including applicable
   repository instructions and known user-owned changes.
4. Run independent tasks in parallel. Keep dependency-bound work sequential.
5. Require each agent to report evidence, unresolved risks, and exact files
   changed. A confident summary is not verification.
6. Integrate centrally, resolve conflicts, run repository-wide checks, and review
   the combined diff for inconsistencies between independently produced work.

## Assignment Contract

Every delegated task should state:

```text
Objective:
Scope and ownership:
Inputs and constraints:
Expected output:
Verification:
Dependencies or handoff target:
```

Use messages for small coordination facts and a structured handoff when another
agent must continue the work. Load the reference material only when choosing a
team shape, resolving file ownership, or designing a multi-stage collaboration.

## Guardrails

- Do not delegate an ambiguous task merely to manufacture parallelism.
- Do not let multiple agents edit the same files without an explicit integration
  strategy.
- Do not accept agent claims without inspecting their output or rerunning the
  appropriate checks.
- Stop or redirect agents whose work has become obsolete after a scope change.

## References

- `references/agent-type-selection.md`
- `references/preset-teams.md`
- `references/file-ownership.md`
- `references/merge-strategies.md`
- `references/messaging-patterns.md`
- `references/full-guide.md`
