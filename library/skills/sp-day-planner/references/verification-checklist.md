# Super Productivity Planning Verification Checklist

Use this checklist before declaring a planning pass complete.

## Data integrity

- [ ] Bridge health succeeded after mutation.
- [ ] Fresh reads, not intended payloads, supplied verification evidence.
- [ ] Every intended write returned success; partial failures are reported.
- [ ] No project or tag was created without a demonstrated need and user intent.
- [ ] No task was deleted, archived, or bulk-completed without authorization.
- [ ] Genuine tracked time and deadline history were preserved.

## Scheduling semantics

- [ ] Recurrence start times are used for reusable anchors.
- [ ] Due dates remain deadlines and `plannedAt` remains one-off placement.
- [ ] An empty `plannedAt` range was not mistaken for an empty recurring day.
- [ ] Meal, break, transition, practice, Home reset, and evening collisions were
      recomputed after duration or start-time changes.
- [ ] Open gaps remain gaps unless the user requested explicit buffer tasks.
- [ ] Focus containers remain unsplit unless the user chose splitting.
- [ ] Removing recurrence did not silently leave an unwanted active one-off; any
      orphan is reported.

## Recurrence evidence

- [ ] Affected tasks have the expected `repeatCfgId`.
- [ ] Projects, tags, titles, notes, and estimates match fresh reads.
- [ ] The next generated instance was inspected when available.
- [ ] `startTime`, weekday flags, and subtask-inheritance claims are labeled as
      write-acknowledged when the bridge cannot read them back.
- [ ] Stale `dueWithTime`, due-day, or current-instance fields are not presented
      as proof that a template write failed or succeeded.

## Recurring parent/subtask routines

- [ ] The parent existed before recurrence was added.
- [ ] Parent `subTaskIds` match the intended child set and order.
- [ ] Children are atomic, estimated, and not independently recurring.
- [ ] The parent estimate is correct after child creation.
- [ ] Newly created children did not inherit impossible historical `timeSpent`.
- [ ] `shouldInheritSubtasks:true` was requested and the next generated parent
      instance was checked when possible.

## Minimal organization

- [ ] Existing tags were resolved by title and reused.
- [ ] Framework tasks generally use one or two useful tags.
- [ ] No near-duplicate taxonomy was introduced.
- [ ] Daily Routine, Work, Home, Personal Admin, Health & Care, and Guitar
      Practice boundaries remain intentional.

## Coverage and hygiene

- [ ] Active unscheduled counts are split into top-level and child tasks.
- [ ] Child tasks lacking dates under a scheduled recurring parent are described
      as expected structure, not loose work.
- [ ] Complete-coverage claims are made only when the user requested them.
- [ ] Inbox-zero, overdue-zero, stale-zero, and all-active scheduling claims are
      verified individually when in scope.
- [ ] Intentionally deferred one-off work and untouched projects are reported.

## Final report

For a full overhaul, include:

- active tasks including subtasks;
- active top-level tasks;
- unscheduled top-level and child counts;
- active top-level Inbox count;
- stale and overdue counts for the anchor date;
- top-level schedule horizon and, if requested, all-active horizon;
- the resulting recurring-day framework;
- direct verification, write-only acknowledgements, remaining orphans, and
  intentionally deferred cleanup.

If a field cannot be read, report it as unverified rather than complete.
