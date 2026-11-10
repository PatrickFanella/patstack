# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `manage-infrastructure` | optional | When injection or rotation touches a self-hosted server or service. |
| `build-and-fix-ci` | optional | When a moved or rotated secret requires changing or rechecking a CI pipeline. |
| `verify-implementation` | optional | Before revoking the old credential, to prove consumers work with the new one. |
