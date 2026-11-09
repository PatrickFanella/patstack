## Example Trajectory

Task: "QA the settings dialog of myapp."

1. `mcp_agent_context` and `mcp_task_plan` for app-QA.
2. `mcp_permissions` to confirm the active boundary.
3. `workspace_start` with `ack_hidden_workspace=true` and purpose
   `"QA myapp settings"`.
4. `workspace_launch_app` with the app command.
5. `workspace_observe` to find the window.
6. `workspace_click` / `workspace_type_text` to exercise Settings.
7. `workspace_screenshot` and `workspace_read_app_log` for evidence.
8. `workspace_stop`.
