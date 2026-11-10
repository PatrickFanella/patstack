---
name: map-codebase
description: Orient in a repository or create and incrementally refresh its codemaps
  when requested.
metadata:
  blacktower-pack: core
  blacktower-kind: tool-wrapper
  blacktower-tier: core
  blacktower-capabilities: repository map,codebase orientation,module ownership,architecture
    navigation
---

# map-codebase

Orientation is read-only. Write codemaps or register them in AGENTS.md only when requested; use one state engine per map.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **repo atlas**: Use when orienting in an unfamiliar repository, or creating or incrementally updating codemap.md files with the bundled inventory script. Read [the procedure](references/base-workflow.md).
- **codemap atlas**: Codemap atlas: generate or incrementally refresh hierarchical codemap.md files with change tracking for an unfamiliar repository, only when the user asks for one. Read [the procedure](references/modes/codemap-atlas/guide.md).

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
