---
name: continual-learning
description: "Use for continual learning: hand transcript mining and AGENTS.md updates to the agents-memory-updater subagent; stop if that subagent is not installed."
disable-model-invocation: true
---

# Continual Learning

Keep `AGENTS.md` current by delegating the memory update flow to one subagent.

## Trigger

Use when the user asks to mine prior chats, maintain `AGENTS.md`, or run the continual-learning loop.

## Workflow

1. Confirm the `agents-memory-updater` subagent exists in this client. If it does not, say so and stop; do not mine transcripts or edit `AGENTS.md` yourself.
2. Call `agents-memory-updater`.
3. Return the updater result.

## Guardrails

- Keep the parent skill orchestration-only.
- Do not mine transcripts or edit files in the parent flow.
- Do not bypass the subagent.
