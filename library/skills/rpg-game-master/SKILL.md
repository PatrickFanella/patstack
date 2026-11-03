---
name: rpg-game-master
description: "RPG game master: run a tabletop or solo narrative RPG session with scene management, NPC portrayal and story continuity."
metadata:
  blacktower-pack: creative
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: worldbuilding-fiction,game,facilitator
---

# rpg-game-master

Run or design tabletop/narrative game facilitation. Use merged D&D/game-master content as a reference, not a separate active skill.

## Workflow

1. Use this skill only when the request matches the frontmatter description.
2. Keep the main context short: read only the relevant reference file for the exact subtask.
3. Prefer existing scripts/templates/assets in this skill before writing ad hoc code. Scripts are Deno programs (`deno run --allow-read ...`). Deno is not installed on the fleet by default; `mise exec deno -- deno run ...` runs one without a global install.
4. Stop and ask when required credentials, CLIs, project context, or user confirmation are missing.

## Resources

- `references/full-guide.md` — detailed guidance.

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/game-master.md` — Game Master guidance.
