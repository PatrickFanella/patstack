## Existing Inputs And Upgrades

Treat character art, generated images, standard or v2 atlases, contact sheets, and built-in pet art as first-class grounding inputs.

- Preserve user-provided art as a generation reference; do not assume it already has final cell geometry.
- For an existing valid 8x9 atlas, use it as the rows `0-8` intermediate after deterministic and visual validation, then generate rows `9-10` and package the result as v2.
- For an existing 8x11 atlas, preserve approved standard rows. If a look cell fails, correct the complete containing 8-frame row before deterministic reassembly. Never package a newly generated one-off repair cell beside cells from another generation.
- For a built-in pet, extract and use its atlas or neutral/idle cell as the canonical identity reference.
- Include every image that defines head shape, face, palette, markings, material, flame/ears/hair, props, or look mechanics in look-direction generation.
- When a renderer or source provides a dedicated neutral/front frame, pass it through `--neutral-cell`; otherwise use the approved idle/default frame. The 16 directional cells never treat `000` as neutral.
