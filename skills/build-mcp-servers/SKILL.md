---
name: build-mcp-servers
description: "Use when building or extending an MCP server in Go, TypeScript or Python: tool contracts, transports, errors, evaluation harnesses. Not for client registration; use fix-mcp-connections."
license: Complete terms in LICENSE.txt
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,mcp,builder
---

# build-mcp-servers

## Use this skill

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, in Go with the official SDK where it fits, otherwise TypeScript or Python.



## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
- `scripts/` — deterministic helpers; inspect --help and side effects before use.

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
