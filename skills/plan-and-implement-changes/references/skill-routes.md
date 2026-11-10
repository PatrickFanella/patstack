# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `verify-implementation` | required | When an implementation task reaches verification; not for a plan-only request. Or: Before reporting the implementation as working. |
| `define-requirements` | optional | When an unresolved product choice changes the implementation. |
| `temporal-workflows` | optional | When the feature contains durable Temporal workflows. |
| `manage-infrastructure` | optional | When the requested deliverable includes Terraform modules. |
| `react-native-expo` | optional | When implementing a React Native/Expo feature. |
| `manage-roadmaps-and-issues` | optional | When the finished plan should be published as tracker issues with a roadmap. |
| `test-driven-development` | required | For the explicitly requested test-first implementation flow. |
| `review-code-changes` | required | For the final code review specified by this implementation flow. |
| `map-codebase` | optional | When the target repository is unfamiliar and the plan needs its structure first. |
| `design-architecture` | optional | When the plan hinges on an unsettled module boundary or interface. |
| `throwaway-prototype` | optional | When a design question needs a runnable answer before the plan can settle. |
| `coordinate-parallel-agents` | optional | When the plan splits work across parallel worker agents. |
| `postgres` | optional | When the implementation includes a PostgreSQL schema migration or backfill. |
| `handoff-and-recall-work` | optional | When a multi-session implementation stops before it is finished. |
