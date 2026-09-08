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
