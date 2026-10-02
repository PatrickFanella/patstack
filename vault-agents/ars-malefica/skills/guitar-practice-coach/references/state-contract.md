# Guitar practice state contract

## Canonical vault surfaces

Resolve all paths relative to the Ars Malefica vault root.

| State | Path |
|---|---|
| Thread map | `001 Projects/Threads/Guitar/Guitar MOC.md` |
| Practice policy | `001 Projects/Threads/Guitar/Practice/Guitar Practice System.md` |
| Stable active pointer | `001 Projects/Threads/Guitar/Practice/Current Practice Block.md` |
| Preserved block history | `001 Projects/Threads/Guitar/Practice/Blocks/` |
| Longitudinal evidence | `001 Projects/Threads/Guitar/Practice/Practice Progress Ledger.md` |
| Source queue | `001 Projects/Threads/Guitar/Practice/Practice Material Library.md` |
| Session log schema | `001 Projects/Threads/Guitar/Practice/Practice Log Template.md` |
| Local lesson artifacts | `001 Projects/Threads/Guitar/Practice/Materials/` and `001 Projects/Threads/Guitar/Tabs/` |
| Country Guitar Online archive | `001 Projects/Threads/Guitar/Sources/Raw/Country Guitar Online/` |
| ArtistWorks Bluegrass Rhythm Toolkit | `001 Projects/Threads/Guitar/Sources/Raw/ArtistWorks/` |
| External lesson videos | `/home/onnwee/Videos/ArtistWorks/` and `/home/onnwee/Videos/Country Guitar Online/Free Lessons/` |

The stable pointer contains one `active-block` property and one wikilink to the
named active block. Completed blocks remain named files; do not turn the pointer
into the historical record.

## Block identity

Every named block requires:

```yaml
block-id: unique-lowercase-id
status: active | complete | paused
started: YYYY-MM-DD
completed: YYYY-MM-DD | null
target-session-count: integer
```

Session count is a planning aid, not an advancement gate.

## Weekly ledger evidence

Record:

- date range and block ID;
- full and floor session counts;
- exact source, fragment, and measure/pattern range;
- starting, clean working, and optional tested-maximum tempo;
- BPM subdivision and whether the clean-pass rule was met;
- memory or cue-map status;
- recording path and take purpose, or `not recorded`;
- timing/tone, tension/coordination, and harmony/phrasing observations;
- pain, numbness, or persistent-tension flag;
- one improvement and one limiting failure;
- the selected intervention;
- `continue`, `narrow`, `vary`, or `advance`, with reason;
- one executable next instruction: tempo, fragment, and listening criterion.

At block end, additionally record every completion-test result, each material
disposition, and the next-block rationale.

## Recording contract

Do not require recordings to live inside the vault. Store a stable path or URI
and label the take `baseline`, `weekly`, `midpoint`, or `final`. State what the
take is intended to demonstrate. Do not create an empty Recordings directory.

## Super Productivity discovery

Find the project by exact title `Guitar Practice`; verify its live ID rather than
assuming an old ID. Read the daily parent, subtasks, review tasks, and recurrence
configs before mutation. Keep the stable pointer link in recurring notes so
future blocks do not require replacing the URL everywhere.

Use dry-run-first bulk updates for broad task changes. Read tasks back after
mutation. Recurring reminders are allowed; Codex automations are out of scope.

## Failure modes

- Advancing by calendar or task completion instead of evidence.
- Logging the fastest accidental tempo as the working tempo.
- Writing vague feedback without passage, tempo, symptom, and intervention.
- Adding several new technical problems or sources at once.
- Treating missed days as a failed week rather than resuming the sequence.
- Losing a recording's path or purpose.
- Guessing attribution for user-authored study files.
- Treating pain or numbness as a speed problem.
- Overwriting completed blocks or breaking ledger links.
