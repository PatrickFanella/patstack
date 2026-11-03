---
name: sp-mcp-doctor
description: "Super Productivity MCP failures: startup, handshake, tool catalog drift, client config or plugin bridge reliability. Not for task planning; use sp-day-planner."
license: MIT
metadata:
  blacktower-pack: personal
  blacktower-kind: tool-wrapper
  blacktower-tier: personal
  blacktower-capabilities: tooling-integrations,super,productivity,mcp
  author: blacktower
  version: "1.0"
  type: diagnostic
  mode: diagnostic+application
  maturity_score: '22'
---

# sp-mcp-doctor

## Use this skill

Diagnose and resolve Super Productivity MCP health, development, startup,
handshake, catalog, client config, and bridge reliability issues. Use for
MCP/runtime failures; use sp-day-planner for task hygiene,
recurring daily frameworks, and one-off scheduling.

## Workflow

1. Confirm the request matches this skill's stated intent; do not activate it
   for a keyword-only near miss.
2. Inspect the user's inputs, repository conventions, and available tools before
   selecting an approach.
3. Load only the relevant section of the detailed guide when the task needs
   domain-specific patterns or edge cases.
4. Perform the smallest complete unit of work and preserve existing behavior or
   user data unless change is explicitly requested.
5. Validate the result with the project's own checks plus any skill-specific
   verification described in the detailed guide.

## Constraints

- Requires the user's local Super Productivity MCP server, client
  configuration, and host workspace access.
- Prefer the project's existing stack and conventions over generic examples.
- State required credentials, network access, CLIs, and destructive side effects
  before relying on them.
- Use current authoritative documentation when provider or framework behavior is
  version-sensitive.
- Report concrete evidence, remaining risks, and any unverified assumptions.

## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
- `scripts/` — deterministic helpers; inspect --help and side effects before use.
