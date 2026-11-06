## Make the result maintainable

Prefer existing tools and conventions over introducing another framework. Add or repair only gates that address demonstrated recurrence risks:

- A documented local command aligned with CI for type checking, lint, source analysis, test discovery, and the appropriate tests.
- Rejection of focused and placeholder tests; explicit, reviewable prerequisites for environment-dependent skips. Critical integration runners should fail when required dependencies or tests are missing.
- Unused-source checks with explicit entry points and treatment of dynamic loading. Do not claim complete dead-code detection from a simple import graph.
- Behavioral coverage floors where they offer useful protection.
- Worker limits, isolated fixtures, and explicit cleanup appropriate to the repository's CI resources.

Tests and test helpers should not leak into production artifacts. For example, Go helpers used only by tests belong in `_test.go` files. Distinguish production type checking from type checking test code when reporting the gate's scope.

### Coverage decisions

The no-green-by-deletion rule in `SKILL.md` governs this section. Repair uncovered crucial behavior with meaningful tests before considering policy changes.

If an inherited global gate already fails, report that baseline honestly. Replacing it with module-specific floors is a policy change, not an automatic cleanup step. Consider whether it fits the user's authorized overhaul and the repository's requirements. Make the tradeoff explicit; otherwise retain the gate and identify the unresolved failure.

When module-specific floors are appropriate:

- Derive modules and floors from actual critical behavior and measured coverage, not numbers copied from another repository.
- Continue reporting whole-application coverage.
- Reject missing or excluded protected modules so a rename/deletion cannot silently remove protection.
- Explain lower existing floors as gaps, not completeness.
- Verify that a missing critical exercise causes a gate failure.
- Update contracts when moving modules, and raise floors when strengthening tests.
