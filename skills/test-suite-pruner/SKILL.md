---
name: test-suite-pruner
description: "Use when a test suite is oversized, slow, flaky or brittle: baseline it, delete obsolete tests with evidence, reshape around contracts. Not for test-first work (red-green-loop)."
---

# test-suite-pruner

Produce a smaller, understandable repository whose important contracts still execute and whose maintenance checks keep the removed clutter from returning. Optimize for regression detection and maintenance cost, not a target test count or coverage percentage.

## Rules for every run

- Never lower thresholds, broaden exclusions, or delete failing tests simply to produce green output. Preserve working gates by default. If an inherited gate already fails, report that baseline honestly.
- Treat analyzer output as deletion candidates, not authority. Keep unrelated dirty work and uncertain untracked material intact, and avoid broad destructive cleanup commands that erase files without classification.
- A request to get up to date means fetch and compare, not permission to upgrade every dependency.
- Do not add trivial tests just to raise an average; coverage cannot establish assertion quality.
- Local verification does not imply a release. Keep commit, push, merge, deployment and outward communication within the user's existing authorization.

## Workflow

Follow the steps in [the task guide](guide.md) in order, reading each procedure when you reach it. Keep the requested scope and repository conventions, and report evidence for the operation actually performed.
