# Inbox intake state contract

## Canonical vault surfaces

Resolve all paths relative to the Ars Malefica vault root.

| Surface | Path |
|---|---|
| Inbox root | `000 Inbox/` |
| Inbox routing guide | `000 Inbox/Inbox.md` |
| Clippings queue | `000 Inbox/Clippings/Clippings Queue.md` |
| Resources and Threads boundary | `003 Resources/Systems/Resources and Threads.md` |
| Media index | `003 Resources/Media/Media Index.md` |
| Threads index | `001 Projects/Threads/Threads Index.md` |
| Works index | `001 Projects/Works/` |
| Archives | `004 Archives/` |
| External video storage | `~/Videos/` on Kvant; confirm the path on other devices |

## Medium directories in Resources/Media

| Medium | Path | Has content |
|---|---|---|
| Articles | `003 Resources/Media/Articles/` | scaffold |
| Books | `003 Resources/Media/Books/` | active |
| Clips | `003 Resources/Media/Clips/` | scaffold |
| Courses | `003 Resources/Media/Courses/` | scaffold |
| Films | `003 Resources/Media/Films/` | scaffold |
| Games | `003 Resources/Media/Games/` | active |
| Music | `003 Resources/Media/Music/` | scaffold |
| Podcasts | `003 Resources/Media/Podcasts/` | scaffold |
| Social Posts | `003 Resources/Media/Social Posts/` | scaffold |
| YouTube | `003 Resources/Media/YouTube/` | scaffold |

## Thread Sources directory split

- `Sources/Raw/` — unprocessed captures (clippings, PDFs, articles)
- `Sources/Research/` — structured analysis of sources (claim audits, evidence registers, case matrices)
- `Notes/` — your own ideas, interpretations, working thoughts
- `Concepts/` — reusable distinctions developed from multiple sources
- `Synthesis/` — claims or models ready to guide future work

## File types that should never enter git

- Video: mp4, mov, mkv, avi, webm
- Audio: mp3, wav, flac
- Databases: sqlite3, db
- Large binaries: anything > 50MB
