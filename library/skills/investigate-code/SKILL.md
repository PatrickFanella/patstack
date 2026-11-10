---
name: investigate-code
description: Investigate a codebase, explain a flow or design decision, or inspect
  a lockfile-pinned dependency implementation.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: dev-workflows,deep,research
  stage: tool
  tags: research
allowed-tools: Read Grep Glob
---

# investigate-code

Return cited source findings without editing. Explain what the code does separately from evidence of why it was chosen. Dependency research must use the pinned version.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **research a repository**: Repository research: investigate how something works across this codebase and return cited findings, key files and open questions, without editing. Read [the procedure](references/base-workflow.md).
- **code walkthrough**: Code walkthrough: explain how a subsystem or flow works, or where code should live, before changing it; optional architecture critique. Read [the procedure](references/modes/code-walkthrough/guide.md).
- **rationale dig**: Why questions: design rationale, 'why we picked Y', regressions, postmortems or data-backed thresholds, answered with cited evidence from git, trackers, docs and chat. Read [the procedure](references/modes/rationale-dig/guide.md).
- **dep source clone**: Use when a question needs a dependency's real source at the lockfile-pinned version: SDK internals, framework behavior, library bugs. Read [the procedure](references/modes/dep-source-clone/guide.md).

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
