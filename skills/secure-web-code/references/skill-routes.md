# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `threat-modeling` | optional | When the user also wants findings prioritized against a system threat model. |
| `build-and-fix-auth` | optional | When a confirmed finding in login, session or access-check code must be fixed. |
| `manage-deployment-secrets` | optional | When the review finds hardcoded or leaked credentials that must be moved or rotated. |
