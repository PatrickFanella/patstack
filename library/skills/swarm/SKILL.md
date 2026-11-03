---
name: swarm
description: "Swarm fan-out: run N parallel subagents on separate slices or as a race, then return one aggregated report. Use for /swarm or 'swarm this'. Not for a single delegated task."
disable-model-invocation: true
---

# Swarm

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todo list (the client's plan or todo tool, or a short checklist in chat) with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the client's concurrency limit.
4. Use the user's named worker model when given. Otherwise keep the client's default subagent model. For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes. Use a worktree, branch, or `/tmp/swarm-<slug>/worker-<n>/`.

## Phase B: Fan out

Spawn all N workers in one message with the client's subagent tool: the Agent tool in Claude Code (background), `spawn_agent` in Codex, or the task tool in OpenCode. Workers run on the current host unless the client offers remote execution and the user asked for it. If the client has no subagent tool, run the slices sequentially yourself and say so in the report.

When a worker must start from a non-default branch, give it a worktree on that branch.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
