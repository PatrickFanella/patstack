# Grilling a plan

Adapted from Matt Pocock's grilling workflow. Inspect the repository and existing decisions first; look up facts yourself.

Map unresolved decisions and their dependencies. Ask a small round of questions whose prerequisites are settled, with a recommended answer and concrete tradeoffs for each. Wait for those decisions before asking dependent questions. Continue useful fact-finding while answers are pending. Use available question tools and respect their size limits.

A requested deep interview can take several rounds. An ordinary implementation task needs only the ambiguity resolved, not an exhaustive interview. Respect the user's stopping point. A request for an interview alone does not authorize implementation.

For grill-with-docs, update the existing decision record and domain glossary as choices settle. State accepted decisions, rejected alternatives with reasons, unresolved questions, and observable acceptance criteria. Reuse the existing canonical docs; do not create a competing CONTEXT.md or ADR system.

Finish when material decisions are resolved or the user stops the interview. Keep remaining unknowns explicit. Never repeat settled questions or invent an approval requirement for work already authorized.
