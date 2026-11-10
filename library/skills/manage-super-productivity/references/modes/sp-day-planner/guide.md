# sp-day-planner procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# Super Productivity Planning

## Overview

Run Super Productivity planning as a controlled live-data operation. This skill
owns the user's recurring daily framework, one-off task placement, task hygiene,
estimates, minimal tags, and reusable routines with subtasks.

## Load-on-Demand References

- Read `references/system-baseline.md` before changing recurring schedules,
  projects, tags, or reusable routines.
- Read `references/planning-runbook.md` before any broad or mutating planning
  pass.
- Read `references/verification-checklist.md` before the final report or when
  the user asks for strong guarantees such as “nothing unscheduled remains.”

## Boundaries

- Use the `sp-mcp-doctor` mode when the server, plugin bridge, catalog, or
  client configuration is failing.
- Use the base procedure when the user wants a high-level periodic
  audit and has not selected planning as the lane.
- Do not delete, bulk-complete, rewrite recurrence templates, or create new
  taxonomy without the required user intent.

## Scheduling Model

- Use recurrence `startTime` for reusable daily and weekly anchors.
- Use due dates for genuine deadlines, not as substitutes for work blocks.
- Use `plannedAt` for one-off placement. An empty `plannedAt` range does not
  mean the recurring schedule is empty.
- Represent buffers as open gaps unless the user explicitly wants buffer tasks.
- Keep one Morning focus and one Afternoon focus container by default. Split a
  focus task only when the user chooses that representation.
- Treat `references/system-baseline.md` as the current source of truth until the
  user changes it.

## Default Workflow

1. **Establish anchors.** Confirm local date/timezone, requested horizon, and
   whether the change affects recurring templates, one-off tasks, or both.
2. **Inventory first.** Query projects, existing tags, active and all-source
   tasks, recurrence links, generated instances, and parent/subtask structure.
3. **Preserve the system.** Reuse projects and tags by name. Preserve true
   deadlines, established routine anchors, intentional overlaps, and open gaps.
4. **Triage only when requested.** Route Inbox and stale work without turning a
   schedule change into an unsolicited full cleanup.
5. **Build reusable routines safely.** Create the parent and subtasks first,
   reorder and verify them, then make the parent recurring with subtask
   inheritance.
6. **Build the schedule.** Update recurrence start times for the reusable
   framework and `plannedAt` only for selected one-off work. Keep meal windows,
   breaks, transitions, and recovery space intact.
7. **Verify from fresh reads.** Do not rely on intended payloads or success
   responses alone. State fields the bridge cannot read back.

## Scheduling Defaults

- Keep recurring Work tasks as containers; choose concrete project work during
  Morning planning instead of assigning every backlog task a time.
- Preserve the current one-hour lunch, 90-minute dinner, movement breaks,
  evening anchors, and explicit open gaps.
- Prefer 15–30 minute estimates for checklist subtasks, 45–90 minutes for
  bounded work, and intentionally sized focus containers. Do not split a focus
  container merely because it is long.
- Reuse the existing compact tags. Create a new tag only for a demonstrated
  recurring filter need and with user approval.
- Do not turn open gaps into recurring completion obligations.
- Schedule all active work only when the user explicitly asks for full coverage.
- Include setup, context switching, review, and cleanup in estimates.

## Verification Contract

For a full overhaul, report:

- active task count including subtasks;
- active top-level task count;
- unscheduled active task count, separated into top-level tasks and children;
- Inbox active top-level count;
- stale and overdue counts for the anchor date;
- schedule horizon for top-level tasks and, when requested, all active tasks;
- the final recurring-day framework.

Distinguish direct evidence from bridge limitations. Recurrence writes can be
acknowledged while `startTime`, weekday flags, and subtask-inheritance settings
remain unavailable for readback. Verify `repeatCfgId`, estimates, projects,
tags, parent `subTaskIds`, and the next generated instance when possible. If a
check is nonzero or unknown, explain whether it is a defect, an expected child
record, intentionally deferred work, or an unverified field.
