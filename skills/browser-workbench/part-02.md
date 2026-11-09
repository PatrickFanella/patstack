## Setup and installation

### Use the dedicated Codex for Linux feature page for setup
Codex for Linux owns Agent Workspace setup through the **Agent Workspaces** page:
binary path, page-authored permission rules, permission file mutation,
Reconnect/Smoke test, profile creation, workspace start/stop, and viewer launch.
Do not send users to generic MCP settings, general configuration pages, or
`~/.codex/config.toml` for normal Codex for Linux setup.

Skip unless: the host is Codex for Linux and the task is setup, permission
changes, reconnect/restart, or the workspace tools are unavailable.

### Keep tools progressive
The bundled installer is skill-first. `./install.sh` installs this skill under
`~/.codex/skills` by default and leaves generic Codex MCP config untouched
unless the user explicitly chooses `--codex-configure` or `--permissions`.
For migration only, `./install.sh --clean-codex-config` removes stale generic
Codex MCP entries left by older installs; restart or reconnect Codex afterward.

Skip unless: the user asks how to install/register the backend or why the tool
family should not be loaded at startup.
