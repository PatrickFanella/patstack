# Local Change Quality Gate

Evaluate the change as evidence, not as an invitation to modify or publish it.

## Workflow

1. **Resolve scope.**
   - Confirm the repository root and current branch.
   - Read every applicable `AGENTS.md`.
   - Preserve unrelated changes and treat untracked files as user-owned.
2. **Inventory without exposing content.**
   - Run `python3 scripts/change_inventory.py <repo> --format markdown`.
   - Inspect staged and unstaged diffs separately.
   - Compare against the requested change, not an assumed branch purpose.
3. **Map impact.**
   - Identify changed responsibilities, public contracts, generated files,
     migrations, configuration, and documentation.
   - Read [references/review-rubric.md](references/review-rubric.md) when
     classifying findings or deciding verification depth.
4. **Review behavior.**
   - Trace changed code through callers, tests, and failure paths.
   - Report only actionable findings supported by a concrete path or scenario.
   - Distinguish defects from optional cleanup and pre-existing problems.
5. **Verify proportionally.**
   - Prefer repository-documented checks, then the narrowest relevant tests.
   - Run broader checks when shared contracts, build configuration, schemas,
     migrations, or security boundaries changed.
   - Record commands, results, skips, and environmental blockers.
6. **Report readiness.**
   - Lead with blocking findings in severity order.
   - Then summarize scope, checks passed, unverified behavior, and handoff risk.
   - State explicitly when no actionable findings remain.

## Safety Boundaries

- Stay read-only unless the user separately asks for fixes.
- Do not stage, commit, push, publish, discard, reset, clean, or rewrite files.
- Do not print secrets or entire environment/configuration files.
- Do not treat a clean test run as proof that an uncovered behavior is correct.
- Route hosted PR review to the GitHub review skill and remote CI failure to the
  GitHub CI skill.

## Completion Contract

Finish only when the inspected file set is explicit, applicable instructions
were applied, relevant checks were attempted, and evidence limits are stated.
