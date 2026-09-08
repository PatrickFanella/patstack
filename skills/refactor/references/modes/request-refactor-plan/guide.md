# Refactor planning

Use this mode when asked for a refactor plan. Inspect the described problem, relevant interfaces, current changes, and tests first. Clarify only material decisions that remain unresolved; do not require a broad interview for a bounded request.

Compare plausible alternatives when the tradeoff matters. State scope, compatibility boundaries, and the verification that protects behavior. Break the chosen approach into small verifiable units. Produce the plan locally or in the response and stop before implementation. Create an issue only when publishing that issue is explicitly requested.

Use the following outline proportionally to the task:

<refactor-plan-template>

## Problem Statement

The problem that the developer is facing, from the developer's perspective.

## Solution

The solution to the problem, from the developer's perspective.

## Implementation units

An ordered plan of verifiable changes. Each unit should leave a working result; identify checks and dependencies. Do not require commits unless requested.

## Decision Document

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Reference inspected paths where they make the plan actionable; mark assumptions that require rechecking.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this refactor.

## Further Notes (optional)

Any further notes about the refactor.

</refactor-plan-template>
