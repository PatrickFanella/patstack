---
name: eval-bench
description: "Use when measuring LLM or prompt behavior: eval datasets, baselines, task metrics, LLM-as-judge rubrics, regression comparisons. Not for retrieval quality; use retrieval-pipeline."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: agent-ecosystem,llm,evaluation
---

# eval-bench

Design and run LLM evaluation workflows. Use references for metrics, judge design, datasets, and iteration loops.

## Workflow

1. Keep the main context short: read only the relevant reference file for the exact subtask.
2. Prefer existing scripts/templates/assets in this skill before writing ad hoc code.
3. Resolve repository facts and available tooling first. Ask only for missing information or authorization required for the requested action; continue independent authorized work.

## Resources

- `references/full-guide.md` — detailed guidance.
