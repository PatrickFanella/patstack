---
name: performance-investigation
description: Diagnose measured latency, CPU, memory, or throughput regressions using comparable profiles and benchmarks.
compatibility: Profiling and benchmark commands depend on the project runtime; use only tools already available in the target environment unless the user approves installation.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: performance profiling,slow endpoint,high cpu,memory leak,latency regression,benchmark verification
---

# Performance Investigation

Treat performance as an evidence problem. Preserve behavior, measure the same
workload before and after changes, and avoid optimizing code that is not on the
measured hot path.

## Workflow

1. Define the symptom and target:
   - affected workload, input, environment, and concurrency
   - metric such as latency, throughput, CPU, memory, allocations, or build time
   - acceptable threshold or comparison baseline
2. Reproduce with the smallest representative workload. Record the command,
   inputs, warm-up policy, sample count, and current result.
3. Localize the cost using available evidence: profiler, trace, query plan,
   flame graph, browser performance recording, allocation report, or focused
   timing instrumentation.
4. Form one falsifiable hypothesis tied to the measured hot path. Change one
   material factor at a time.
5. Re-run the same workload and report both absolute results and relative
   change. Check variance before claiming improvement.
6. Run correctness tests and add a regression benchmark or budget when it can
   be stable in the project environment.

## Guardrails

- Never trade correctness, security, accessibility, or maintainability for an
  unmeasured speedup.
- Separate cold-start, warm-state, network, database, and client-render costs.
- Treat microbenchmarks as local evidence, not proof of end-to-end improvement.
- Call out noisy environments, small samples, caches, and changed inputs.
- If profiling cannot reproduce the symptom, stop with the evidence and the
  next discriminating measurement instead of guessing.

## Report

Return the baseline, bottleneck evidence, change, after-result, confidence and
variance, correctness checks, and any remaining risk.
