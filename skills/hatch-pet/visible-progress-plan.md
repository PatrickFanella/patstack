## Visible Progress Plan

For every pet run, keep a visible checklist so the user can see where the work is up to. Create the checklist before starting, keep one step active at a time, and update it as each step finishes.

Use this checklist for every v2 pet run, replacing `<Pet>` with the pet's name or `your pet`:

1. Getting `<Pet>` ready.
2. Imagining `<Pet>`'s main look.
3. Picturing `<Pet>`'s poses.
4. Hatching `<Pet>`.

What each step means:

- `Getting <Pet> ready.` Choose or confirm the pet name, description, source images, style preset, style notes, and working folder. For bare brand/product/company requests, first run the brand discovery worker and capture the compact brand brief, source URLs, and avatar seed.
- `Imagining <Pet>'s main look.` Generate the pet's main reference image. This becomes the visual source of truth.
- `Picturing <Pet>'s poses.` Generate and approve rows `0-8`, write the pet-specific look mechanics plan, then generate rows `9-10`. Only mirror `running-left` if `running-right` clearly works when flipped.
- `Hatching <Pet>.` Assemble the 8x11 atlas, review standard motion plus all 16 look directions, fix every failed cell or row, package `spriteVersionNumber: 2`, and report the output paths.

Only mark a step complete when the real file, image, or decision exists. If this is a repair run, start from the first relevant step instead of restarting the whole checklist.
