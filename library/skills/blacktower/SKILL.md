---
name: blacktower
description: Configure and improve Blacktower for the current user. Use when users want to tune agents, models, prompts, custom agents, skills, MCPs, presets, or plugin behavior. Also use when recurring workflow friction suggests a safe config or prompt improvement.
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: blacktower configuration,agent tuning,model routing,skill catalog maintenance,plugin behavior
---

# blacktower

## Use this skill

Configure and improve Blacktower for the current user. Use when users want to tune agents, models, prompts, custom agents, skills, MCPs, presets, or plugin behavior. Also use when recurring workflow friction suggests a safe config or prompt improvement.

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
