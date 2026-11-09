---
name: behavior-proof
description: Verify an implementation, assess repository readiness, or create and
  maintain a project-specific verification workflow.
---

# behavior-proof

Distinguish proof of one changed behavior from whole-repository readiness. Report PASS, FAIL or INCONCLUSIVE with evidence; do not infer deployed behavior from local tests.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **behavior proof**: Use before claiming a UI, CLI, API, build or performance change works: run a conformance, regression or baseline check and report PASS, FAIL or INCONCLUSIVE with evidence. Read [the procedure](references/base-workflow.md).
- **ship check**: Use when asked how complete, ready or viable a repository is: trace claimed capabilities to code and tests; separate implemented, partial, planned, unverified. Read [the procedure](references/modes/ship-check/guide.md).
- **verify skill forge**: Verification skill generator: on /create-verification-skill, write a project-local skill that launches, drives and proves a repo's UI, CLI or service. Read [the procedure](references/modes/verify-skill-forge/guide.md).
- **verify skill audit**: Periodic audit of a project's verification skill and feature map against source and one live session, ending in at most one PR of proven fixes. Use for /maintain-verification-skill. Read [the procedure](references/modes/verify-skill-audit/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
