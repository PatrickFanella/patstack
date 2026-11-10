---
name: coordinate-parallel-agents
description: Coordinate authorized parallel agent work, candidate comparisons or a
  supported multi-phase agent workflow.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: parallel delegation,subagent coordination,file ownership,agent
    handoff,integration sequencing
  author: blacktower
  version: '2.0'
---

# coordinate-parallel-agents

Delegation requires the current task authorization. Respect client orchestration contracts, ownership and integration checks. OpenCode deepwork requires its actual Blacktower runtime; never invent agent types or providers.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **agent fanout plan**: Parallel subagent coordination (Claude Code, Codex, OpenCode, Blacktower): ownership, sequencing, handoffs and integration checks. Not when one agent can finish more cheaply. Read [the procedure](references/base-workflow.md).
- **worker swarm fanout**: Swarm fan-out: run N parallel subagents on separate slices or as a race, then return one aggregated report. Use for /swarm or 'swarm this'. Read [the procedure](references/modes/worker-swarm-fanout/guide.md).
- **candidate arena**: Use for /arena or arena this: run N parallel candidates on one non-trivial task, cross-judge them, pick a base and graft the best parts of the rest into it. Read [the procedure](references/modes/candidate-arena/guide.md).
- **opencode deepwork**: OpenCode deepwork: orchestrate a long, risky multi-phase coding task with Blacktower @oracle reviews, delegated phases and a progress file. Needs OpenCode with Blacktower agents. Read [the procedure](references/modes/opencode-deepwork/guide.md).

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
