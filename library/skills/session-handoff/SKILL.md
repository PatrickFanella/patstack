---
name: session-handoff
description: "Write a continuation record (progress, decisions, blockers, next steps) when work moves to another session, agent or host. Use before a context reset, ownership transfer or long pause. Not for final summaries."
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: session continuation,context reset,ownership transfer,progress handoff,continuation record
  author: blacktower
  version: '2.0'
---

# Session Handoff

Create a compact, evidence-backed continuation record. Use the repository's
existing handoff convention; otherwise prefer `.blacktower/handoff.md`, unless
the user requests another location. When the next session runs on another host
or client (T3 Code across hosts), commit or push the handoff, or give its
absolute path and host, so the next agent can reach it.

## Workflow

1. Re-read the goal, current plan, `git status`, recent commits, and relevant
   verification output.
2. Distinguish finished work from work merely attempted or discussed.
3. Record decisions and their reasons, especially choices not evident in code.
4. Name blockers, open questions, risky assumptions, and unrelated dirty files.
5. Give the next session the smallest safe continuation sequence with exact
   paths and commands.
6. On resume, verify the handoff against current repository state before acting.

## Handoff Format

```markdown
# Handoff: <task>

Date:
Branch and worktree:
Status: in-progress | blocked | ready-for-review

## Goal and scope
## Completed and verified
## Remaining work
## Decisions and rationale
## Blockers, risks, and open questions
## Key files and unrelated changes
## Exact continuation steps
```

Keep the handoff scannable. Include file paths, symbols, command outcomes, and
test status; omit conversational history that does not affect continuation.

For longer-running context systems, load the relevant material in
`references/context-management/` and the optional templates in
`templates/context-network/`. Do not create a context network for a short,
single-session task.

## Guardrails

- Never claim tests passed when they were not run or did not complete.
- Preserve user-owned dirty changes and identify them explicitly.
- Do not include secrets, personal data, tokens, or transient credentials.
- A handoff is not a substitute for committing finished work when the user has
  requested a commit.
