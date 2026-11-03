---
name: prometheus-configuration
description: "Use when writing or debugging Prometheus scrape configs, recording or alerting rules, exporters, remote write or retention. Not for dashboards, tracing or SLO design (observability)."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: analytics-observability,prometheus,configuration
---

# prometheus-configuration

## Use this skill

Set up Prometheus for comprehensive metric collection, storage, and monitoring of infrastructure and applications. Use when implementing metrics collection, setting up monitoring infrastructure, or configuring alerting systems.

## Workflow

1. Confirm the request matches this skill's stated intent; do not activate it
   for a keyword-only near miss.
2. Inspect the user's inputs, repository conventions, and available tools before
   selecting an approach.
3. Load only the relevant section of the detailed guide when the task needs
   domain-specific patterns or edge cases.
4. Perform the smallest complete unit of work and preserve existing behavior or
   user data unless change is explicitly requested.
5. Validate the result with the project's own checks plus any skill-specific
   verification described in the detailed guide.

## Constraints

- Prefer the project's existing stack and conventions over generic examples.
- State required credentials, network access, CLIs, and destructive side effects
  before relying on them.
- Use current authoritative documentation when provider or framework behavior is
  version-sensitive.
- Report concrete evidence, remaining risks, and any unverified assumptions.
- In this homelab, central Prometheus, Blackbox probes and alerting run on Dozor; NUC runs a remote-write agent. Read `~/.homelab/HOMELAB.md` and the live config on the target host before changing either.

## Resources

- `references/detailed-guide.md` — detailed framework and edge cases; load only the sections needed for the task.
