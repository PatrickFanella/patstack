---
name: security-threat-model
description: 'Requested repository threat model: assets, trust boundaries, attacker paths, and prioritized mitigations.'
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
4. Resolve repository facts and available tooling first. Ask only for missing information or authorization required for the requested action; continue independent authorized work.

## Resources

- `references/full-guide.md` — detailed guidance.

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/attack-tree-construction.md` — Attack Tree Construction guidance.
- `references/curated/security-requirement-extraction.md` — Security Requirement Extraction guidance.
- `references/curated/stride-analysis-patterns.md` — Stride Analysis Patterns guidance.
- `references/curated/threat-mitigation-mapping.md` — Threat Mitigation Mapping guidance.
