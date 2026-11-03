---
name: skill-creator
description: "Create, evaluate or improve an Agent Skills SKILL.md: trigger descriptions, progressive disclosure, resources, packaging, trigger evals. Use for skill authoring. Not for ordinary prompts or project instructions."
compatibility: Requires Python 3 or Bun only when the selected validation or scaffolding script is used.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,skill,creator
  author: blacktower
  version: '2.0'
---

# Skill Creator

Create a skill only when reusable procedural knowledge materially improves an
agent's behavior beyond the base model, project instructions, a command, or a
tool. This canonical workflow includes the former `prompt-craft` responsibility
for description quality and progressive disclosure.

## Workflow

1. Define the target behavior, likely trigger phrases, near-miss prompts, and a
   no-skill baseline. Reject the skill abstraction when a command, tool, or
   reference document is a better fit.
2. Choose a unique lowercase hyphenated ID and write a concise description that
   says what the skill does, when to use it, and important negative boundaries.
3. Keep `SKILL.md` focused on activation and procedure. Put conditional detail
   in `references/`, deterministic work in `scripts/`, reusable inputs in
   `assets/`, and output skeletons in `templates/`.
4. Declare runtime, network, credential, and host assumptions in
   `compatibility`. Keep Blacktower pack, kind, tier, and capabilities as string
   values under `metadata`.
5. Validate YAML, links, resource routing, portability, and the hard activation
   budget. Run scripts directly and inspect their outputs before documenting
   them as reliable.
6. Evaluate triggering with positive and near-miss negative prompts. Compare at
   least two isolated with-skill results against the baseline for procedural or
   high-risk skills; record assertions, timing, and token usage.
7. Rewrite when trigger error exceeds 20 percent, merge repeatedly overlapping
   skills, and remove generic skills that show no material quality gain.

## Quality Bar

- Standard `SKILL.md` frontmatter is authoritative.
- Prefer fewer than 2,000 activation tokens; never exceed 5,000.
- Every resource directory is routed from the activation file.
- Portable packs contain no user-specific absolute paths or hidden host state.
- Examples and scripts support the stated workflow instead of becoming an
  unrelated knowledge dump.

## Resources

- `references/full-guide.md` — detailed creation and packaging guidance.
- `references/workflows.md` — reusable authoring workflows.
- `references/output-patterns.md` — output and review patterns.
- `references/curated/` — legacy source material; consult only for a relevant
  edge case.
- `scripts/` — scaffold, package, validate, and analysis helpers; inspect usage
  and side effects before running.
- `templates/` — reusable skill and output skeletons.
- `assets/` and `examples/` — optional source material and evaluation examples.
