# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `build-and-fix-auth` | optional | When export or deletion endpoints need identity or object-level access checks. |
| `postgres` | optional | When retention or deletion requires a schema migration or backfill. |
| `verify-implementation` | optional | Before claiming deletion, export or consent enforcement works. |
