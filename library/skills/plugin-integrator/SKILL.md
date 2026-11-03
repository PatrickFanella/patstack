---
name: plugin-integrator
description: "Blacktower and OpenCode plugin integration changes: bootstrap, agent, tool and MCP registration, hooks, config schema and loader, managed skill wiring, OpenCode SDK plugin APIs."
metadata:
  blacktower-pack: engineering
  blacktower-kind: internal
  blacktower-tier: niche
  blacktower-capabilities: agent-ecosystem,plugin,integrator
---

# Plugin Integrator

Use this skill when the change crosses Blacktower composition boundaries. The
goal is to avoid “works in one file, breaks at startup” failures.

## Workflow

1. **Map the integration surface**
   - Read `codemap.md` and the relevant subsystem `codemap.md`.
   - Identify every boundary touched: config, agent definitions, tools, MCPs,
     hooks, CLI install, skills, schemas, docs.
   - Run `python3 scripts/list_plugin_touchpoints.py <paths...>` from this skill
     if you have a file list and want a quick boundary summary.

2. **Preserve plugin invariants**
   - Keep SDK session calls timeout-guarded.
   - Keep event handlers isolated; one hook must not block the pipeline.
   - Keep config/schema changes backward-compatible unless the user approved a
     breaking migration.
   - Keep docs and generated artifacts synchronized when behavior changes.

3. **Plan the edit before coding**
   - Use `templates/plugin-change-plan.md` for broad changes.
   - Read `references/integration-boundaries.md` when touching `src/index.ts`,
     `src/config/`, `src/agents/`, `src/tools/`, `src/hooks/`, or `src/mcp/`.

4. **Validate the complete path**
   - Run the most specific tests first.
   - Then run `bun run check:ci`, `bun run typecheck`, and relevant build/tests.
   - If config schema changed, regenerate and verify `blacktower.schema.json`.

## Do Not

- Do not add a tool without registering, documenting, and testing it.
- Do not add config fields without loader/default/schema/docs alignment.
- Do not replace user-facing names without compatibility aliases.
- Do not let plugin bootstrap depend on optional local files.
