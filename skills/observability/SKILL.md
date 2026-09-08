---
name: observability
description: Metrics, traces, dashboards, and SLOs; implement telemetry or diagnose a specific monitoring gap.
---

# observability

Start with the operational question and signal. Choose metrics, tracing, dashboards, or SLO design; keep signal names, labels, units, and time windows consistent across the selected artifacts.

## Select a mode

- Implement distributed tracing with Jaeger and Tempo to track requests across microservices and identify performance bottlenecks. Read [the procedure](references/modes/distributed-tracing/guide.md).
- Create and manage production Grafana dashboards for real-time visualization of system and application metrics. Read [the procedure](references/modes/grafana-dashboards/guide.md).
- Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Read [the procedure](references/modes/prometheus-configuration/guide.md).
- Define and implement Service Level Indicators (SLIs) and Service Level Objectives (SLOs) with error budgets and alerting. Read [the procedure](references/modes/slo-implementation/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
