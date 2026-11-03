---
name: pet-hatchery
description: "Use when creating, repairing, upgrading or validating a Codex app animated pet (v2 spritesheet atlas). Generation needs Codex's imagegen skill; validation and packaging run in any client."
---

# Codex v2 animated pets

Choose the requested operation before loading generation instructions:

- New pet or an explicitly requested v1-to-v2 upgrade: [creation stages](creation.md). Load the current stage only.
- Existing-pet repair: [repair](repair.md). Preserve good rows; do not restart the creation workflow.
- Look-direction generation or repair: [look-direction procedure](required-v2-look-direction-stage.md).
- Inspection, validation, or packaging: [validation](validation.md). Validation alone performs no image generation.

Use the installed imagegen skill for authorized visual generation. It ships with Codex (`.system/imagegen`); in Claude Code or OpenCode it is normally absent, so limit work there to planning, validation, packaging, and deterministic repair, and say that generation needs a Codex session. Keep character identity, approved references, source images, and manifest provenance recoverable. Use the bundled deterministic scripts for geometry and image assembly, not generated pictures of an atlas.

All script and reference paths are relative to this skill directory. Resolve available runtimes before using them. Scope generation, publishing, and final pet installation to the user's request.

Look rows must be coherent eight-frame row generations. Do not paste an individual repaired look cell into the final atlas. Preserve the approved cardinal basis, row ordering, and independent direction review. For detailed failure handling consult the look-direction procedure; ordinary repairs do not require its full generation pipeline.

## Shared acceptance contract


- Final atlas is PNG or WebP, exactly `1536x2288`, and based on `192x208` cells. The `1536x1872` standard atlas is intermediate-only.
- `pet.json` contains `spriteVersionNumber: 2`, the extended despill report has `ok: true`, and the packaged spritesheet passes `validate_atlas.py --require-v2` with the run's chroma key. These deterministic results close chroma QA; no separate visual chroma-fringe gate or image retry is allowed.
- Used cells are non-empty and unused cells are fully transparent.
- Atlas follows the row/frame counts in `references/animation-rows.md`.
- The four-cardinal strip has been deterministically extracted, its clipping report passes, and all four anchors are semantically approved before look-row generation.
- Both coherent look rows use `decoded/look-anchors-approved.png` as the direction basis, interpolate all intermediate directions as even 22.5-degree steps, and preserve the fixed clockwise order.
- Deterministic pose-group registration, post-registration final-cell edge diagnostics, and labeled per-direction semantic QA pass immediately on each coherent source row before final atlas assembly; blind horizontal-and-vertical axis QA runs after both rows exist.
- Contact sheet and per-row motion previews have been produced and inspected by a lightweight visual QA worker.
- A focused neutral-plus-16-directions QA sheet has been produced and inspected before packaging.
- A randomized unlabeled horizontal-and-vertical axis pair sheet has been classified by three isolated blind workers and combined by strict majority. Both cardinal pairs pass. `qa/direction-blind-validation.json` has `ok: true`, or a worker-level/intermediate failure has an accepted minor resolution in `qa/blind-review-resolution.json` backed by labeled and continuity evidence.
- Every expected direction has an explicit `pass`, `warning`, or `fail` semantic verdict with horizontal and vertical axis evidence where applicable; no wrong cardinal, labeled wrong-quadrant pose, or visible reversal remains.
- `qa/direction-semantics.json` records verdicts for all 16 directions from an independent visual QA worker or explicit user inspection, including review notes for accepted warnings.
- `qa/look-continuity.json` has been reviewed; metric warnings are acceptable when the normal-size ordered loop has no visible snap, pop, identity change, or semantic discontinuity.
- `qa/review.json` has no errors.
- Row-by-row review confirms the animation cycles are complete enough for the Codex app.
- Motion previews do not show unintended size popping, reversed directional cadence, or wrong row semantics.
- Look directions follow the fixed clockwise order and form a cohesive, readable loop at normal pet size. Cardinals must be unmistakable. Intermediate blind uncertainty is acceptable as a reviewed warning when labeled normal-size review confirms the intended direction and the loop does not reverse.
- Non-pixel styles are accepted when readable at pet size and consistent across rows.
- `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/pet.json` and `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/spritesheet.webp` are staged together for custom pets.
