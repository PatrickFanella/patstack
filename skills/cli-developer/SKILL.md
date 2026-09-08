---
name: cli-developer
description: 'CLI design and implementation: flags, subcommands, completions, interactive fallback, and automation contracts.'
---

# cli-developer

Design flags, stdout/stderr, exit codes, and noninteractive input as a contract. Preserve human interaction when requested; make it an optional fallback for automatable operations.

## Select a mode

- Use when building CLI tools, implementing argument parsing, or adding interactive prompts. Read [the procedure](references/modes/cli-developer/guide.md).
- Designs or reviews CLIs so coding agents can run them reliably: non-interactive flags, layered --help with examples, stdin/pipelines, fast actionable errors, idempotency, dry-run, and predic. Read [the procedure](references/modes/cli-for-agents/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
