---
name: ars-malefica-inbox-intake
description: Route inbox items to their canonical vault destinations following the Ars Malefica conventions. Use when triaging the inbox, processing captured clippings/articles/PDFs, intaking a large batch of new material, or cleaning up 000 Inbox. Knows the Resources-and-Threads boundary, the Sources/Raw-vs-Research-vs-Notes split, and the Media directory structure.
---

# Ars Malefica Inbox Intake

Read the inbox, classify every item, suggest a destination, and execute moves with
user confirmation. Follow the conventions in `Resources and Threads.md` and the
Inbox routing guide.

## Read first

1. `references/state-contract.md` for the canonical vault surfaces.
2. The vault's `003 Resources/Systems/Resources and Threads.md` for the boundary
   rules and routing table.
3. `000 Inbox/Inbox.md` for the current inbox contents and triage prompts.

## Workflow

### 1. Inventory the inbox

Read `000 Inbox/` fully — every file and subdirectory. Group items by type:

- **Loose files** (markdown, images, PDFs, unknown)
- **Clippings** (in `Clippings/`, excluding `Clippings Queue.md`)
- **Directory trees** (multi-file packages like courses, archives, project dumps)

### 2. Classify each item

Apply the triage prompts from Inbox.md:

> - What is the smallest stable home for this?
> - Is this a source, a thought, a theme, or an output?
> - Does it need a new note, or should it attach to an existing Thread/Work/Resource?
> - Is there a claim or question hiding inside it?
> - What link would make this easier to rediscover later?

Then map to the routing table:

| If the item is... | Route to... |
|---|---|
| Lived experience, daily context, mood, timestamped reflection | `003 Resources/Periodic Notes/` |
| Source primarily serving one inquiry | that Thread's `Sources/Raw/` or `Sources/Research/` |
| General book, article, video, podcast, recipe, plant note, reference | `003 Resources/Media/<medium>/` |
| Ongoing question, theme, synthesis, research arc | `001 Projects/Threads/` |
| Output, artifact, draft, software, post, release | `001 Projects/Works/` |
| Ongoing responsibility or standard | `002 Areas/` |
| Runbook, system note, template, operational memory | `003 Resources/Systems/` |
| Public or self-standing documentation | `001 Projects/Works/Documentation/` |
| No longer useful | delete or `004 Archives/` |

### 3. Present the plan

For each item, show:
- Current path
- Proposed destination with rationale
- Any wikilink fixes needed after the move
- Items recommended for deletion with justification

Group by destination. Ask for confirmation before any moves.

### 4. Execute moves

Move files to their canonical destinations. When moving into an existing
Thread's Sources directory:

- Raw captured material → `Sources/Raw/`
- Structured analysis of that material → `Sources/Research/`
- Your own interpretations and ideas → `Notes/`
- Reusable developed concepts → `Concepts/`
- Claims or models → `Synthesis/`

After moves, fix any broken absolute-path wikilinks in the moved files. Run a
grep for the old path and verify zero remaining references.

### 5. Clean up

- Remove empty inbox directories.
- Delete `.DS_Store` files.
- Verify `000 Inbox/` contains only `Inbox.md` and `Clippings/Clippings Queue.md`
  (plus gitignored reference material the user intends to keep).

## Bulk video/media handling

When an inbox directory contains video or large binary files (mp4, mov, mp3,
sqlite3):

1. Identify text/knowledge content (markdown, PDF study materials, JSON
   manifests) — route these normally.
2. Identify reference media — move outside the vault to
   `/home/onnwee/Videos/` or the appropriate external path.
3. Never stage video or large binary files for git. Update `.gitignore` if
   residual directories will remain.

## Guardrails

- Keep one canonical copy. Use `threads` metadata links, not file duplication.
- Do not move files the user is currently editing.
- Do not touch `.obsidian/`, `.git/`, or other hidden vault infrastructure.
- Prefer archive over deletion for ambiguous items.
- When routing a clipping, check whether it already exists in the destination.
- Do not route licensed/paid material into git-tracked paths without explicit
  user confirmation of rights.