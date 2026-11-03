---
name: interface-originality-audit
description: Use when asked to audit a UI for generic or AI-looking design, unsupported product claims, or missing states. Reports findings only; use frontend-design to implement fixes.
metadata:
  blacktower-pack: creative
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: design-review,visual-originality,product-credibility
---

# Interface originality audit

Find places where defaults have replaced design decisions. Review the interface in its actual context, then recommend the smallest changes that make it specific to the product.

Do not treat familiar components, colors, fonts, or effects as universally forbidden. A pattern is a problem when it lacks a product, brand, information, or interaction reason. Preserve established brand rules, accessibility, platform conventions, and user-tested behavior.

## Gather evidence

1. Read the existing brand and design-system guidance.
2. Identify the product, audience, task, and page goal.
3. Inspect the running interface or representative screenshots when available.
4. Distinguish deliberate repetition from an unexamined template default.

If the evidence is incomplete, state what was unavailable. Screenshots support visual findings; use observed interactions for behavioral claims. Review quality and specificity without asserting AI authorship from appearance.

For a requested AI-look/generic-design review, or when judging an apparent cluster of defaults, read [the research and task checks](references/research-informed-interface-review.md). It distinguishes measured patterns, practitioner observations, and review heuristics.

## Audit lenses

### Borrowed aesthetic

Look for clusters of fashionable defaults that could belong to any product: decorative gradients or glowing orbs, neon or pastel palettes, purple-on-black themes, glass effects, uniformly soft corners, generic shadows, sparkle motifs, default icon sets, and fashionable typefaces used without a typographic system.

Ask what each choice communicates about this product. A justified choice can stay. Replace an unjustified cluster with a coherent direction grounded in the brand, content, and audience.

### Templated composition

Check whether the information architecture has been forced into familiar demo layouts: arbitrary three-card or three-tier groups, bento grids without meaningful hierarchy, colored accent stripes, fake terminal windows, repeated checkmark bullets, decorative arrows, and hover or motion effects that do not explain state.

Recommend the number, grouping, and interaction pattern the content actually needs.

### Product specificity and trust

Prefer inspectable evidence over atmosphere: real screens, useful demos, representative data, relevant imagery, attributable customer proof, and concrete capabilities. Flag unsupported testimonials or metrics and claims that could be pasted onto a competitor's page unchanged. Missing provenance means unverified; appearance alone does not establish fabrication.

### Production completeness

Check the states polished mockups often omit: loading or skeleton states, empty and error states, focus and keyboard behavior, responsive layouts, reduced motion, and legible contrast. For a public product, also note absent trust essentials such as applicable terms and privacy links.

### System coherence

Verify that typography has defined roles, color carries consistent meaning, spacing follows a rhythm, component shapes have a rationale, and motion signals hierarchy, feedback, or state. Variety without a system is not originality.

## Report findings

For each finding, include:

- the observed evidence and location;
- why the choice appears context-free or incomplete;
- the likely effect on comprehension, trust, accessibility, or distinctiveness;
- a concrete replacement that fits the existing system;
- severity: blocker, important, or opportunity.

Separate evidence-based defects from subjective taste. End with the two or three changes with the highest product impact, even when the audit found many minor clichés.

## Related skills

- Use `frontend-design` to design and implement the recommended interface changes.
- Use `unslop` to remove generic AI phrasing and unsupported promotional language from interface copy.
