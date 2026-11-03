---
name: book-marketing
description: "Book marketing copy: diagnose weak blurbs, or write retailer descriptions, taglines and query pitches. Not for general product marketing."
license: MIT
metadata:
  blacktower-pack: growth
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: growth-marketing,book,marketing
  author: jwynia
  version: "1.0"
  type: diagnostic
  mode: diagnostic+generative
  domain: publishing
---

# book-marketing

## Use this skill

Diagnose book marketing copy problems and generate platform-optimized blurbs, descriptions, taglines, and query pitches. Use when marketing copy feels weak, when descriptions aren't converting, or when starting marketing from scratch.

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
- `templates/` — reusable output skeletons.
