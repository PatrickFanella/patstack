# Banned defaults

Research reviewed 2026-11-13; sources and limits are at the end. These are the fonts, palettes and patterns that generated interfaces reach for whatever the product is. They make a page look like every other generated page, so do not introduce them.

## When a banned item is allowed

- **The brand already has it.** An existing design system, product UI or selected Studio pack keeps its fonts, colors and components. Do not replace them as a side effect of other work; mention the match in the report so the owner can decide.
- **The owner asked for it.** A brief or owner decision that names the font, color or pattern wins.
- **It does a job listed beside it below.** Record that job in the token file, design note or PR description.

Swapping a banned item for its neighbor on the same list is not a fix. Choose from the product's subject, audience and material, then check the choice against this page again.

## Fonts

Do not pick these as a new typeface for a brand, a marketing page or display type:

- Inter, Inter Tight and Inter Display.
- Roboto, Arial, Helvetica or the system stack as the only face.
- Geist and Geist Mono left in place from the Next.js starter.
- Space Grotesk, Syne, Sora and Cal Sans: the "designed-looking" free sans set.
- Instrument Serif, Fraunces and Playfair Display as the display serif over a sans body: the cream-editorial set.
- Space Mono or JetBrains Mono as a label or heading face.

Allowed:

- A system stack, or the brand's own sans, for body text in dense product UI such as dashboards, admin screens and forms, where speed and native rendering matter. Headings and the brand surfaces still use a chosen face.
- Monospace for code, commands, keys and tabular data a reader scans.

Before shipping, confirm that every family the CSS names has an `@font-face` rule or a font-host link, and check the rendered page. A face that never loads leaves visitors on the fallback.

## Typographic treatments

- One word or phrase in a headline set apart by italic, color, weight, a highlighter or a gradient. This includes the serif-italic word in a sans headline.
- Tracked all-caps eyebrow labels above headings. Allowed when the label carries information the heading lacks; set it in sentence case.
- Metadata joined with middle dots (`A · B · C`) and labels built as `WORD — fragment`.
- A `→` glyph appended to link and button text.
- Decorative `01 / 02 / 03` numbering. Allowed for a real sequence: steps, a timeline, a ranking.
- Gradient-filled heading text.

## Color

- An indigo or violet to blue gradient, and indigo or violet primary buttons.
- Emerald or teal as the lone accent on a neutral page when the brand did not ask for green.
- A warm cream ground (near `#F4F1EA`) with a terracotta or clay accent (near `#D97757`) and a high-contrast serif. The cream-serif-sage variant counts too.
- A near-black ground (`#0B0B0B` to `#111`) with one acid-green, lime or vermilion accent.
- Dark mode shipped as the only theme without a reason, especially with medium-grey body text and a purple accent. Allowed for night use, media, monitoring and other dark-first products, themed as a full palette.
- Colored glow shadows under cards and buttons.
- Primary and accent within about 20 degrees of hue: one color pretending to be two.

A gradient built from the brand's own colors, with a job, is allowed. Body text below 4.5:1 is an accessibility defect, not a style choice.

## Layout

- The template hero: pill badge, centered headline, centered subhead and two centered buttons over a three-card row. Centering alone is fine; the full kit is banned.
- A row of three or six identical cards, each with an icon in a tinted rounded square, a short title and one line of text.
- A bento grid whose tile sizes do not encode importance.
- A band of round numbers ("10,000+ users · 99.9% uptime · 4.9★"), logo walls of companies that are not customers, and testimonials without a source.
- The stock section order: hero, logos, features, how it works, testimonials, stats, pricing, FAQ, call to action, footer. Order sections by what this audience needs to decide.
- Three pricing cards with a "Most popular" ring on the middle one, when the real offer has a different shape.
- A four-column footer with a newsletter box and social icons that the site does not need.
- Fake window chrome (traffic-light dots, a generic terminal) as the hero image. Show the real product.
- Every section in the same `max-w-7xl mx-auto` container.

## Components

- shadcn/ui or another kit shipped with its default base color, `--radius` and unstyled Card, Button and Badge.
- The same large radius and soft grey shadow (`rgba(0,0,0,.1)`) on every surface, and a hairline grey border around every card.
- A colored stripe on the left or top edge of cards.
- Glass (`backdrop-blur`) panels. Allowed on one surface where layering is real, such as a sticky nav over scrolling content.
- Cards nested inside cards.
- Badges and status chips with no real state behind them.
- Effect-library pieces dropped in as shipped: spotlight, beams, meteors, shimmer buttons, 3D tilt cards, number tickers, marquees, sparkles.
- The `zinc-950` card with a `white/10` border as the default dark surface.

## Motion

- The same fade-and-rise entrance on every section, and a hover transition on every card. Use one orchestrated moment instead.
- Bounce and elastic easing on interface motion. Allowed for a playful brand that chose it.
- Count-up number animations.
- Any motion without a `prefers-reduced-motion` path.

## Icons and imagery

- The sparkle (✦ or Lucide `Sparkles`) as the sign for AI, and the stock Lucide set (`Zap`, `Rocket`, `Shield`, `ArrowRight`) in a feature-card row.
- Emoji standing in for icons in navigation or feature lists.
- Glossy 3D blobs, abstract gradient orbs and generated "diverse team at a laptop" photos.
- Corporate Memphis people: flat, faceless, long-limbed figures.
- Placeholder avatars from avatar services, and an empty `aspect-video` box where a screenshot belongs.
- Generator leftovers: `lovable-tagger`, v0, Bolt or Lovable meta tags.

## Copy in the interface

Interface copy follows `write-plainly`. These patterns appear often enough in generated pages to name here:

- Headlines that could front any product: "Build the future of work", "Your all-in-one platform", "Supercharge your workflow".
- Three-adjective slogans: "Faster. Smarter. Simpler."
- Buttons that say "Get started", "Learn more" or "Submit" where a specific action exists. Name the action and keep the verb through the flow.

## Check before handing over

1. List every font, color, radius, shadow and motion token. Mark each one that appears above and give its allowed reason or replace it.
2. Ask whether the same plan would come out for a similar product. If yes, it is still a default.
3. Judge combinations. One eyebrow label on an otherwise authored page is minor; cream, serif italic, all-caps labels and decorative numbering together is the template.
4. Compare pages of the same product side by side. Every page uses the same tokens, nav and footer.

## Sources and limits

- Anthropic, [frontend design skill](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/frontend-design/SKILL.md), commit `41bbe19` (2026-09-03): the five clusters (cream and terracotta, near-black and one accent, broadsheet, SaaS card kit, template chrome), the typographic treatments and the motion defaults.
- Adrian Krebs, [Scoring Show HN submissions for AI design patterns](https://adriankrebs.ch/blog/design-slop/) (2026-04-20): 16 DOM checks over 1,590 Show HN pages, 22% matched four or more. The author reports 5–10% false positives, and the sample leans toward solo, AI-built projects.
- J. Carter Johnson, [vibecoded-design-tells](https://github.com/JCarterJohnson/vibecoded-design-tells): about 3.2 million Reddit posts mined for named tells. shadcn/Tailwind defaults and the purple gradient rank highest; bento, glass and aurora backgrounds rank low; it also names the cream-serif-sage default.
- [avoid-ai-design](https://github.com/funboy322/avoid-ai-design/tree/2b7c71836b06cdf6b3d73265b56490c1b75ad5aa) v0.4.0 (MIT), retained in this repository under `archive/removed-skills-2026-11-09/ui-cliche-audit/`, for the fuller catalog with detection notes and its source list.
- [Laith0003/ux-skill anti-slop ban list](https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list) and [Creative Boom, 10 trends creatives are over in 2026](https://www.creativeboom.com/insight/10-trends-creatives-are-so-over-in-2026/), for practitioner agreement on fonts, gradients and glass.
- Counter-evidence: the [HTTP Archive 2025 Web Almanac](https://almanac.httparchive.org/en/2025/generative-ai) found no statistically significant rise in the examined gradients, shadows and fonts across the wider web. These bans exist to keep SUBCULT work distinct, not to detect AI authorship. Never claim a page was generated because it uses one of them.

The lists above are original synthesis. Retrieval hashes are in `catalog/research-review-2026-11-13.json`.
