# Coding challenge state contract

Resolve paths relative to the Ars Malefica vault root.

## Canonical surfaces

| State | Path |
|---|---|
| Thread map | `001 Projects/Threads/Programming/Programming MOC.md` |
| Practice policy | `001 Projects/Threads/Programming/Practice/Coding Challenge Practice System.md` |
| Learner evidence profile | `001 Projects/Threads/Programming/Practice/Learner Profile.md` |
| Stable active pointer | `001 Projects/Threads/Programming/Practice/Current Challenge Block.md` |
| Preserved block history | `001 Projects/Threads/Programming/Practice/Blocks/` |
| Longitudinal evidence | `001 Projects/Threads/Programming/Practice/Challenge Progress Ledger.md` |
| Challenge queue | `001 Projects/Threads/Programming/Practice/Challenge Library.md` |
| Attempt schema | `001 Projects/Threads/Programming/Practice/Challenge Attempt Template.md` |
| Language tracks | `001 Projects/Threads/Programming/Practice/Tracks/<Language> Track.md` |
| Puzzle set index | `001 Projects/Threads/Programming/Practice/Puzzle Sets/Puzzle Sets.md` |
| Puzzle set notes | `001 Projects/Threads/Programming/Practice/Puzzle Sets/Puzzle Set NN.md` |

The practice workspace is `/home/onnwee/Work/Lab/practice`: one folder per track
(`typescript/`, `go/`, `python/`) and `puzzles/set-NN/pNN-slug/<language>/` for
puzzle sets. The practice-coach app (`/home/onnwee/Work/Lab/practice-coach`)
reads these notes, writes puzzle set notes, and keeps a coach log at
`~/.local/state/practice-coach/coach-log.jsonl`.

Do not create an attempt or solution directory until a real challenge workspace
is chosen. Store a stable absolute path or repository-relative reference to code
evidence; do not copy entire repositories into the vault.

## Block identity

Every named block requires:

```yaml
block-id: unique-lowercase-id
status: active | complete | paused
phase: baseline | practice
started: YYYY-MM-DD
completed: YYYY-MM-DD | null
target-attempt-count: integer
target-language: language | pending
workspace: absolute path | pending
```

Attempt count is a planning aid, not an advancement gate. The stable pointer has
one `active-block` property and one wikilink to that block. Preserve history.

The pointer names the shared baseline block. After the baseline, each track
names its own block in its track note's `active-block`; the pointer's
`active-block` may then be left empty, but only when every track note names an
active block.

## Track identity

Every track note requires:

```yaml
track-id: typescript | go | python
language: TypeScript | Go | Python
toolchain: exact runtime and versions
workspace: absolute path to the track folder
active-challenge: challenge ID | pending
phase: baseline | practice
active-block: vault-relative block path   # optional during the shared baseline
```

and the sections `## Current state`, `## Dimensions` and `## Next instruction`.
A track's `Dimensions` table changes only from attempts in that language.

## Puzzle set identity

The index has an `active-set` property (empty before the first set) and a table
of sets. Every set note requires:

```yaml
set-id: set-NN
status: active | complete
workspace: absolute path to puzzles/set-NN
```

and the sections `## Puzzles`, `## Review` and `## Next set guidance`. A set is
`complete` only after its review has been approved and written. Puzzle sets do
not change track bands or count toward block gates.

## Evidence model

For each attempt record:

- date, block ID, challenge ID, prompt version, objective, and provenance;
- language, runtime/toolchain, workspace, and revision/diff or source path;
- permitted resources and highest assistance level used (`0` through `6`);
- commands run and exact outcome summary;
- correctness, edge cases, tests/debugging, clarity, and complexity observations;
- the learner's explanation and confidence assessment;
- one demonstrated strength, one limiting failure, and one intervention;
- `continue`, `narrow`, `vary`, or `advance`, with reason;
- one executable next instruction.

Do not collapse the baseline into a global beginner/intermediate/expert label.
Record each dimension as `not evidenced`, `guided`, `independent`, or `transfer`
with `low`, `medium`, or `high` confidence and direct evidence.

## Baseline completion

Require at least three reviewed attempts, including:

- one implementation from a behavioral contract;
- one debugging or failing-test diagnosis;
- one transfer task with altered surface details.

The same attempt may satisfy more than one category only when the evidence is
substantive. A passing result supplied by assistance level 5 or 6 cannot establish
independence. After baseline completion, create one successor focused on the
weakest goal-relevant dimension rather than every weakness at once.

## Challenge identity and safety

Use stable lowercase IDs such as `cc-baseline-debug-01`. Record the prompt before
the attempt and version material changes. Prefer original challenges. Attribute
external prompts and respect access and redistribution terms.

Never introduce destructive filesystem, production, credential, purchase, or
external-message actions as a surprise challenge. Keep practice work in a
dedicated workspace unless the user explicitly selects an existing repository.

## Common failure modes

- Inferring skill from years, titles, solved counts, or conversation.
- Giving a full solution before diagnosing the learner's bottleneck.
- Treating tests as complete proof of correctness.
- Counting assisted code as independent performance.
- Raising several difficulty axes at once.
- Counting evidence from one language toward another track.
- Letting puzzle results change a track's bands.
- Generating a puzzle that overlaps an active track challenge.
- Optimizing for speed, streaks, or challenge volume.
- Replacing the active pointer with history or overwriting completed blocks.
- Copying proprietary prompts or test suites into the vault.
