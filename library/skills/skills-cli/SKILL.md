---
name: skills-cli
description: "Use the `skills` CLI (bunx/npx skills, skills.sh, skills-lock.json) to find, install, update, remove, back up or sync Agent Skills. Use for 'find a skill for X'. Not for patstack profile deployment."
compatibility: Requires Bun or Node.js with npx; discovery and installation require network access.
metadata:
  blacktower-pack: engineering
  blacktower-kind: tool-wrapper
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,skills,cli
---

# skills-cli

## Use this skill

Use when users ask to discover, install, list, check, update, remove, back up, restore, sync, or initialize Agent Skills, mention `bunx skills`, `npx skills`, `skills.sh`, or `skills-lock.json`, ask "find a skill for X", or want help extending agent capabilities with installable skills.

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

- Prefer the project's existing stack and conventions over generic examples.
- State required credentials, network access, CLIs, and destructive side effects
  before relying on them.
- Use current authoritative documentation when provider or framework behavior is
  version-sensitive.
- Report concrete evidence, remaining risks, and any unverified assumptions.

## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
