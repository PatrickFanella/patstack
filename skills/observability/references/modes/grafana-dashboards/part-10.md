## Common Dashboard Patterns

### Infrastructure Dashboard

**Key Panels:**

- CPU utilization per node
- Memory usage per node
- Disk I/O
- Network traffic
- Pod count by namespace
- Node status

**Reference:** See `assets/infrastructure-dashboard.json`

### Database Dashboard

**Key Panels:**

- Queries per second
- Connection pool usage
- Query latency (P50, P95, P99)
- Active connections
- Database size
- Replication lag
- Slow queries

**Reference:** See `assets/database-dashboard.json`

### Application Dashboard

**Key Panels:**

- Request rate
- Error rate
- Response time (percentiles)
- Active users/sessions
- Cache hit rate
- Queue length
