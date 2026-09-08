---
name: systematic-debugging
description: Reproduce and diagnose a defect; choose a tight failing check, isolate the cause, and verify the repair.
---

# systematic-debugging

Establish a failing observation before selecting a cause. Change one causal variable at a time; verify the same reproducer after repair. Use recurring-failure analysis only for repeated incidents, not every trivial failure.

## Select a mode

- Diagnosis loop for hard bugs and performance regressions. Read [the procedure](references/modes/diagnosing-bugs/guide.md).
- Analyze recurring failures and produce prevention-focused postmortems. Read [the procedure](references/modes/failure-anthropologist/guide.md).
- Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Read [the procedure](references/modes/systematic-debugging/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [fix root causes](references/principles/fix-root-causes.md) — consult only for this specific design or execution concern.
