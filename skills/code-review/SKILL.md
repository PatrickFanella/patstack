---
name: code-review
description: Review code changes for actionable defects or requested maintainability concerns; keep repository audits separate.
---

# code-review

Default to read-only, defect-first review of the requested change. Pin the comparison and trace findings through actual callers. Maintainability and strict thermo-nuclear modes require a specific request. Multiple reviewers are optional when scope warrants them; never assume named agent types.

## Select a mode

- Assess downstream consequences or “what could this break?” with [blast-radius review](references/blast-radius.md).

- Review a local Git working tree before commit, handoff, or pull-request preparation. Read [the procedure](references/modes/local-change-quality-gate/guide.md).
- Coordinate parallel code reviews across multiple quality dimensions with finding deduplication, severity calibration, and consolidated reporting. Read [the procedure](references/modes/multi-reviewer-patterns/guide.md).
- Unified codebase quality review: merge readiness verdict + maintainability (Clean Code) + docs-vs-code consistency. Read [the procedure](references/modes/review-quality/guide.md).
- Only when explicitly requested: Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Read [the procedure](references/modes/thermo-nuclear-code-quality-review/guide.md).
- Only when explicitly requested: Comprehensive security and correctness audit of a branch's changes. Read [the procedure](references/modes/thermo-nuclear-review/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
