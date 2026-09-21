# Skill review acceptance cases

Method: manual procedure walkthrough against concrete positive and near-miss cases. These are review fixtures, not independently sampled model evaluations.

| Request | Expected behavior | Walkthrough |
|---|---|---|
| Grill me about splitting public docs from private operations | Inspect existing policy; ask unresolved decisions in dependency order; record accepted boundaries | Grilling procedure starts with facts, then a bounded round, and reuses canonical decisions |
| Rename this known variable | Implement directly; no design interview | Ordinary interview trigger excludes already clear repository facts |
| Unslop: “Our groundbreaking cache significantly improves speed; benchmark pending” | Remove puffery; retain benchmark uncertainty; invent no speedup | “The cache is implemented. Its performance has not been benchmarked.” |
| Unslop a paragraph containing `a--`, quoted punctuation, and a measured p95 | Preserve code, quotation, identifier, and measurement | Explicit preservation takes precedence over upstream punctuation heuristics |
| What could this API field rename break? | Trace serialized clients and prove the key compatibility fact with real code | Blast-radius mode includes wire consumers and requires evidence tier labels |
| Show me your work on a long migration | Record observable decisions and actual evidence, including failed checks | Decision-trail mode records checkpoints and corrections; excludes private deliberation |
| Fix one typo | No TSV ledger, interview, or parallel reviewer | Conditional triggers scope each procedure |

Fresh discovery and deterministic profile/installer tests are separate evidence. A repeated behavioral evaluation should run these prompts in isolated sessions before broadening the active catalog; no model-quality score is claimed here.
