# Current Super Productivity System

Read this file before changing recurring schedules, projects, tags, or reusable
routines. Treat user-provided corrections and the live interface as newer than
this baseline.

## Scheduling semantics

- Recurrence `startTime` defines reusable daily and weekly anchors.
- Due dates represent deadlines.
- `plannedAt` places one-off tasks. An empty `plannedAt` schedule does not mean
  the recurring day is empty.
- Leave buffers as open gaps, not tasks.
- Keep one Morning focus and one Afternoon focus task unless the user chooses to
  split them. Removing recurrence may leave an active one-off task behind.

## Weekday framework

| Time | Duration | Task |
|---|---:|---|
| 08:00 | 30m | Morning reset |
| 08:30 | 20m | Choose one nice thing |
| 08:30 | 25m | Fuel up |
| 08:55 | 15m | Wake up the body |
| 09:10 | 15m | Morning planning |
| 09:25 | 30m | Morning admin |
| 09:55 | 65m | Morning focus |
| 11:00 | 5m | Morning water and movement break |
| 11:05–12:30 | open | Work or buffer; no continuation task by default |
| 12:30 | 60m | Lunch away from work |
| 13:30 | 120m | Afternoon focus |
| 15:30 | 5m | Afternoon water and movement break |
| 15:35–16:30 | open | Buffer or lighter work |
| 16:30 | 15m | Afternoon regroup |
| 16:45 | 30m | Wrap up |
| 17:15–17:45 | open | Buffer |
| 17:45 | 45m | Walk or bike |
| 18:45 | 90m | Dinner |
| 20:15 | 15m | Home reset |
| 20:30 | 45m | Guitar practice |
| 21:15–23:20 | open | Personal time |
| 23:20 | 20m | Evening reset |
| 23:55 | 5m | Go to bed |

The 08:30 overlap is intentional: Choose one nice thing can happen while Fuel
up is underway. Preserve it unless the user asks to separate them.

## Projects

- `Daily Routine`: chronological personal anchors.
- `Work`: recurring admin, focus, regroup, and wrap-up containers.
- `Home`: weekly chores; do not consume Work focus blocks by default.
- `Health & Care`: available for future health-domain work; do not move routine
  anchors merely to fill the project.
- `Personal Admin`: weekly/monthly/quarterly/yearly reviews and commitments.
- `Guitar Practice`: the recurring practice parent and current music work.

Weekly Home chores currently include garbage Monday, bathroom Tuesday, floors
Wednesday, plants Thursday, dust Friday, dishes Saturday, and laundry plus
sheets Sunday. Keep weekend load visible and do not turn weekdays into overflow.

## Minimal tag system

Reuse existing tags by title; never hard-code IDs.

- Work container: `Routine`
- Focus container: `Routine`, `Focus`
- Planning/regroup/wrap: `Routine`, `Planning`
- Meals: `Routine`, `Meals`
- Movement: `Routine`, `Health`, `Movement`; add `Quick` only when useful
- Home reset/chores: `Routine`, `Chores`; add `Quick` only when useful
- Guitar practice: `Routine`, `Focus`

Do not create `Admin`, `Shutdown`, `Focus Block`, or other near-duplicate tags
without a demonstrated filter need and user approval.

## Recurring routines with subtasks

Use this sequence:

1. Create or reuse a normal parent task.
2. Create its subtasks with estimates and notes.
3. Reorder the subtasks and re-read the parent.
4. Correct any accidental estimate or tracked-time propagation.
5. Make the parent recurring with `shouldInheritSubtasks:true`.
6. Verify `repeatCfgId`, parent `subTaskIds`, order, estimates, and the next
   generated instance. Do not make each child independently recurring.

Guitar practice is the working example: target 2m, warm-up 5m, vocabulary 8m,
weekly technique 10m, application 15m, and record/review 5m. Its notes contain
a 15-minute fallback.

## Bridge evidence limits

The current bridge can write recurrence start times and weekday settings but
does not reliably read those configuration fields back. `dueWithTime`, due
dates, or generated instances may remain stale after editing an existing
template. Report acknowledged writes separately from verified current fields.
