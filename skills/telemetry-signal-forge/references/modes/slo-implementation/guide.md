# SLO implementation

Define Service Level Indicators (SLIs), Service Level Objectives (SLOs) and error budgets that balance reliability with delivery speed.

Paths here are relative to this mode directory; pass the target repository explicitly.

## SLI/SLO/SLA Hierarchy

```
SLA (Service Level Agreement)
  ↓ Contract with customers
SLO (Service Level Objective)
  ↓ Internal reliability target
SLI (Service Level Indicator)
  ↓ Actual measurement
```

## Error Budget Calculation

### Error Budget Formula

```
Error Budget = 1 - SLO Target
```

**Example:**

- SLO: 99.9% availability
- Error Budget: 0.1% = 43.2 minutes/month
- Current Error: 0.05% = 21.6 minutes/month
- Remaining Budget: 50%

### Error Budget Policy

```yaml
error_budget_policy:
  - remaining_budget: 100%
    action: Normal development velocity
  - remaining_budget: 50%
    action: Consider postponing risky changes
  - remaining_budget: 10%
    action: Freeze non-critical changes
  - remaining_budget: 0%
    action: Feature freeze, focus on reliability
```

## Best Practices

1. **Start with user-facing services**
2. **Use multiple SLIs** (availability, latency, etc.)
3. **Set achievable SLOs** (don't aim for 100%)
4. **Implement multi-window alerts** to reduce noise
5. **Track error budget** consistently
6. **Review SLOs regularly**
7. **Document SLO decisions**
8. **Align with business goals**
9. **Automate SLO reporting**
10. **Use SLOs for prioritization**

For metric collection use the [Prometheus configuration mode](../prometheus-configuration/guide.md); for visualization use the [Grafana dashboards mode](../grafana-dashboards/guide.md).

## Read when needed

- [Defining SLIs](part-05.md): read when choosing availability, latency or durability indicators.
- [Setting SLO targets](part-06.md): read when picking target percentages and windows.
- [SLO implementation](part-08.md): read when writing Prometheus recording and alerting rules for an SLO.
- [SLO dashboard](part-09.md): read when building the SLO and error-budget dashboard.
- [Multi-window burn rate alerts](part-10.md): read when tuning SLO alerts to cut noise.
- [SLO review process](part-11.md): read when setting up weekly, monthly or quarterly SLO reviews.
