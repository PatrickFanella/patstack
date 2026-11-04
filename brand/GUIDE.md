# patstack brand guide

Direction: **A1 Rack + A3 Registration**, selected by the owner on November 3, 2026 from nine candidates. The masters, the full guide, the tokens and the direction study live in SUBCULT Studio (`subculture-collective/subcult-tv`, `studio/brands/patstack/` and `studio/studies/patstack-directions/`). The files in this folder are copies exported from Studio; `studio-assets.json` records the source revision and the SHA-256 of each one. Change the masters in Studio and rerun the export; do not edit the copies.

## What the system means

- **Rack units are the fleet.** Hosts and installed trees are drawn as rack units: ears, slot number, host name, role, lamp and a state label. The rack carries real deployment information, never decoration. The rows in the exported artwork are the fleet as recorded on 2026-11-03, after the Subsets category rebuild (PR #26) was verified on all six hosts; rebuild after the next verified deployment so they stay true.
- **Registered plates explain verify and drift.** Three offset plates stand for the installed tree, the plan (expected and desired trees) and the source tree. Registration means SHA-256 hashes, file modes and symlink targets agree. A misaligned plate is a refused apply.
- **Status labels are true.** `[ACTIVE]`, `[WARNING]`, `[VETO]` and `[ARCHIVE]` are semantic: color and text agree with the installer's real result. Never use a state color for emphasis.
- **Violet marks the tool, never a state.** It is the SUBCULT lineage cue in the mark block and the tag `A SUBCULT TOOL`.

## Color and type

| Token | Color | Use |
| --- | --- | --- |
| ground | `#100b19` | Pages, posters, the terminal |
| surface | `#1f1830` | Panels, rack bodies, code blocks |
| line | `#3b2470` | Rules, borders, the back plate |
| paper | `#f0ece4` | Text, rack units, the front plate |
| muted | `#a89fb8` | Secondary text; also the archive state |
| acid | `#00ff88` | The live signal: lit lamp, `[ACTIVE]`, the plan plate |
| violet | `#8b5cf6` | Lineage; large text only on the ground (4.58:1) |
| warning | `#f28c28` | `[WARNING]` |
| critical | `#ff4055` | `[VETO]` on the ground; `#d52032` on paper |

Oswald 700 uppercase for display and host names; Space Grotesk for body; JetBrains Mono for labels, paths and commands. Write `PATSTACK` only in the wordmark and display headings; `patstack` in prose. Spacing steps 8, 16, 24, 32, 48, 64, 96. Square corners. No texture outside posters.

## Using the files in this repository

| File | Use |
| --- | --- |
| `readme-banner.png`, `readme-banner.svg` | The README header |
| `repo-avatar.png` | The Gitea repository avatar (512×512) |
| `og.png` | Link preview (1200×630) |
| `favicon-64.png` | Small icon where one is needed |
| `mark-primary.svg`, `mark-light.svg`, `mark-mono-dark.svg`, `mark-mono-light.svg` | The mark for dark grounds, paper grounds and single-color uses |
| `lockup-primary-outlined.svg`, `lockup-light-outlined.svg` | Mark plus wordmark with text converted to paths; no font dependency |
| `tokens.json`, `tokens.css` | Color roles, measured contrast, type roles, state table, motif rules |

Mark clear space is one quarter of its height; minimum size 32 pixels, mono below 24. Minimum lockup width 220 pixels; use the mark alone below that. Do not stretch, rotate or add effects.

patstack has no web application. Its surfaces are this repository, documentation pages if they are ever published, the terminal and occasional posters. Documentation uses the ground, paper text, rack units for hosts, the plates for the verify diagram and real commands in code blocks; it never shows web buttons for actions that do not exist. The installed Omarchy `subcult` theme already carries this palette in the terminal.

## Before publishing anything

Selection is not publication. A public post should check whether host names belong in it, replace sample copy, verify claims against the README and `docs/OPERATING-MODEL.md`, and carry alt text that describes the finished image. Setting the Gitea avatar or link preview is a separate, reversible action.
