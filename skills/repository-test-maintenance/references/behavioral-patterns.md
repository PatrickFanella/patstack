# Behavioral patterns for a durable suite

Read these examples when replacing brittle tests or repairing uncovered boundaries. They illustrate test selection, not a mandatory list for every repository.

## Identity and stored credentials

Test OAuth state mismatch and missing verifier before any exchange request, cleanup after a successful or failed exchange, and logout cleanup even when the server request fails. Keep server-side replay/authorization tests separate from client adapter tests.

Authentication tests must cover cached private data as well as credentials. On publicly routable detail pages, visit private content, log out through the UI, then use browser Back without reloading the application. Verify both server denial and absence of the private content. Exercise cancellation of in-flight reads so late responses cannot repopulate the previous session, and distinguish account changes from refreshing the same account. A fresh browser context alone cannot reveal a shared query-cache leak.

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

Before a page-wide accessibility scan, assert that representative loaded content is visible. A permissive route mock or an incorrect pagination envelope can leave the application on an error screen while the scanner passes. Match fixture routes narrowly and preserve the real response shape.

For request-recovery tests, retain evidence that the intended request was intercepted and failed, then restore that same endpoint and verify a successful retry with the current filters or drafts preserved. Avoid proving only that an error message or Retry button exists.

When fixed banners overlap the application, test keyboard focus visibility and actual bounding boxes across narrow and wide viewports. A class-name assertion cannot establish that a focused control remains reachable above a banner. For virtual feeds, exercise scrolling down, back up, and browser Back while checking both restored content and the mounted-item bound.

## Test harness discipline

Reset the mocks owned by a suite instead of blindly resetting all mocks when shared setup owns console enforcement or other invariants. Explicitly allow expected error output for the case that triggers it; avoid muting console errors globally.

Use isolated query clients, database fixtures, and cleanup so test order does not affect results. A test that passes only after another test initialized a module or session is a suite defect.

## Production browser journeys

When qualifying built application images, include the production service worker lifecycle. A development-server suite or a context with service workers blocked cannot establish that first activation or an accepted update preserves in-progress forms. Test first installation and accepted/declined updates as distinct behaviors when the application owns update prompts.

Use fresh disposable identities for independent executions and assert the authenticated identity before role-sensitive mutations. Keep simultaneous roles in isolated sessions; a shared persistent browser profile can invalidate the authorization comparison. Exercise normal quotas and rate controls. If repeated runs exhaust a per-account or per-IP budget, isolate the disposable fixtures and their actual network source rather than disabling the control or silently retrying until a pass.

Assert the visible completion state and reload persisted data. If a browser driver cannot read a response body, a separate authenticated read can verify persistence while preserving the original UI assertion. Record the browser and driver versions when comparing runtimes; a newer runner passing does not prove the old runner's failure was an application defect. Preserve the original error before attempting screenshots or traces, and bound diagnostic capture so a second failure cannot hide the first.

Exercise the other participant's interface in multi-role workflows. Approving a submission through a direct API call does not prove that the moderator can load the pending queue or find its review controls. Include populated data: an empty result bypasses row scanners and can hide a missing selected column. For saved preferences, verify the write, an independent read, and a fresh session; a successful write alone misses database decoding errors and clients that bypass CSRF or authentication interceptors.

Keep sustained load pacing consistent with ordinary client budgets, and record the offered request rate alongside virtual-user counts. Separate intentional burst rejection from ordinary journeys. Preserve failed runs, allocate fresh client addresses between executions, and never clear bans or relax success thresholds to manufacture capacity evidence. A paced-user pass is not a maximum-throughput or shared-network qualification.

Separate source prerequisites from external operator evidence before freezing a release candidate. Run source-only checks from the final acceptance verifier early, even when credentials or evidence hosting are unavailable. When an API contract changes, regenerate every maintained representation, including embedded specifications and route manifests, and tighten obsolete transitional allowances. A late source correction creates a new revision; retain earlier image and operational results under their actual identity instead of relabelling them.

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
