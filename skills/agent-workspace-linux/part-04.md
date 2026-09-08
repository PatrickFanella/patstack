## Permission Model

- **Default**: no MCP ceiling is configured; the host/client owns approvals.
  Call `mcp_permissions` once before mutating to confirm `configured=false`.
- **Permission ceiling**: `--permissions PATH` or
  `AGENT_WORKSPACE_PERMISSIONS` caps network, mounts, and app allowlist for the
  life of that MCP process. It can only be broadened by changing the config and
  restarting/reconnecting the backend from the owning setup surface.
- **Live control**: `mcp_control_state` read-only/paused/active is a
  best-effort runtime control, not the authoritative security boundary.
- **Real-world actions**: checkout, purchases, account changes, and messages
  require explicit user approval. Keep drafting separate from final action.

Skip unless: you are about to start a workspace, open a profile, launch/run an
app, send input, or act on an external account/site.
