# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `verify-implementation` | required | Before claiming the reproducer is fixed. |
| `improve-performance` | optional | When the observed defect is a measured performance regression. |
| `investigate-code` | optional | When diagnosis depends on the pinned dependency implementation. |
| `build-and-fix-ci` | optional | When the failure reproduces only in CI or the report starts from a red check. |
| `postgres` | optional | When the root cause traces to a query, lock or migration. |
| `test-driven-development` | optional | When the user asks for the fix to be driven test-first. |
