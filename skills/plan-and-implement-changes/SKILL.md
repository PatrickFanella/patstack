---
name: plan-and-implement-changes
description: Plan or execute a feature, specification, migration or multi-session
  implementation sequence.
---

# plan-and-implement-changes

A plan-only request stops at the plan. Spec execution, unusual playbooks and multi-session maps are conditional modes; do not impose test-first work or extra commits on every task.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **build sequencer**: Use when turning a feature spec into an ordered, verifiable change plan, or implementing a multi-step feature against acceptance criteria. Read [the procedure](references/base-workflow.md).
- **build plan writer**: Implementation plan: turn a spec or requirements for a multi-step coding task into a bite-sized, test-first plan before touching code. Read [the procedure](references/modes/build-plan-writer/guide.md).
- **spec implementer**: Implement from spec: on /implement, build work described in a spec or tickets with TDD, regular checks, a code review and a commit. Read [the procedure](references/modes/spec-implementer/guide.md).
- **playbook designer**: Playbook design: on /figure-it-out, design and run an auditable workflow for a large migration or multi-part change that no narrower playbook covers. Read [the procedure](references/modes/playbook-designer/guide.md).
- **wayfinder map**: Wayfinder: plan work too large for one agent session as a map issue of decision tickets on the tracker, then resolve them one at a time. Read [the procedure](references/modes/wayfinder-map/guide.md).
- **pocock flow router**: Use for /ask-matt: choose which Matt Pocock flow or skill fits the situation, from idea to ship, bug hunts, issue triage or codebase upkeep. Read [the procedure](references/modes/pocock-flow-router/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
