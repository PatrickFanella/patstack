---
name: bug-tracer
description: "Use when a bug, failing test or unexpected behavior needs a root cause: reproduce, isolate one variable at a time, verify the fix. Also for recurring-failure postmortems."
---

# bug-tracer

Establish a failing observation before selecting a cause. Change one causal variable at a time; verify the same reproducer after repair. Use recurring-failure analysis only for repeated incidents, not every trivial failure.

## Select a mode

- Diagnosis loop for hard bugs and performance regressions. Read [the procedure](references/modes/diagnosing-bugs/guide.md).
- Analyze recurring failures and produce prevention-focused postmortems. Read [the procedure](references/modes/failure-anthropologist/guide.md).
- Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Read [the procedure](references/modes/systematic-debugging/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [fix root causes](references/principles/fix-root-causes.md) — consult only for this specific design or execution concern.

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
