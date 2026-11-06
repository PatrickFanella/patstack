# Grafana dashboards

Design and manage production Grafana dashboards for applications, infrastructure and business metrics.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Dashboard Design Principles

### 1. Hierarchy of Information

```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │
└─────────────────────────────────────┘
```

### 2. RED Method (Services)

- **Rate** - Requests per second
- **Errors** - Error rate
- **Duration** - Latency/response time

### 3. USE Method (Resources)

- **Utilization** - % time resource is busy
- **Saturation** - Queue length/wait time
- **Errors** - Error count

## Best Practices

1. **Start with templates** (Grafana community dashboards)
2. **Use consistent naming** for panels and variables
3. **Group related metrics** in rows
4. **Set appropriate time ranges** (default: Last 6 hours)
5. **Use variables** for flexibility
6. **Add panel descriptions** for context
7. **Configure units** correctly
8. **Set meaningful thresholds** for colors
9. **Use consistent colors** across dashboards
10. **Test with different time ranges**

For metric collection use the [Prometheus configuration mode](../prometheus-configuration/guide.md); for SLO targets and burn-rate alerts use the [SLO implementation mode](../slo-implementation/guide.md).

## Read when needed

- [Dashboard structure](part-05.md): read when laying out a new service dashboard's panels and queries.
- [Panel types](part-06.md): read when configuring a stat, time-series, table or heatmap panel.
- [Variables](part-07.md): read when adding template variables or using them in queries.
- [Alerts in dashboards](part-08.md): read when attaching an alert rule to a panel.
- [Dashboard provisioning](part-09.md): read when loading dashboards from files through provisioning.
- [Common dashboard patterns](part-10.md): read when building an infrastructure, database or application dashboard.
- [Dashboard as code](part-12.md): read when managing dashboards with Terraform or Ansible.
