---
name: sandbox-desktop
description: "Use when sandbox-desktop MCP tools are available and a task needs an isolated hidden Linux desktop or workspace browser: GUI app QA, sandboxed browsing, stale workspace cleanup. Not for host desktop control."
---

# sandbox-desktop

Drive an isolated, agent-owned Linux desktop and workspace-owned browser through the `sandbox-desktop` MCP server. Apps, browser automation, screenshots, clipboard and input run inside the workspace's hidden display, never on the user's real desktop, focus or host Chrome. For pure code, shell or file edits, do not start a workspace.

If the `sandbox-desktop` MCP tools are not available in the active client, say so and stop; do not fall back to host desktop or host browser control. Setup notes in the procedures describe the Codex for Linux app; in Claude Code or OpenCode, registration goes through that client's own MCP configuration.

## Rules for every run

- Target only the hidden workspace. For the user's real Linux desktop, real Chrome profile, existing tabs, or host focus, mouse or keyboard, use the appropriate host tool instead. Never send input to or screenshot the user's real desktop, and never attach to host Chrome, Playwright or Computer Use as a shortcut.
- Load tool schemas by phase, only for the next action. Never list or paste the whole MCP tool family into context.
- Call `mcp_permissions` once before mutating. With no ceiling configured (`configured=false`) the host or client owns approvals. A ceiling from `--permissions PATH` or `AGENT_WORKSPACE_PERMISSIONS` caps network, mounts and the app allowlist for that MCP process's life; only a config change plus a backend restart or reconnect from the owning setup surface broadens it. `mcp_control_state` (read-only, paused, active) is best-effort runtime control, not the security boundary.
- Checkout, purchases, account changes and sent messages require explicit user approval. Keep drafting separate from the final action.
- Start a workspace only with `ack_hidden_workspace=true` and a clear `purpose`. Stop it when the task ends.

## Workflow

1. Orient: call `mcp_agent_context` or `mcp_session_brief`, then `mcp_task_plan` for the app-QA, browser, observe or cleanup intent.
2. Check permissions with `mcp_permissions`.
3. Start with `workspace_start`, or `workspace_open_profile` for a saved profile.
4. Observe with `workspace_observe` or focused screenshot, window, log or event tools before sending input.
5. Act only inside the workspace: launch apps, run commands, click, type, paste, press keys.
6. Stop with `workspace_stop`; use `workspace_cleanup_stale` for orphaned runtimes.

Take each step only when its precondition is visible in the previous tool result: workspace id, app id, target window, browser target, or explicit user approval.

[The task guide](guide.md) holds the per-phase tool table, the browser procedure, setup notes and a worked example. Read only the entry whose trigger matches.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.
