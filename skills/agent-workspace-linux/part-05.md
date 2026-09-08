## Phase Router

Always orient before mutating.

| Phase | Load only these tools |
| --- | --- |
| Orient | `mcp_agent_context`, `mcp_session_brief`, `mcp_task_plan`, `mcp_permissions`, `mcp_action_catalog`, `workspace_doctor`, `workspace_list`, `workspace_status` |
| Profiles | `profile_list`, `profile_get`, `profile_template`, `profile_put`, `profile_check` |
| Start | `workspace_start`, `workspace_open_profile` |
| Observe | `workspace_observe`, `workspace_screenshot`, `workspace_list_windows`, `workspace_active_window`, `workspace_read_app_log`, `workspace_events` |
| Act | `workspace_launch_app`, `workspace_run_app`, `workspace_click`, `workspace_type_text`, `workspace_key`, `workspace_paste_text`, `workspace_focus_window`, `workspace_close_window` |
| Browser | `workspace_open_browser`, `workspace_browser_targets`, `workspace_browser_snapshot`, `workspace_browser_navigate`, `workspace_browser_search_results`, `workspace_browser_click` |
| Viewer/control | `mcp_control_state`, `mcp_control_update`, `workspace_open_viewer`, `workspace_list_viewers`, `workspace_close_viewer` |
| Teardown | `workspace_stop`, `workspace_kill_app`, `workspace_cleanup_stale` |

Skip unless: the current phase needs one of the listed capabilities. Do not load
schemas for later phases until the plan reaches them.
