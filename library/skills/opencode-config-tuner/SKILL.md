---
name: opencode-config-tuner
description: Configure OpenCode agents, skills, plugins, MCP, permissions or its supported
  scheduler.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: opencode configuration,agent configuration,mcp configuration,permission
    rules,plugin configuration
---

# opencode-config-tuner

Use the scheduling mode only with the actual OpenCode scheduler plugin. It is not a T3 or Claude scheduler. Preserve existing permissions, authentication and unrelated configuration.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **opencode config tuner**: OpenCode configuration: edit opencode.json/jsonc, .opencode or ~/.config/opencode agents, skills, plugins, MCP servers or permissions. Read [the procedure](references/base-workflow.md).
- **opencode cron**: Schedule OpenCode tasks: one-off schedule_task runs, recurring cron task files, status and history, unattended permissions. Use only with the OpenCode scheduler plugin. Read [the procedure](references/modes/opencode-cron/guide.md).
