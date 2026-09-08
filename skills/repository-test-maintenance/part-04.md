## Reshape tests around contracts

For each important behavior, identify the suite and layer that owns it. A small maintained ownership registry can help larger repositories; file-existence checks are a discovery guard, not evidence of exercised behavior.

Prefer tests that fail when access is bypassed, data is corrupted, a public request changes shape, an async result becomes stale, or a failed write leaves the UI inconsistent. Retain security, transaction, concurrency, idempotency, pagination, retry/cancellation, and recovery cases where applicable.

Consolidate repeated setup and parallel cases into readable tables when inputs represent distinct outcomes. Remove tautologies, constructor/shape-only assertions, implementation-detail checks, and duplicate cases only after checking for unique contracts. Do not merely rename or combine files while leaving the same maintenance burden.

Choose the cheapest layer that can prove the behavior:

- Unit tests for pure rules and transformations.
- Component/state tests for interaction, state transitions, and cache behavior.
- Real database/service tests for persistence, isolation, transactions, and concurrency.
- Browser tests for journeys, focus, layout, and browser-dependent behavior.

Mocks belong at external boundaries. A mocked backend cannot prove authorization or persistence. Preserve a small real-service smoke tier; keep load, migration, restore, and deployment checks separate. Unsupported browser capabilities should be expressed through project selection rather than silently skipped cases.

When boundary work is needed, read [references/behavioral-patterns.md](references/behavioral-patterns.md) for concrete examples and common false confidence traps.
