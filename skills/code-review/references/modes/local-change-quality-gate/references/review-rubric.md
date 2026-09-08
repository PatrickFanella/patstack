# Local Change Review Rubric

## Evidence order

1. Applicable repository instructions and requested outcome.
2. Staged, unstaged, and untracked file inventory.
3. Changed behavior and its callers or consumers.
4. Existing tests and documentation.
5. Commands executed in the current review.

## Finding threshold

Report a finding only when it has:

- an identifiable changed location;
- a reproducible or logically complete failure scenario;
- meaningful impact on correctness, safety, compatibility, operations, or
  maintainability;
- an actionable remedy.

Classify findings as blocking, important, or advisory. Do not inflate style
preferences into defects.

## Scope checks

- Does each changed file serve the requested outcome?
- Are generated files paired with their source changes?
- Are schema, migration, configuration, or API changes backward-compatible?
- Are docs and examples consistent with implemented behavior?
- Did unrelated user work get mixed into the intended handoff?

## Verification depth

- Local leaf change: focused tests and static checks.
- Shared library or public contract: affected callers plus broader package tests.
- Build, dependency, schema, migration, auth, or deployment change: repository
  gate plus the relevant smoke or compatibility check.
- Documentation-only change: link, command, and claim validation.

Never claim behavior was verified when only structure or documentation was
inspected.
