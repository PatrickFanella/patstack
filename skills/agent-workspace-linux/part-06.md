## Safe Workflow

1. Orient: call `mcp_agent_context` or `mcp_session_brief`, then use
   `mcp_task_plan` for app-QA, browser, observe, or cleanup intent.
2. Check permissions: call `mcp_permissions` before mutating.
3. Start: use `workspace_start` with `ack_hidden_workspace=true` and a clear
   `purpose`, or `workspace_open_profile` for a saved profile.
4. Observe: use `workspace_observe` or focused screenshot/window/log/event
   tools before sending input.
5. Act: launch apps, run commands, click/type/paste/key only inside the
   workspace.
6. Stop: use `workspace_stop` when finished; use `workspace_cleanup_stale` for
   orphaned runtimes.

Skip unless: each step's precondition is visible in the previous tool result
(workspace id, app id, target window, browser target, or explicit user approval).
