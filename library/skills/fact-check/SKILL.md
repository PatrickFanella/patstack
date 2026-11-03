---
name: fact-check
description: "Fact check: verify claims in already generated output against sources, as a separate pass after writing. Not for generating the content."
license: MIT
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: fact verification,source checking,citation audit,hallucination detection
  author: jwynia
  version: "1.0"
  domain: research
  cluster: methodology
  type: diagnostic
  mode: evaluative
---

# fact-check

## Use this skill

Verify claims in generated output against sources. Use as a separate pass AFTER content generation to catch hallucinations. Critical constraint - cannot be reliably combined with generation in a single pass.

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
