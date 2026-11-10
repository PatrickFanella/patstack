# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `fix-bugs` | optional | When the failing check also fails locally and needs a root cause. |
| `manage-deployment-secrets` | optional | When a pipeline needs a secret added or a failure traces to a missing or expired secret. |
| `clean-up-test-suites` | optional | When flaky or slow tests, not the pipeline, keep checks red. |
| `manage-infrastructure` | optional | When pipeline design needs Kubernetes manifests, Terraform or runner changes. |
