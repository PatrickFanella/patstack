---
name: build-cli-tools
description: "Use when designing or building a command-line tool: argument parsing, subcommands, completions, prompts, exit codes, or agent-safe noninteractive use. Not for shell scripts; use bash-scripts."
---

# build-cli-tools

Design flags, stdout/stderr, exit codes, and noninteractive input as a contract. Preserve human interaction when requested; make it an optional fallback for automatable operations.

## Select a mode

- Use when building CLI tools, implementing argument parsing, or adding interactive prompts. Read [the procedure](references/modes/cli-developer/guide.md).
- Designs or reviews CLIs so coding agents can run them reliably: non-interactive flags, layered --help with examples, stdin/pipelines, fast actionable errors, idempotency, dry-run, and predic. Read [the procedure](references/modes/cli-for-agents/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
