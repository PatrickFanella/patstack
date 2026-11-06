# PostgreSQL pro

Query optimization with EXPLAIN, index design, JSONB, replication, extensions, and VACUUM/autovacuum maintenance.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Core Workflow

1. **Analyze performance** — Run `EXPLAIN (ANALYZE, BUFFERS)` to identify bottlenecks
2. **Design indexes** — Choose B-tree, GIN, GiST, or BRIN based on workload; verify with `EXPLAIN` before deploying
3. **Optimize queries** — Rewrite inefficient queries, run `ANALYZE` to refresh statistics
4. **Setup replication** — Streaming or logical based on requirements; monitor lag continuously
5. **Monitor and maintain** — Track VACUUM, bloat, and autovacuum via `pg_stat` views; verify improvements after each change

### End-to-End Example: Slow Query → Fix → Verification

```sql
-- Step 1: Identify slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Step 2: Analyze a specific slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
-- Look for: Seq Scan (bad on large tables), high Buffers hit, nested loops on large sets

-- Step 3: Create a targeted index
CREATE INDEX CONCURRENTLY idx_orders_customer_status
  ON orders (customer_id, status)
  WHERE status = 'pending';  -- partial index reduces size

-- Step 4: Verify the index is used
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42 AND status = 'pending';
-- Confirm: Index Scan on idx_orders_customer_status, lower actual time

-- Step 5: Update statistics if needed after bulk changes
ANALYZE orders;
```

## Constraints

### MUST DO
- Use `EXPLAIN (ANALYZE, BUFFERS)` for query optimization
- Verify indexes are actually used with `EXPLAIN` before and after creation
- Use `CREATE INDEX CONCURRENTLY` to avoid table locks in production
- Run `ANALYZE` after bulk data changes to refresh statistics
- Monitor autovacuum; tune `autovacuum_vacuum_scale_factor` for high-churn tables
- Use connection pooling (pgBouncer, pgPool)
- Monitor replication lag via `pg_stat_replication`
- Use prepared statements to prevent SQL injection
- Use `uuid` type for UUIDs, not `text`

### MUST NOT DO
- Disable autovacuum globally
- Create indexes without first analyzing query patterns
- Use `SELECT *` in production queries
- Ignore replication lag alerts
- Skip VACUUM on high-churn tables
- Store large BLOBs in the database (use object storage)
- Deploy index changes without verifying the planner uses them

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Performance | `references/performance.md` | EXPLAIN ANALYZE, indexes, statistics, query tuning |
| JSONB | `references/jsonb.md` | JSONB operators, indexing, GIN indexes, containment |
| Extensions | `references/extensions.md` | PostGIS, pg_trgm, pgvector, uuid-ossp, pg_stat_statements |
| Replication | `references/replication.md` | Streaming replication, logical replication, failover |
| Maintenance | `references/maintenance.md` | VACUUM, ANALYZE, pg_stat views, monitoring, bloat |
| Table design | `references/curated/postgresql-table-design.md` | Data types, keys, constraints, partitioning |
| SQL optimization | `references/curated/sql-optimization-patterns.md` | Query rewrites and optimization patterns |

## Output Templates

When implementing PostgreSQL solutions, provide:
1. Query with `EXPLAIN (ANALYZE, BUFFERS)` output and interpretation
2. Index definitions with rationale and pre/post verification
3. Configuration changes with before/after values
4. Monitoring queries for ongoing health checks
5. Brief explanation of performance impact

## Read when needed

- [Common patterns](part-05.md): read when writing a JSONB GIN query, checking bloat and dead tuples, or monitoring replication lag.
