# Writing and interface research integration

Authoring source verified: `/home/onnwee/Work/Tools/codex-skills`, using its `AGENTS.md` and `docs/OPERATING-MODEL.md`. The checkout was clean before this task. Curated source and installed entrypoints matched for the three changed personal skills. The optional `copywriting` skill was not active in `~/.agents/skills/`.

## Ownership decisions

| Owner | Change |
|---|---|
| `unslop` | Add conditional deeper copy review and distinguish stylistic clues from authorship evidence. |
| `frontend-design` | Ground composition in product tasks, preserve justified conventions, and verify relevant behavior beyond a screenshot. |
| `interface-originality-audit` | Add contextual review checks and distinguish observed defects, design concerns, and taste. |
| Optional `copywriting` | Preserve meaningful qualifications, substantiate numbers, choose structure from visitor needs, and align CTA promises with the journey. Its transition reference now treats phrase examples as optional and removes unsupported authorship/SEO claims. |

No new skill: the capabilities already have owners. Catalog membership, profile selection, and automatic invocation policies remain applicable. Research URLs, versions or retrieved snapshots, response hashes, and adaptation/license notes are recorded in `catalog/research-review-2026-10-02.json`. New reference prose is original synthesis; upstream skill procedures were not imported.

## Acceptance scenarios

These are manual scenario walk-throughs against the final instructions, not independent model-session trials or product/browser tests.

| Scenario | Expected decision | Review result |
|---|---|---|
| Rewrite “Our platform seamlessly revolutionizes collaboration” with supplied shared-inbox behavior | Describe assigning/replying to messages without inventing a time-saving statistic. | Covered by claim grounding, specificity, and the supported example. |
| Edit a qualified reliability statement | Retain conditions and uncertainty; remove only empty intensifiers. | Covered by both writing owners. |
| Accuse an author because a paragraph uses an em dash and contractions | Explain that these cues do not establish authorship; offer quality review within scope. | Covered by the entrypoint evidence boundary and research limits. |
| Refine an established purple/Inter brand | Preserve justified choices; improve hierarchy and task fit without changing the identity arbitrarily. | Covered by both interface owners. |
| Audit a course-access page dominated by personal-profile details | Identify the task conflict and recommend prioritizing course access. | Covered by priority checks and the bounded NN/G example. |
| Assess a screenshot containing an export button | Review visible composition; do not claim export works or that failure states are absent. | Covered by screenshot/runtime evidence limits. |
| Rewrite a CTA for a paid registration flow | Do not introduce a free-trial promise; choose a truthful next-action label. | Covered by the action contract and copywriting CTA rules. |
| Send an ordinary short status reply | Apply short unslop pass without loading the deeper research reference or launching an originality audit. | Covered by conditional loading and existing skill boundaries. |

## Deployment boundary

The bounded installer preview stopped with `Externally owned skill changed: /home/onnwee/.codex/skills/.system`. The installer checks that protected package-owned tree even when selecting only personal skills. No baseline was rewritten, guard bypassed, system skill changed, or installed skill overwritten. Resolving package-owner drift requires a separate reviewed ownership reconciliation before guarded deployment can proceed.

Source validation passed with zero errors, 65 personal entrypoints, and all 139 original capability mappings intact. All 16 repository unit tests passed; whitespace checks passed. The optional copywriting entrypoint and transition reference were reviewed separately because the collection validator does not scan the optional library. No optional profile activation or remote/fleet publication is part of this update.

Read-only inspection of the protected drift found two changed entries: the package marker and `plugin-creator` directory. This observation does not authorize changing their baseline or owner.
