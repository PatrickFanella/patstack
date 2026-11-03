---
name: raster-image-gen
description: "Raster image generation: create or edit bitmap images (photos, sprites, textures, transparent cutouts) with Codex image_gen or the OpenAI CLI fallback. Not for SVG, icons or code-native visuals."
---

# Image Generation Skill

Generate or edit raster assets for the current project: photos, illustrations, textures, sprites, mockups, wireframes, logos, and infographics.

## Trigger and boundaries

Use for new bitmap assets, bitmap edits, reference-guided variants, and transparent-background cutouts. Do not use for an established SVG/vector/logo system, simple code-native diagrams or shapes, editable native source assets, or deterministic code-native output.

## Core mode rules

- Built-in `image_gen` exists only in Codex, which also ships its own system `imagegen` skill. In Claude Code or OpenCode, say that only the CLI fallback is available and use it on an explicit request.

- Use built-in `image_gen` by default for generation, edits, and simple transparency requests; it does not need `OPENAI_API_KEY`.
- Use `scripts/image_gen.py` only when the user explicitly requests CLI/API/model controls, or explicitly confirms the true-transparency fallback. It requires `OPENAI_API_KEY`; never create a one-off SDK runner or modify the script.
- Never silently downgrade to CLI `gpt-image-1.5`. Explain and obtain confirmation unless the user already explicitly requested `gpt-image-1.5`, the script, or CLI fallback.
- A request for many assets or the word “batch” alone stays on the built-in path: make one call per distinct asset or variant. CLI `generate-batch` is only for an explicitly chosen CLI workflow.
- If built-in generation is unavailable, say that CLI fallback exists and requires `OPENAI_API_KEY`; proceed only on an explicit request.

## Workflow

1. Choose built-in mode by default; choose CLI only under the rules above.
2. Classify the request as **generate** or **edit**. A supplied style/composition reference is generation; a request to preserve and change parts of an image is an edit. If a built-in edit target is local-only, view it with `view_image` first.
3. Collect the prompt, verbatim text, constraints/avoid list, intended destination, and inputs. Label every input as a reference, edit target, or supporting/compositing input.
4. Shape a concise prompt, preserving detailed user requirements and adding only useful detail. See [prompting guidance](references/prompting.md) and [sample prompts](references/sample-prompts.md).
5. Generate or edit. For edits, state invariants and preserve them on every iteration. Inspect subject, style, composition, text, and constraints; iterate with one targeted change.
6. Handle transparency using the built-in-first procedure in [transparent output](references/transparent-output.md).
7. For project-bound work, move or copy the selected final artifact into the workspace and update consumers. Do not overwrite an existing asset without explicit permission; otherwise use a versioned sibling filename. Preview-only output may remain under `$CODEX_HOME/generated_images/...` and render inline.
8. Report final saved path(s), final prompt(s), and whether built-in or CLI mode was used.

## Guardrails

- Do not claim arbitrary filesystem-path editing through built-in `image_gen`; it edits images visible in conversation context.
- Do not substitute SVG/HTML/CSS for explicitly requested raster assets. Prefer repo-native vector/code assets when the request is an icon, logo, or UI graphic that must match them.
- Do not treat CLI-only controls (`quality`, `input_fidelity`, masks, output format, output paths) as built-in tool arguments.
- Never leave a project-referenced asset solely in `$CODEX_HOME/*`.
- Never ask the user to paste an API key; ask them to set `OPENAI_API_KEY` locally and confirm.

## Reference routing

- [Prompting guidance](references/prompting.md): prompt structure, specificity, input roles, invariants, iteration, taxonomy, and use-case advice.
- [Sample prompts](references/sample-prompts.md): copy/paste asset recipes.
- [Transparent output](references/transparent-output.md): built-in chroma-key procedure, validation, and confirmed native-transparency fallback.
- [CLI fallback](references/cli.md): `scripts/image_gen.py` commands and examples.
- [Image API reference](references/image-api.md): CLI model, size, quality, mask, and output parameters.
- [Network setup](references/codex-network.md): CLI network/sandbox troubleshooting.
- `scripts/image_gen.py`: fallback-only implementation; load/use only after CLI is explicitly selected.
- `scripts/remove_chroma_key.py`: bundled helper for built-in transparent-image post-processing.
- `assets/`: presentation metadata icons; they are not generation inputs.
