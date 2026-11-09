# Base procedure

Reviewed source clients: codex, claude.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# diff-inspector

Default to read-only, defect-first review of the requested change. Pin the comparison and trace findings through actual callers. Maintainability and strict thermo-nuclear modes require a specific request. Multiple reviewers are optional when scope warrants them; never assume named agent types.

## Select a mode

- Assess downstream consequences or “what could this break?” with [change-blast-check review](blast-radius.md).

- Review a local Git working tree before commit, handoff, or pull-request preparation. Read [the procedure](modes/local-change-quality-gate/guide.md).
- Coordinate parallel code reviews across multiple quality dimensions with finding deduplication, severity calibration, and consolidated reporting. Read [the procedure](modes/multi-reviewer-patterns/guide.md).
- Unified codebase quality review: merge readiness verdict + maintainability (Clean Code) + docs the change makes stale. Read [the procedure](modes/review-quality/guide.md).
- Only when explicitly requested: Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Read [the procedure](modes/thermo-nuclear-code-quality-review/guide.md).
- Only when explicitly requested: strict security and correctness audit limited to a branch's changes. Read [the procedure](modes/thermo-nuclear-review/guide.md). A security review of code beyond the diff, or of a whole stack, belongs to `secure-code-audit`.

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Companion skills

Load [required steps and optional helpers](skill-routes.md) only when their stated condition applies.
