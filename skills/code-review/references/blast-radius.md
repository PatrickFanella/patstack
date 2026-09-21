# Blast radius

Use for “what could this break?”, a requested blast-radius review, or a small diff with consequences outside its immediate callers.

1. Pin the diff and trace the changed behavior. Follow consumers beyond symbol search: serialized fields, database readers, generated clients, feature flags, lifecycle timing, and the pinned dependency implementation.
2. Identify the one or two facts the safety claim depends on. State each as a falsifiable claim.
3. Use the cheapest representative execution of the real code to disprove each claim. Prefer an existing test or a small reproducible script; a running-app reproduction is stronger when the concern is runtime behavior.
4. Distinguish code inspection, an executed test, and a live reproduction. Mark a claim unproven if execution is unavailable; a plausible explanation or a prior agent summary is not evidence.
5. Report confirmed failure paths with source locations, consequences, and verification. Separate cleared concerns from remaining unknowns. Keep the review read-only unless fixes are requested.

Do not automatically launch an arena or multiple models. Use the available authorization and task scope. Keep secrets out of evidence and public reports.
