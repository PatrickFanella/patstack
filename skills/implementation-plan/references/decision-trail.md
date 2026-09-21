# Reviewable decision trail

For requested “show me your work”, a long unattended migration, or a multi-phase task whose choices need review, keep one evidence log beside the existing plan. Reuse the project's existing ledger. For short work, a normal result summary is enough.

Use TSV columns `ts`, `phase`, `decision`, `reason`, `evidence`, `result`. A row records an observable decision or checkpoint and a concise reason, not hidden reasoning or a transcript of deliberation. Evidence is a resolvable path, commit, test result, or URL. Record actual outcomes, including failed and inconclusive checks.

Append corrections as new rows that supersede earlier claims. Preserve failed evidence. Keep cells single-line and escape leading spreadsheet formula characters when exporting TSV. Log meaningful choices, pivots, completed units, and blockers, not every command.

Before handoff, verify evidence pointers against the actual artifacts. Record missing proof as unverified. Store the log privately by default; use the project's commit/publication policy. Never collect unrelated conversation histories or require an unavailable cross-model reviewer. Independent review is optional when authorized and useful.
