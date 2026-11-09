---
name: skill-forge
description: Create or evaluate agent skills, install an explicitly requested unmanaged
  skill, or scaffold a Codex or Cursor plugin.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,skill,creator
  author: blacktower
  version: '2.0'
---

# skill-forge

Prefer a current system or plugin owner when available. Preserve source ownership: installed caches and Patstack-managed selections are not authoring targets. Select the correct client packaging contract before creating files.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **skill forge**: Create, evaluate or improve an Agent Skills SKILL.md: trigger descriptions, progressive disclosure, resources, packaging, trigger evals. Use for skill authoring. Read [the procedure](references/base-workflow.md).
- **codex skill fetch**: Install Codex skills into $CODEX_HOME/skills from openai/skills lists or a GitHub path. Use for an ad hoc Codex install. Read [the procedure](references/modes/codex-skill-fetch/guide.md).
- **codex plugin scaffold**: Codex plugin scaffolding: create .codex-plugin/plugin.json and folders, add personal marketplace entries, reinstall during local development. Read [the procedure](references/modes/codex-plugin-scaffold/guide.md).
- **cursor plugin forge**: Cursor plugin scaffold: create a new Cursor plugin with manifest, component folders and marketplace entry. Read [the procedure](references/modes/cursor-plugin-forge/guide.md).
