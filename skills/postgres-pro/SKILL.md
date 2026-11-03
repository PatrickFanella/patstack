---
name: postgres-pro
description: "Use for PostgreSQL against a real schema: slow queries and EXPLAIN plans, indexes, locks, replication, data-quality constraints and checks. Not for migration rollout (database-migration)."
---

# postgres-pro

Use the real schema and query plan to establish the problem. Separate read-only diagnostics from index, schema, data, replication, and production changes. Data-quality conclusions need explicit keys and population boundaries.

## Select a mode

- Implement PostgreSQL-first data quality checks using constraints, indexes, validation queries, pgTAP/dbt when useful, and CI-safe SQL checks. Read [the procedure](references/modes/postgres-data-quality/guide.md).
- Use when optimizing PostgreSQL queries, configuring replication, or implementing advanced database features. Read [the procedure](references/modes/postgres-pro/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
