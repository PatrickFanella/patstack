---
name: use-my-browser
description: Use when work depends on the user's live browser session or visible rendered state rather than static fetches, especially for browser debugging contexts or DevTools-selected elements or requests, logged-in dashboards or CMS flows, localhost apps, forms, uploads, downloads, media inspection, DOM or iframe inspection, Shadow DOM, or browser failures that look like soft 404s, auth walls, anti-bot checks, or rate limits.
compatibility: Requires an available browser-control integration with access to the user's existing browser session.
metadata:
  blacktower-pack: integrations
  blacktower-kind: tool-wrapper
  blacktower-tier: standard
  blacktower-capabilities: tooling-integrations,use,my,browser
---

# use-my-browser

## Use this skill

Use when work depends on the user's live browser session or visible rendered state rather than static fetches, especially for browser debugging contexts or DevTools-selected elements or requests, logged-in dashboards or CMS flows, localhost apps, forms, uploads, downloads, media inspection, DOM or iframe inspection, Shadow DOM, or browser failures that look like soft 404s, auth walls, anti-bot checks, or rate limits.

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
