# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `build-and-fix-observability` | optional | When a production slowdown cannot be measured because a metric or trace is missing. |
| `fix-bugs` | optional | When measurement exposes a functional defect rather than a cost. |
| `postgres` | optional | When the measured hot path is a query plan or lock wait. |
| `react-and-nextjs` | optional | When the measured cost is React rerenders or bundle size. |
| `golang` | optional | When profiling Go code with pprof or benchmarks. |
