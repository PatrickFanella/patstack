---
name: relay-baton
description: Recall recent work or record a handoff before a context reset, session
  continuation or explicitly requested background handoff.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: session continuation,context reset,ownership transfer,progress
    handoff,continuation record
  author: blacktower
  version: '2.0'
---

# relay-baton

Recalling work is read-only. Preserve source provenance, unfinished changes and next steps. Starting a background session is a separate explicit request and uses the current client contract.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **relay baton**: Use before a context reset, a handoff to another agent or session, or a long pause, to record progress, decisions, blockers and next steps. Read [the procedure](references/base-workflow.md).
- **context recall**: Recall recent working context from chat transcripts, live repo state and the shared record. Use for 'catch me up', 'where did I leave off', 'recall my work on X'. Read [the procedure](references/modes/context-recall/guide.md).
- **claude bg handoff**: Use for /claude-handoff in Claude Code: summarize this conversation and start a background claude --bg session to continue it. Other clients: relay-baton. Read [the procedure](references/modes/claude-bg-handoff/guide.md).
