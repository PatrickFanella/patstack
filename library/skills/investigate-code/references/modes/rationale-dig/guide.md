# rationale-dig procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# Why

Investigate the motivation and intent behind code: the constraints, edge cases, alternatives, and product, business, or operational forces that shaped it. Use this skill's `code-walkthrough` mode for runtime behavior and mechanics.

## Trigger and posture

Use for design rationale, tradeoffs, regressions, postmortems, historical archaeology, and data-backed thresholds. Establish evidence before narrative: code shows mechanics, not intent. Cite direct claims, label inference as inference, surface contradictions and gaps, and match confidence language to the evidence. Never construct a satisfying story from thin records.

The full confidence framework and mandatory phrasing are in [epistemics](references/epistemics.md).

## Core workflow

1. Identify the target and question. If the target is vague, make the best context-based interpretation, state it briefly, and proceed.
2. Build a code anchor: relevant file/line ranges, symbols, recent touching commits, PR numbers, and linked ticket IDs. Use git history and PR bodies/discussion for substantive commits (`tea` for Gitea repositories, `gh` for GitHub).
3. Discover available MCPs, map them to the seven evidence categories, and build a coverage map. Spawn one investigator for each available category concurrently; source control is always included.
4. Give each investigator the code anchor, original question, [investigator prompt](references/investigator-prompt.md), and its category playbook from [source playbooks](references/source-playbook.md). Include the incident/postmortem playbook for defensive code.
5. Give all findings (including null results and justified skips) plus the anchor and question to one synthesizer with [synthesizer prompt](references/synthesizer-prompt.md) and [epistemics](references/epistemics.md).
6. Present the synthesizer's confidence-weighted, cited result without strengthening its hedges. If the question precedes a change, append Preserve / Change / Avoid / Risk constraints.

## Guardrails

- Default to complete parallel coverage, not minimalism. A null search is evidence and must be reported.
- Do not skip a category because it seems unlikely. Skip only when no matching MCP exists or the source is provably irrelevant, and give the written justification in Sources Consulted.
- One investigator owns one evidence category; do not merge categories or chase cross-source leads.
- Investigators and synthesizer need MCP and tool access for searching and citation spot-checks; instruct them not to write. If the client has no subagent tool, run each category pass yourself in turn.
- Do not infer motivation from code shape, silently resolve contradictions, or omit unsearchable/empty sources.

## Required result shape

Keep separate sections for: **The Question**, **The Code in Question**, **What We Found (direct evidence)**, **What We Can Reasonably Infer**, **Competing Hypotheses** when warranted, **What We Don't Know**, and **Sources Consulted**. Every source line states what was searched and what was found, empty, or skipped with its reason. Full output conventions and examples are in [investigation details](references/investigation-details.md).

## Reference routing

- [Epistemics](references/epistemics.md): confidence tiers, citations, and phrasing discipline.
- [Investigation details](references/investigation-details.md): anchor commands, category roster, skip standard, investigator configuration, synthesis inputs, and output example.
- [Investigator prompt](references/investigator-prompt.md): base prompt and required investigator findings format.
- [Source playbooks](references/source-playbook.md): category-to-playbook index and incident-postmortem routing.
- `references/sources/*.md`: self-contained playbooks for the assigned source category.
- [Synthesizer prompt](references/synthesizer-prompt.md): final synthesis template and quality checks.
