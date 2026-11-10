# Base procedure

Reviewed source clients: claude, codex, opencode.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# Super Productivity Maintenance

## Overview

Coordinate a high-level Super Productivity maintenance pass without mixing
runtime diagnostics, task planning, and review work into one blob. Use this
skill as the router and runbook for deciding which focused Super Productivity
workflow should own each lane.

## Skill Boundaries

Use the three-procedure split deliberately:

- The `sp-mcp-doctor` mode — MCP health, development, bridge reliability,
  protocol smoke tests, tool/resource catalog drift, install/config issues.
- This base procedure — high-level periodic upkeep, system audit,
  routing, scope control, and final maintenance report.
- The `sp-day-planner` mode — task hygiene, inbox triage, estimates,
  minimal tags, overdue/today/unscheduled cleanup, recurring daily frameworks,
  and one-off task planning.

If the request is entirely one lane, load the focused mode and do not keep
this maintenance wrapper in the foreground.

## Maintenance Workflow

1. **Clarify the maintenance goal.** Establish date, timezone, desired horizon,
   whether live task mutation is allowed, and whether the user wants a light
   audit or a full overhaul.
2. **Health gate the MCP.** If any Super Productivity call fails, stalls, or
   reports missing tools/resources, switch to the `sp-mcp-doctor` mode before
   modifying data.
3. **Inventory the system.** Collect projects, tags, current task, active tasks,
   inbox tasks, overdue tasks, one-off planned work, and recurring routines.
   Check active data and the all/done/archive views because recurrence-linked
   Home and Personal Admin instances may be absent from the active list.
4. **Route the work.** Use the `sp-day-planner` mode for any mutation pass
   that touches task hygiene, estimates, tags, inbox, or scheduling. Keep this
   skill responsible for scope, priorities, and final reporting.
5. **Preserve slack.** Unless explicitly told otherwise, maintenance should not
   fill every open minute. Leave room for miscellaneous work, recovery,
   interruptions, and routines.
6. **Verify before reporting.** Do not claim the system is clean until targeted
   checks prove the requested invariants.

## Safety Rules

- Treat Super Productivity as a live personal operating system, not a test
  fixture. Prefer reversible changes.
- Ask before deleting tasks, bulk-completing tasks, changing recurring
  templates, or creating broad new taxonomy surfaces.
- Avoid hard-coded project or tag IDs. Resolve names to IDs from the current
  instance before writing.
- Preserve three distinct scheduling concepts: recurrence start times for the
  reusable daily framework, due dates for deadlines, and `plannedAt` for
  one-off placement. Do not call the recurring schedule empty merely because a
  `plannedAt` range is empty.
- Use todos for multi-step maintenance passes and include the final
  verification task from the start.

## Standard Output

Return a compact maintenance report with:

- scope and anchor dates used;
- lanes executed and any focused skills used;
- important changes made;
- verification results, including remaining known gaps;
- the next schedule or next recommended maintenance pass.

If the pass was intentionally partial, say what was not touched.
