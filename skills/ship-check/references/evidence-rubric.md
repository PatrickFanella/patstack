# Repository Delivery Evidence Rubric

## Capability states

| State | Minimum evidence |
| --- | --- |
| Intended | Roadmap, plan, issue, or prose claim only |
| Scaffolded | Types, routes, UI shell, stubs, or configuration exist without a complete path |
| Implemented | Concrete end-to-end code path exists across required responsibilities |
| Test-verified | Relevant automated checks passed for the reviewed revision |
| Runtime-verified | Current target behavior passed a representative smoke or contract check |
| Production-verified | Intended revision passed the real host, route, auth, safety, and rollback-relevant contract |

Do not skip levels by inference. A higher level may include narrower caveats; a
runtime smoke does not automatically prove complete test coverage.

## Gap classes

- **Missing capability:** required behavior has no complete implementation.
- **Migration debt:** old and new paths coexist or an adapter remains incomplete.
- **Evidence gap:** implementation may exist, but current checks were not run or
  do not cover the claim.
- **Documentation drift:** docs contradict the active code or configuration.
- **Operational prerequisite:** backups, monitoring, credentials, capacity,
  deployment, or rollback work remains outside core implementation.
- **Maintainability risk:** concentration, duplication, unclear ownership, or
  fragile boundaries threaten future change.

## Viability judgment

Base viability on:

- coherence of the architecture and ownership boundaries;
- depth of implemented core paths;
- durability and migration posture;
- quality and breadth of automated evidence;
- operational safety and recoverability;
- size and coupling of the remaining work.

Use a direct verdict such as viable, viable with material conditions, uncertain,
or not currently viable. Name the conditions and evidence limits.

## Report shape

1. Verdict and confidence.
2. Scope and revision.
3. Implemented and verified capability.
4. Incomplete, planned, or migrating capability.
5. Verification performed and not performed.
6. Technical and operational risks.
7. Prioritized next steps.

Avoid raw file inventories in the final report unless they materially support a
claim.
