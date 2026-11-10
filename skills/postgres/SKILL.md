---
name: postgres
description: Diagnose PostgreSQL queries, locks and indexes, or plan and apply requested
  schema migrations and backfills.
---

# postgres

Select diagnosis, tuning or migration from the request. Inspect the real schema and baseline first. Use expand/backfill/contract when appropriate, with explicit rollback and data checks; read-only analysis does not authorize database writes.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **pg plan reader**: Use for PostgreSQL against a real schema: slow queries and EXPLAIN plans, indexes, locks, replication, data-quality constraints and checks. Read [the procedure](references/base-workflow.md).
- **schema migrator**: Use when changing a database schema or transforming data: ORM migrations, backfills, zero-downtime expand and contract, cutover and rollback. Read [the procedure](references/modes/schema-migrator/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
