# Transparent output

## Default built-in procedure

Transparent-image requests use built-in `image_gen` first. It has no true transparent-background control, so generate a removable chroma-key source and convert the key color to alpha locally.

1. Generate the requested subject on a perfectly flat solid chroma-key background.
2. Use `#00ff00` by default; use `#ff00ff` for green subjects and avoid `#0000ff` for blue subjects. Never choose a key color present in the subject.
3. Move or copy the selected source from `$CODEX_HOME/generated_images/...` into the workspace or `tmp/imagegen/`.
4. Run this skill's bundled helper (`$IMAGEGEN_SKILL` is the directory holding this skill's `SKILL.md`), not a project script:

```bash
python "$IMAGEGEN_SKILL/scripts/remove_chroma_key.py" \
  --input <source> \
  --out <final.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

5. Validate alpha channel, transparent corners, plausible subject coverage, and absence of key-color fringe. Retry once with `--edge-contract 1` for a thin fringe. Use `--edge-feather 0.25` only for visibly stair-stepped, non-shiny/non-reflective subjects.
6. Save project-bound PNG/WebP in the project; never leave a project-referenced transparent asset only under `$CODEX_HOME/*`.

Use this prompt clause:

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

## True native transparency fallback

Do not automatically switch to CLI `gpt-image-1.5 --background transparent --output-format png`. Ask first if the user requests true/native transparency, chroma-key removal fails validation, or the subject is complex: hair, fur, feathers, smoke, glass, liquids, translucent materials, reflective objects, soft shadows, realistic product grounding, or colors conflicting with practical key colors.

Explain that `gpt-image-2` does not support `background=transparent`, native transparency requires CLI `gpt-image-1.5`, and CLI needs `OPENAI_API_KEY`. A suitable confirmation is:

```text
This likely needs true native transparency. The default built-in path uses a chroma-key background plus local removal, but true transparency requires the CLI fallback with gpt-image-1.5 because gpt-image-2 does not support background=transparent. It also requires OPENAI_API_KEY. Should I proceed with that CLI fallback?
```
