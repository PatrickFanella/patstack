---
name: threat-modeling
description: "Use only when asked to threat-model a repository or system: assets, trust boundaries, STRIDE, attack trees, prioritized mitigations. Not for line-level code review."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: security,threat,model
---

# threat-modeling

Create repo-grounded threat models. Use STRIDE, attack tree, requirements, and mitigation references only as needed.

## Workflow

1. Keep the main context short: read only the relevant reference file for the exact subtask.
2. Prefer existing scripts/templates/assets in this skill before writing ad hoc code.
3. Resolve repository facts and available tooling first. Ask only for missing information or authorization required for the requested action; continue independent authorized work.

## Resources

- `references/full-guide.md` — detailed guidance.

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/attack-tree-construction.md` — Attack Tree Construction guidance.
- `references/curated/security-requirement-extraction.md` — Security Requirement Extraction guidance.
- `references/curated/stride-analysis-patterns.md` — Stride Analysis Patterns guidance.
- `references/curated/threat-mitigation-mapping.md` — Threat Mitigation Mapping guidance.

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
