---
name: define-requirements
description: Resolve requirements and produce a requested PRD, recurring-workflow
  specification or decision questionnaire.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: requirements discovery,acceptance criteria,scope clarification,constraint
    discovery,decision questions
  author: blacktower
  version: '2.0'
---

# define-requirements

Planning and interviewing do not authorize implementation or tracker publication. Select the requested deliverable before proceeding.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **scope grill**: Use when ambiguity in outcome, scope, constraints or acceptance criteria would change the implementation, or on grill-me, grill-with-docs or a plan stress-test. Skip when the repository already answers it. Read [the procedure](references/base-workflow.md).
- **prd from context**: PRD from context: turn the current conversation and codebase understanding into a PRD and file it on the project tracker. Read [the procedure](references/modes/prd-from-context/guide.md).
- **loop spec grill**: Workflow-spec grilling on explicit request: interview the user about recurring loops worth delegating and write implementer-ready specs under workflows/*.md. Read [the procedure](references/modes/loop-spec-grill/guide.md).
- **decision questionnaire**: Questionnaire: turn a decision you can't fully answer into questions for someone else to fill in. Read [the procedure](references/modes/decision-questionnaire/guide.md).

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
