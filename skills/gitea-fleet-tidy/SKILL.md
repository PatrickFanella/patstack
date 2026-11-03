---
name: gitea-fleet-tidy
description: "Use when auditing or normalizing Gitea/Forgejo repositories in bulk: settings, labels, issues, wiki, branch protection, default branches, workflows, releases. Not for code changes inside one repo."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: git-github,gitea,repo,overhaul
---

# gitea-fleet-tidy

## Use this skill

End-to-end Gitea/Forgejo repository overhaul workflow for self-hosted repos. Use when asked to inventory, modernize, normalize, audit, or aggressively improve Gitea repos by creating manifests/reports, normalizing labels/issues/wiki pages, enabling repo units, adding soft branch protections, migrating default branches, planning workflows/releases/packages, and keeping repo settings sane.



## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
- `templates/` — reusable output skeletons.
