---
name: temporal-workflows
description: Design durable Temporal workflows and verify Python replay, timers, activities
  and determinism.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: backend-architecture,workflow,orchestration,patterns
---

# temporal-workflows

Load design guidance for workflow structure and Python test guidance for replay/time-skipping checks. Replay evidence and real worker or deployment behavior are separate claims.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **temporal flow design**: Temporal workflow design: workflow and activity split, sagas, durable state, determinism and failure recovery for long-running processes. Read [the procedure](references/base-workflow.md).
- **temporal py tests**: Temporal Python tests: replay, time skipping, activity mocks and determinism checks for workflow code. Read [the procedure](references/modes/temporal-py-tests/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
