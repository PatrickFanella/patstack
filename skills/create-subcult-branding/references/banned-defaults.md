# Banned brand defaults

Reviewed 2026-11-13. A new direction, pack or round may not use the type, palettes, marks or imagery below. They are what generated brands and interfaces converge on, and a SUBCULT product wearing them looks like every other generated launch. Product sites built in Launch mode also follow the interface list in `style-web-ui` (`references/banned-defaults.md` in that skill).

## Exceptions

- **Selected packs keep their choices.** A pack selected before this date that uses a listed font or color keeps it until the owner reopens that part of the identity. Do not change it as a side effect; list the match in the board or audit so the owner can decide. As of the 2026-10-11 local Studio checkout, Space Grotesk is in SUBCULT, Backline, Patrick__Eff, Rekolekt and Subsets; Inter in Tadooer and Patrick__Eff; Inter Tight in HasanAra; Fraunces in Patchwork; Space Mono in Subcult OS.
- **The owner names it.** An owner decision that names the font, color or motif wins. Record it in the selection record.
- **The product's own material supplies it.** A color or form taken from the product's real artifacts (its interface, the hardware it imitates, the archive it serves) is not a default. Record the source.

Swapping one listed item for its neighbor is not a new direction. Each candidate on a board states, per axis, where the choice came from.

## Type

Not as the display face, wordmark face or the pack's only face:

- Inter, Inter Tight, Inter Display, Roboto, Arial, Helvetica, or the system stack.
- Geist and Geist Mono.
- Space Grotesk, Syne, Sora and Cal Sans.
- Instrument Serif, Fraunces and Playfair Display paired with a plain sans body.
- Space Mono and JetBrains Mono, except for code and data in the product's own UI.

When a reference uses one of these, the board's OFL substitute must come from outside the list.

## Palettes

- Indigo or violet into blue, as a gradient or a primary.
- Cream (near `#F4F1EA`) with terracotta or clay (near `#D97757`), with or without sage.
- Near-black with one acid-green, lime or vermilion accent.
- Emerald or teal as the only accent on neutrals.
- A primary and an accent within about 20 degrees of hue.
- Medium-grey text on near-black with a purple accent.

## Marks

- A circle with a gradient, radiating curves and a central opening: the shape many AI company logos now share.
- The four-point sparkle (✦) or a sparkles cluster.
- Robot heads, brains, circuit traces and neural-network nodes.
- Rockets, gears and globes as the whole idea.

The mark must also pass the existing 16-pixel test and differ from every sibling pack's mark.

## Imagery and promotional layouts

- Glossy 3D blobs, gradient meshes and plastic abstract shapes.
- Corporate Memphis people.
- Generated stock scenes such as a smiling team around a laptop.
- Fake window chrome or a generic terminal standing in for the product.
- The mark, the name and one tagline centered on a gradient: use the pack's signature scene.

## Sources

Anthropic's [frontend design skill](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/frontend-design/SKILL.md) (commit `41bbe19`), [Krebs's Show HN study](https://adriankrebs.ch/blog/design-slop/), the [vibecoded-design-tells](https://github.com/JCarterJohnson/vibecoded-design-tells) Reddit study and the archived avoid-ai-design catalog supply the type and palette lists. For marks: [VelvetShark on AI company logos](https://velvetshark.com/ai-company-logos-that-look-like-buttholes) describes the gradient-circle pattern; [NN/g](https://www.nngroup.com/articles/ai-sparkles-icon-problem/) found users could not say what the sparkle means, and [Studio Output](https://www.studio-output.com/thought/when-did-ai-brands-become-just-a-sparkle/) covers its spread; [Sologo](https://www.sologo.ai/blog/12-common-startup-logo-mistakes--optimization) names rockets, gears and globes. Apart from the NN/g study, this is commentary, not measurement. Hashes are in patstack's `catalog/research-review-2026-11-13.json`.
