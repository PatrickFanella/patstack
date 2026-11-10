# Super Productivity Planning Runbook

Use this runbook for broad or mutating planning passes. Read
`system-baseline.md` first when recurrence schedules, projects, tags, or reusable
routines are in scope.

## 1. Establish scope

Capture:

- local date and timezone;
- whether the request changes recurring templates, one-off work, or both;
- requested workday or weekend horizon;
- permission for recurrence changes, project/tag creation, deletion, archival,
  bulk completion, and other destructive actions;
- whether the user wants general work containers or specific tasks scheduled.

Use todos for a multi-step overhaul and include final verification from the
start. Do not turn a focused schedule adjustment into a full task cleanup.

## 2. Inventory the real system

Collect a read-only snapshot before mutation:

- bridge health and capabilities;
- projects and tags resolved by title;
- active top-level tasks and active subtasks;
- Inbox, overdue, stale, one-off planned, and unscheduled work;
- recurrence-linked tasks and generated instances;
- parent `subTaskIds`, estimates, tags, and tracked time;
- target-day and next-generated-day instances.

Query both active tasks and `source: all` with completed/archived records when
recurring Home or Personal Admin work is relevant. The bridge may expose a
recurrence only through a historical or future generated instance. Do not infer
that a project has no recurring templates merely because its active list is
empty.

If MCP calls fail, stop planning and switch to the `sp-mcp-doctor` mode.

## 3. Preserve scheduling semantics

- Recurrence `startTime` owns the reusable framework.
- Due dates own deadlines.
- `plannedAt` owns selected one-off placement.
- General Work focus tasks are containers. Choose their concrete project target
  during Morning planning.
- Open gaps are deliberate buffer, transition, lighter-work, or recovery space.
  Do not create recurring buffer tasks by default.
- Keep one Morning focus and one Afternoon focus task unless the user asks to
  split them. A movement break may sit at a boundary; do not manufacture
  continuation tasks automatically.
- Preserve intentional overlaps recorded in `system-baseline.md`.

When changing duration, recompute downstream collisions. Expanding a meal may
require shifting a focus block, movement break, Home reset, or practice routine.

## 4. Use minimal organization

### Titles and notes

- Preserve plain, recognizable titles such as Morning focus, Dinner, and Guitar
  practice. Do not impose category prefixes on routine containers.
- Add notes when they clarify scope, next action, fallback behavior, or what
  completion means.
- Omit frequency words when recurrence already expresses frequency.

### Estimates

- Use realistic estimates including setup, transition, review, and cleanup.
- Use 15–30 minutes for checklist steps and 45–90 minutes for bounded work.
- Permit intentionally larger focus containers. Split only by user preference,
  not a universal two-hour rule.

### Tags

- Resolve and reuse existing tags by title.
- Follow the mapping in `system-baseline.md`.
- Prefer one to two tags on framework tasks; retain additional health/movement
  tags only when they support a real view.
- Create a tag only after confirming a repeated filtering need and user intent.

### Projects

- Keep chronological anchors in Daily Routine.
- Keep Work containers in Work and weekly chores in Home.
- Do not move health-related anchors to Health & Care merely to populate it.
- Preserve Personal Admin periodic work and Guitar Practice material in their
  domain projects.

## 5. Build recurring routines with subtasks

For a checklist that must repeat:

1. Create or reuse the normal parent task.
2. Add atomic subtasks with notes and estimates.
3. Re-read the parent and reorder `subTaskIds` into the intended sequence.
4. Check the parent estimate and every new child's `timeSpent`. Some bridge/app
   combinations may copy the parent's historical tracked time onto the first
   newly created child or alter the parent estimate. Correct only impossible
   propagation and preserve genuine history.
5. Call `set_task_recurrence` on the parent with
   `shouldInheritSubtasks:true`. Do not make each child recurring.
6. Verify the parent `repeatCfgId`, ordered `subTaskIds`, estimates, tags, and
   the next generated instance.

If the parent is already recurring, inspect before creating anything. Never
duplicate a routine merely because the recurrence configuration is not readable.

## 6. Mutate conservatively

- Preview broad field changes with dry-run tools.
- Apply recurrence changes in coherent waves, then re-read affected tasks.
- Resolve names to IDs from the live instance; do not hard-code IDs in the
  skill or reports.
- Removing recurrence may leave the current task active without `repeatCfgId`.
  Report that orphan; do not delete or archive it without authorization.
- Treat `isAskToUpdateAllTaskInstances` as version-sensitive. Use the current
  tool contract and report whether the call updated the template, instances, or
  both.

## 7. Triage Inbox and stale work only when requested

For each Inbox task, decide whether it is active work, reference, routine, or
backlog. Preserve context, clarify the next action, assign an estimate, and move
or schedule it only within the user's stated scope. Preserve true deadlines when
moving stale planned work.

## 8. Verify honestly

- Recheck bridge health after mutation.
- Use fresh task reads rather than payloads or cached inventory.
- Verify recurrence links, projects, tags, estimates, parent/child order, and
  generated instances.
- Separate unscheduled top-level work from child tasks whose recurring parent is
  scheduled. Child records may legitimately lack dates.
- Do not claim recurrence `startTime`, weekday flags, or inheritance settings
  were read back when the bridge only acknowledged the write.
- Use `verification-checklist.md` before the final report.

Report the resulting recurring framework, changed fields, direct verification,
expected gaps, orphan tasks, and any intentionally deferred cleanup.
