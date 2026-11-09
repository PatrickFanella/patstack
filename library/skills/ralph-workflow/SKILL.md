---
name: ralph-workflow
description: Explain, start or stop a Ralph iteration loop when explicitly requested
  and supported by the current client.
---

# ralph-workflow

Confirm the client and installed stop hook before starting or stopping a loop. Explanation has no side effects. Codex and OpenCode do not gain a stop hook from a state file; do not run an unbounded external loop.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **ralph loop explainer**: Use when the user asks what a Ralph loop is, how it works, or how to start or cancel one. Read [the procedure](references/base-workflow.md).
- **ralph loop start**: Use when the user asks to start a Ralph loop: the same prompt re-fed each turn until a completion promise or iteration cap. Needs a client stop hook (Cursor or the Claude Code plugin). Read [the procedure](references/modes/ralph-loop-start/guide.md).
- **ralph loop stop**: Ralph loop cancel: stop, cancel or abort an active Ralph loop started by ralph-loop-start. Read [the procedure](references/modes/ralph-loop-stop/guide.md).
