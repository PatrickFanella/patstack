---
name: python-testing-patterns
description: "Use when writing or restructuring pytest suites: fixtures, parametrization, mocking, async tests, coverage. Not for repository-wide test upkeep (repository-test-maintenance)."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: language-python,python,testing,patterns
---

# python-testing-patterns

## Use this skill

Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices.

## Workflow

1. Confirm the request matches this skill's stated intent; do not activate it
   for a keyword-only near miss.
2. Inspect the user's inputs, repository conventions, and available tools before
   selecting an approach.
3. Load only the relevant section of the detailed guide when the task needs
   domain-specific patterns or edge cases.
4. Perform the smallest complete unit of work and preserve existing behavior or
   user data unless change is explicitly requested.
5. Validate the result with the project's own checks plus any skill-specific
   verification described in the detailed guide.

## Constraints

- Prefer the project's existing stack and conventions over generic examples.
- State required credentials, network access, CLIs, and destructive side effects
  before relying on them.
- Use current authoritative documentation when provider or framework behavior is
  version-sensitive.
- Report concrete evidence, remaining risks, and any unverified assumptions.

## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
- `references/advanced-patterns.md` — async tests, monkeypatching, conftest, property-based, database and CI patterns.
