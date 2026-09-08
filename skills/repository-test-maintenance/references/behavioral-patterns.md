# Behavioral patterns for a durable suite

Read these examples when replacing brittle tests or repairing uncovered boundaries. They illustrate test selection, not a mandatory list for every repository.

## Identity and stored credentials

Test OAuth state mismatch and missing verifier before any exchange request, cleanup after a successful or failed exchange, and logout cleanup even when the server request fails. Keep server-side replay/authorization tests separate from client adapter tests.

For encrypted browser storage, exercise the encryption path with real Web Crypto and an IndexedDB-compatible test implementation, as well as the unavailable-storage fallback. Useful cases include key loss or invalid key data, overwriting credentials, aborted transactions, and recovery after a failed write.

A request's success event does not prove its transaction committed. An asynchronous rejection is not caught by a surrounding synchronous try/catch unless awaited. If a failed update writes a fallback while older encrypted data remains, reads must follow the documented precedence and must not silently return stale credentials.

Client-side encryption with a key accessible to the same origin is not an XSS boundary. Test only the protection the implementation actually provides. Use browser coverage when storage behavior depends on the browser itself.

## Queries, mutations, and async state

Use the actual query/cache library where practical. Seed distinct cache entries, perform the mutation, and assert which views become stale and which remain untouched. Verify rejected writes preserve authoritative cached data and surface failure.

Exercise pagination limits, server-provided continuation metadata, final-page stopping, disabled queries, and identifier/access boundaries. Preserve cancellation and stale-response tests when concurrent work can overwrite newer state.

Avoid asserting only that a mocked mutation function was called. That misses broken invalidation, rollback, or cache-key selection.

## Playback and external SDKs

Mock the SDK boundary while rendering the real component. Verify coordination between players, callbacks after rerender, teardown on replacement/unmount, and supported fallback behavior.

Do not invent SDK methods to satisfy a component type. Test documented capability variations, such as cleanup when no destroy method exists. Verify the resulting DOM/resources, not only a cleanup spy.

Preserve browser tests for capabilities that DOM emulators cannot establish. Express browser support in the test projects, not a runtime skip that lets a required journey disappear.

## UI and accessibility

Assert accessible roles, keyboard interaction, focus behavior, and user-visible transitions. An accessibility scanner is useful alongside interaction tests, but neither a screenshot nor a scanner pass alone proves the whole journey accessible.

Prefer one coherent interaction test to many tests checking individual utility classes, static copy strings, or that a component renders. Retain layout-specific browser checks where actual geometry matters.

## Test harness discipline

Reset the mocks owned by a suite instead of blindly resetting all mocks when shared setup owns console enforcement or other invariants. Explicitly allow expected error output for the case that triggers it; avoid muting console errors globally.

Use isolated query clients, database fixtures, and cleanup so test order does not affect results. A test that passes only after another test initialized a module or session is a suite defect.

## Tooling and deletion traps

- Build-time plugins can appear unused to dependency analyzers that do not load the build configuration.
- Barrel exports and lazy entry points can obscure actual application reachability.
- Reflection, plugin discovery, generated code, and public package exports need entry points beyond the main application file.
- Tests excluded from the production compiler are not thereby obsolete; execute them and label any separate test-typecheck gate accurately.
- A green test command with prerequisite skips does not establish service-backed coverage.
- A registry proving that a suite exists cannot substitute for execution or meaningful assertions.

## Counterexamples to check before finalizing

- A checkout has untracked notes and tracked obsolete plans: clean up the requested tracked history without treating the notes as recoverable from Git.
- A static analyzer marks a configured plugin unused: verify the configuration before changing the dependency.
- A suite contains many payment replay cases: retain distinct replay/idempotency boundaries even if they resemble one another.
- Global coverage fails on the untouched baseline: do not disguise that fact with exclusions or claim a changed policy met the old target.
- A protected module is renamed: move its coverage contract and ensure the old missing path fails validation.
- Unit tests pass but integration services were unavailable: report the missing evidence instead of calling all tests green.
