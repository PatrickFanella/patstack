# Review interface decisions in context

Research reviewed October 2, 2026. Use for requested reviews of generic or AI-looking interfaces. These are product-review heuristics, not evidence of who authored an interface.

## Inspect the task behind the screen

Identify the user's goal and the information needed to accomplish it before judging the styling. Inspect a representative journey when runtime access is available. With screenshots alone, limit conclusions to visible composition, copy, and states.

| Check | Evidence to inspect | Contextual recommendation |
|---|---|---|
| Substitution | Would the interface serve an unrelated product after replacing its logo and labels? | Use the domain's real objects, operations, and information priorities. |
| Priority | Do attractive profile details or generic metrics displace the main task? | Give the task and its prerequisites prominence; charts need a meaningful decision or monitoring purpose. |
| Grouping | Are unrelated facts equal-sized cards, or related facts separated by decoration? | Group according to relationships; select a list, table, document, or cards based on use. |
| Evidence | Are testimonials, metrics, imagery, and demo data attributable or identified as examples? | Flag unsupported claims without inventing proof or asserting fabrication from appearance. |
| Action contract | Do navigation, labels, and calls to action match what happens next? | Name the action and disclose material conditions where users need them. |
| Stress | What happens with empty data, loading, failure, permissions, long content, narrow screens, keyboard focus, and reduced motion? | Exercise relevant states and report observed failures; do not infer missing behavior from one screenshot. |
| Coherence | Do typography, spacing, color, iconography, and motion support understandable roles? | Adapt the existing system; novelty and random variation do not establish originality. |

Separate three kinds of finding:

- **Observed defect:** a failed interaction, unreadable contrast, misleading claim, or task obstruction supported by inspected evidence.
- **Contextual design concern:** a composition or default conflicts with the supplied task or brand. Explain the conflict and the proposed improvement.
- **Taste preference:** a stylistic alternative without demonstrated harm. Label it as optional.

Do not score “percent AI,” diagnose provenance from fonts/colors, or promise conversion improvements without measurement. Familiar components and standard navigation can improve usability. Preserve justified purple palettes, gradients, Inter, rounded cards, and stock components. Changing the palette alone does not repair missing product decisions.

## Evidence and its limits

- [NN/G, AI Prototyping in Real Design Contexts](https://www.nngroup.com/articles/ai-prototyping/), published October 2025, reviewed August 2026: a heuristic evaluation of a learner-profile redesign found inappropriate social-profile patterns, weak grouping, and hierarchy problems. Detailed context and artifacts improved outputs. This is evidence from one project, not proof that every generated app has these defects.
- [Anthropic, Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills): the developer describes unguided output converging on familiar fonts, colors, and layouts. This practitioner/vendor explanation is not a universal prevalence measurement or a known description of every model's training corpus.
- [HTTP Archive, 2025 Web Almanac](https://almanac.httparchive.org/en/2025/generative-ai#ai-fingerprints), published January 2026: tracked “AI colors” did not surge within identified Tailwind sites; wider-web growth accompanied Tailwind adoption. Tests found no statistically significant increases in the examined gradients, shadows, and fonts. CSS-variable detection missed hardcoded colors and variations. A purple palette is weak provenance evidence.
- [UI-Bench, September 2025 version](https://arxiv.org/html/2508.20410v3): expert comparisons across generated interfaces distinguished quality among tested tools. It lacked a human baseline and excluded accessibility, load time, and code quality from its stated scope. A visual ranking is not production qualification; do not turn tentative failure-mode discussion into measured defect prevalence.
- [NN/G, UX-Context Design, July 2026](https://www.nngroup.com/articles/ux-context-design/): curated user, domain, and design context guides generated interfaces. This supplies a practical rationale for giving a model task knowledge rather than only an aesthetic prompt.
- [Anthropic, Harness design, March 2026](https://www.anthropic.com/engineering/harness-design-long-running-apps): the developer reports generous self-evaluation and experiments with separate evaluation against concrete criteria. Review generation critically; this does not mandate subagents or authorize delegation.

These checks are original synthesis. They support review and implementation choices; they do not establish AI authorship or parity with human design.
