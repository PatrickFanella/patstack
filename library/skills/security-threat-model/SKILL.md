---
name: security-threat-model
description: "Threat-model a repository or path: assets, trust boundaries, attacker capabilities, abuse paths, mitigations, written as Markdown. Use only on an explicit threat-model request. Not for code review."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: security,threat,model
---

# security-threat-model

Create repo-grounded threat models. Use STRIDE, attack tree, requirements, and mitigation references only as needed.

## Workflow

1. Use this skill only when the request matches the frontmatter description.
2. Keep the main context short: read only the relevant reference file for the exact subtask.
3. Prefer existing scripts/templates/assets in this skill before writing ad hoc code.
4. Stop and ask when required credentials, CLIs, project context, or user confirmation are missing.

## Resources

- `references/full-guide.md` — detailed guidance.

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/attack-tree-construction.md` — Attack Tree Construction guidance.
- `references/curated/security-requirement-extraction.md` — Security Requirement Extraction guidance.
- `references/curated/stride-analysis-patterns.md` — Stride Analysis Patterns guidance.
- `references/curated/threat-mitigation-mapping.md` — Threat Mitigation Mapping guidance.
