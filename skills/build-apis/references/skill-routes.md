# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `build-and-fix-auth` | optional | When an endpoint needs login, sessions or access checks. |
| `verify-implementation` | optional | Before claiming an implemented endpoint or contract works; not for a design-only request. |
| `postgres` | optional | When the API change needs a PostgreSQL schema migration or query design. |
| `typescript` | optional | When the contract is implemented in a TypeScript service or client. |
