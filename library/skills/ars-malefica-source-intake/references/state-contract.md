# Source intake state contract

## Canonical vault surfaces

| Surface | Path |
|---|---|
| Media index | `003 Resources/Media/Media Index.md` |
| Resources and Threads boundary | `003 Resources/Systems/Resources and Threads.md` |
| Threads index | `001 Projects/Threads/Threads Index.md` |

## Medium directories

| Medium | Path | MOC |
|---|---|---|
| Articles | `003 Resources/Media/Articles/` | none yet |
| Books | `003 Resources/Media/Books/` | `Books MOC.md` |
| Clips | `003 Resources/Media/Clips/` | none yet |
| Courses | `003 Resources/Media/Courses/` | none yet |
| Films | `003 Resources/Media/Films/` | none yet |
| Games | `003 Resources/Media/Games/` | `Games MOC.md` |
| Music | `003 Resources/Media/Music/` | none yet |
| Podcasts | `003 Resources/Media/Podcasts/` | none yet |
| Social Posts | `003 Resources/Media/Social Posts/` | none yet |
| YouTube | `003 Resources/Media/YouTube/` | none yet |

## Catalog card frontmatter (full schema)

```yaml
type: resource
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
medium: <articles|books|clips|courses|films|games|music|podcasts|social-posts|youtube>
source: <URL>
author: <name>
published: <YYYY-MM-DD>
started: <YYYY-MM-DD>
finished: <YYYY-MM-DD>
rating: <1-5>
threads:
  - "[[Thread Name]]"
tags:
  - domain/media
  - medium/<medium>
  - topic/<topic>
title: <Title>
```

## Minimal MOC template

When a medium directory has its first content entry, create a minimal MOC:

```yaml
type: moc
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - domain/media
  - topic/<medium>
---
# <Medium> MOC

> [!abstract] Curated map of <medium> notes. Use for meaning; use Media Index for lists.

## Entries

- [[Title]]
```

## Boundary check

Before creating a catalog card, verify the source passes the reusable-across-Threads test:
- Would it still be findable and useful if every Thread changed?
- If YES → catalog card in Resources/Media/
- If NO → suggest routing to the owning Thread's Sources/Raw/