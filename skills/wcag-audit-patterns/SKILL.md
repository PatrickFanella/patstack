---
name: wcag-audit-patterns
description: Audit or repair web accessibility using keyboard, semantics, contrast, and assistive-technology evidence.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: mobile-apps,wcag,audit,patterns
---

# WCAG Audit Patterns

Use for web accessibility audits and fixes. Screen-reader-specific material is available as merged reference, but the active workflow is WCAG-first.

## Workflow

1. Identify target pages/components and required conformance level (usually WCAG 2.2 AA).
2. Run automated checks if tooling exists.
3. Manually verify keyboard, focus order, landmarks, headings, labels, names/roles/states, contrast, and responsive zoom.
4. Add screen-reader checks when flows are critical or ARIA/custom widgets are involved.
5. Fix at source with semantic HTML first; use ARIA only when native semantics cannot express the control.
6. Re-test and document residual risk.

## Review Checklist

- [ ] Keyboard-only flow works.
- [ ] Visible focus is clear.
- [ ] Forms and controls have accessible names.
- [ ] Headings/landmarks communicate structure.
- [ ] Color contrast passes target level.
- [ ] Dynamic UI updates are announced when needed.
- [ ] Custom widgets expose correct role/state/keyboard behavior.

## Resources

- `references/full-guide.md` — detailed WCAG audit checklist.

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/screen-reader-testing.md` — Screen Reader Testing guidance.
