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

**Reference:** See `references/error-budget.md`
