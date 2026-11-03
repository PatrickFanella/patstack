---
name: mcp-server-forge
description: "Use when building or extending an MCP server (Go preferred, TypeScript fallback): tool contracts, transports, errors, evaluation harnesses. Not for client registration; use mcp-wire-tracer."
license: Complete terms in LICENSE.txt
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,mcp,builder
---

# mcp-server-forge

## Use this skill

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, preferably in Go using the MCP API, with TypeScript as the primary fallback.



## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
- `scripts/` — deterministic helpers; inspect --help and side effects before use.
