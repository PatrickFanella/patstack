# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `verify-implementation` | optional | Before claiming a login, session or access-check flow works. |
| `manage-deployment-secrets` | optional | When signing keys or session secrets must be stored, injected or rotated. |
| `build-apis` | optional | When the auth change alters a public endpoint or API contract. |
