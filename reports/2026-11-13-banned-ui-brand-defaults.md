# Banned UI and brand defaults

The owner asked on 2026-11-13 for overused generated-interface and generated-brand patterns and fonts to be banned, within reason, in the UI and branding skills. This reverses the 2026-10-02 rule in `style-web-ui` that familiar fonts and effects were "not forbidden signs of AI authorship" (see `2026-10-02-writing-design-research-acceptance.md`).

## Changes

| Owner | Change |
|---|---|
| `style-web-ui` | New `references/banned-defaults.md`: fonts, typographic treatments, color, layout, components, motion, icons, imagery and interface copy, each with the condition that allows it. The entrypoint links it from Defaults, adds a pre-edit check (the missing workflow step 3) and a checklist line, and tells the agent to drop dataset or preset suggestions that hit the list. |
| `create-subcult-branding` | New `references/banned-defaults.md` for type, palettes, marks and promotional imagery, with the selected-pack exception. Linked from the entrypoint, the Select step in `workflow.md`, and stages 2 and 6 of `product-launch.md`. |
| `studio-brand-audit` | Reports matches: a defect in new work, an optional finding in a pack selected before 2026-11-13. Other sentences were tightened to stay under the 4,000-character body limit without changing their meaning. |

"Within reason" is implemented as three exceptions: an existing brand or selected pack keeps its choices, an owner decision that names the item wins, and listed functional uses stay allowed (system stack for dense product UI body text, monospace for code and data, numbering for real sequences, glass on one layered surface, dark themes for dark-first products). Bans never support a claim that a page was AI-generated.

Sources, revisions and hashes are in `catalog/research-review-2026-11-13.json`. The lists are original synthesis; no upstream prose was copied.

## Acceptance scenarios

Manual walk-throughs against the final instructions, not model-session trials.

| Scenario | Expected decision |
|---|---|
| Build a new landing page with no brand: the first plan uses Inter, an indigo gradient hero and three icon cards | Step 3 flags all three; the agent replaces them from the product's subject and records the choices. |
| Restyle a settings screen in an app whose design system already uses Inter | Keep Inter; mention the match in the report; no font change. |
| Owner brief says "cream background, terracotta accent, serif headings" | Follow the brief; record the owner decision as the reason. |
| Code block and CLI flags rendered in JetBrains Mono | Allowed: monospace for code. |
| Launch board for a new product whose best reference uses Space Grotesk | The board's OFL substitute comes from outside the list; the collision is listed under Recommendation and collisions. |
| Audit the SUBCULT umbrella site, which uses Space Grotesk from its selected pack | Optional finding for the owner, not a defect; no change. |
| Draw a mark for an AI-assisted product: first idea is a gradient circle with a sparkle | Rejected by the mark list; the mark comes from the product's own material. |
| Someone asks whether a site was made by AI because it uses a purple gradient | The lists do not establish authorship; offer a design review instead. |

## Checks

- `python3 -B scripts/validate.py`: no errors.
- `python3 -B -m unittest discover -s tests`: 149 tests pass.
- skill-creator `quick_validate.py` on the three changed skills: valid.

Not done here: Subsets bundle build and fleet deployment, and the `subcult-tv` project selection that installs `studio-brand-audit`.
