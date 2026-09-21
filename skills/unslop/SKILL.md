---
name: unslop
description: Edit prose to remove AI filler, vague claims, inflated language, and repetitive framing while preserving meaning, evidence, and the author's voice. Use for unslop, natural-language rewrites, and polishing documentation or agent responses.
---

# Unslop

Read the supplied text and its intended audience. Preserve facts, uncertainty, citations, technical identifiers, quoted material, and the author's meaning.

1. Replace vague praise and abstract claims with the specific action, mechanism, or measured result. Delete empty sentences.
2. Use plain words, direct statements, and varied sentence lengths. Remove canned openings, repeated conclusions, forced contrasts, and decorative emphasis.
3. Keep the author's tone. Add personality only where supported by the source; never invent experience, opinions, evidence, or measurements.
4. Read the revision once as its audience. Remove remaining awkward phrasing and check that no claim became stronger or lost a qualification.

For a longer editing pass, consult the [pattern examples](references/upstream.md). Treat its punctuation preferences as editing heuristics: preserve syntax in code, quotations, names, and required formats. Its universal trigger is upstream context, not a requirement to load this reference on every turn.

Return the requested rewrite. Explain substantive changes when useful; omit a change log for a small rewrite. Prose editing does not authorize changing code behavior or publishing the text.
