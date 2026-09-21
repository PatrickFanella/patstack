---
name: gitea-repo-overhaul
description: End-to-end Gitea/Forgejo repository overhaul workflow for self-hosted repos. Use when asked to inventory, modernize, normalize, audit, or aggressively improve Gitea repos by creating manifests/reports, normalizing labels/issues/wiki pages, enabling repo units, adding soft branch protections, migrating default branches, planning workflows/releases/packages, and keeping repo settings sane.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: git-github,gitea,repo,overhaul
---

# gitea-repo-overhaul

## Use this skill

End-to-end Gitea/Forgejo repository overhaul workflow for self-hosted repos. Use when asked to inventory, modernize, normalize, audit, or aggressively improve Gitea repos by creating manifests/reports, normalizing labels/issues/wiki pages, enabling repo units, adding soft branch protections, migrating default branches, planning workflows/releases/packages, and keeping repo settings sane.

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
