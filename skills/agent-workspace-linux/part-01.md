# agent-workspace-linux

Drive an isolated, agent-owned Linux desktop and workspace-owned browser through
the `agent-workspace-linux` MCP server. The workspace runs apps, browser
automation, screenshots, clipboard, and input inside its own hidden display,
never the user's real desktop, focus, or host Chrome.

This skill is the lightweight entry point. The MCP exposes many tools; do not
load, list, or paste them all up front. Route by phase and ask the host to load
only the tool schemas needed for the next action.
