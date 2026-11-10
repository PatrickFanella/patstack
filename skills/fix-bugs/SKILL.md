---
name: fix-bugs
description: "Use when a bug or reproducible failing test needs a root cause: reproduce, isolate one variable at a time, verify the fix; also recurring-failure postmortems. A red CI check starts in build-and-fix-ci; slowness goes to improve-performance."
---

# fix-bugs

Establish a failing observation before selecting a cause. Change one causal variable at a time; verify the same reproducer after repair. Use recurring-failure analysis only for repeated incidents, not every trivial failure.

## Select a mode

- Hard or intermittent bugs that resist a first pass: build a tight red/green feedback loop, minimise the repro, rank hypotheses. Read [the procedure](references/modes/diagnosing-bugs/guide.md).
- Analyze recurring failures and produce prevention-focused postmortems. Read [the procedure](references/modes/failure-anthropologist/guide.md).
- Default for an ordinary bug, test failure or unexpected behavior: the root-cause pass before proposing any fix. Read [the procedure](references/modes/systematic-debugging/guide.md).

Performance regressions belong to `improve-performance`. A failing CI check starts in `build-and-fix-ci`; come back here once a failing test reproduces and needs a root cause.

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

## Conditional design notes

- [fix root causes](references/principles/fix-root-causes.md): read before applying a fix, to check it addresses the cause rather than hiding the failing state.

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
