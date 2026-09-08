## Setting SLO Targets

### Availability SLO Examples

| SLO %  | Downtime/Month | Downtime/Year |
| ------ | -------------- | ------------- |
| 99%    | 7.2 hours      | 3.65 days     |
| 99.9%  | 43.2 minutes   | 8.76 hours    |
| 99.95% | 21.6 minutes   | 4.38 hours    |
| 99.99% | 4.32 minutes   | 52.56 minutes |

### Choose Appropriate SLOs

**Consider:**

- User expectations
- Business requirements
- Current performance
- Cost of reliability
- Competitor benchmarks

**Example SLOs:**

```yaml
slos:
  - name: api_availability
    target: 99.9
    window: 28d
    sli: |
      sum(rate(http_requests_total{status!~"5.."}[28d]))
      /
      sum(rate(http_requests_total[28d]))

  - name: api_latency_p95
    target: 99
    window: 28d
    sli: |
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
      /
      sum(rate(http_request_duration_seconds_count[28d]))
```
