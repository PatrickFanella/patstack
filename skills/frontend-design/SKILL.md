---
name: frontend-design
description: Implement or refine web interface visuals, responsive layouts, and interaction states within the product design.
license: Complete terms in LICENSE.txt
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: frontend-ui,frontend,design
---

# Frontend Design

Implement UI with clear priorities and coherent styling. Use for code-level visual work; use `react-pro` for React architecture, state, or performance.

## Defaults

- Target stack: TypeScript, React/Next.js, Tailwind, CSS, browser testing.
- Treat familiar fonts, colors, cards, and effects as choices to justify against the product, not forbidden signs of AI authorship. Preserve established branding and usable conventions.
- Choose a coherent direction from the audience, content, task, and existing system; novelty alone is not a design goal.
- Match complexity to the aesthetic: maximalist needs rich detail; minimalism needs precision.
- Prefer real implementation over mockups: responsive, accessible, keyboard-safe, and testable.

## Workflow

1. Read available product and design context: primary task, audience language, supported capabilities, representative data, constraints, and existing design rules. Resolve missing information only when it changes the implementation.
2. Explain how the hierarchy and visual direction serve the task. Choose sections and groupings from the content; do not impose a hero, three-card grid, bento layout, or generic KPI dashboard by default.
3. Implement layout, typography, color, spacing, motion, and responsive states.
4. Check accessibility basics: contrast, labels, focus, keyboard, semantics.
5. Inspect the rendered interface and exercise the main task when browser tools are available. Include relevant empty, loading, error, permission, long-content, and narrow-screen conditions. Report unavailable checks; a screenshot does not prove working interactions.
6. If more design data is needed, consult merged `tool-ui-ux-pro-max` references/scripts.

## Review Checklist

- [ ] UI has a clear point of view.
- [ ] Typography, spacing, color, and motion are coherent.
- [ ] Responsive states are handled.
- [ ] Components and visual emphasis have a product or interaction reason.
- [ ] Labels, claims, and resulting behavior agree; sample data and unverified proof are identified.
- [ ] Accessibility basics pass.
- [ ] Visual QA findings include source-file fixes, not just comments.

For a requested originality review, use `interface-originality-audit` and its research reference. Use `unslop` for generic interface copy. Separate visual taste, observed usability defects, and verified behavior; keep implementation details out of product flows unless users need them to decide.

## Resources

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/design-system-patterns.md` — Design System Patterns guidance.
- `references/curated/interaction-design.md` — Interaction Design guidance.
- `references/curated/responsive-design.md` — Responsive Design guidance.
- `references/curated/tailwind-design-system.md` — Tailwind Design System guidance.
- `references/curated/theme-factory.md` — Theme Factory guidance.
- `references/curated/tool-design-style-selector.md` — Tool Design Style Selector guidance.
- `references/curated/tool-ui-ux-pro-max.md` — Tool Ui Ux Pro Max guidance.
- `references/curated/visual-design-foundations.md` — Visual Design Foundations guidance.
- `references/curated/web-design-reviewer.md` — Web Design Reviewer guidance.


## Design-data lookup

For a palette, typography, UX, or stack-guideline lookup, run `python scripts/tool-ui-ux-pro-max/search.py "query" --domain ux --json` from this skill directory. The pinned MIT dataset and checksums are in `scripts/data/provenance.json`. An error payload or nonzero exit is failure; never invent missing results.
