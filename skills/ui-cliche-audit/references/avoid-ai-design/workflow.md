# Review generic design patterns

Use this procedure for a requested AI-look audit, or from `ui-craft` when
implementing or correcting frontend visuals. The imported resources come from
`funboy322/avoid-ai-design` v0.4.0 at commit
`2b7c71836b06cdf6b3d73265b56490c1b75ad5aa` under MIT; the notice is in
`../../notices/avoid-ai-design-MIT.txt`. The source repository's
`catalog/avoid-ai-design-intake-2026-11-04.json` records hashes and adaptations.

## Select the mode

- **Audit:** inspect and report. Do not change product files, add ignore
  comments, generate `DESIGN.md`, or install hooks.
- **Implement:** only within an authorized UI implementation or repair task,
  use `ui-craft` to plan, edit, and verify the changes. Continue routine,
  reversible work within that scope without another approval pause.

The original upstream entrypoint is archived outside discovery. This adapted
procedure keeps the stack's existing audit and implementation owners.

## Scope and scan

1. Read the requested components or pages and the existing brand rules,
   tokens, `DESIGN.md`, and sibling pages. State the page's primary task.
2. If Node 18+ is available, run the scanner on explicit files or directories:

   ```sh
   node <skill-root>/scripts/detect.mjs --json <target-path>
   ```

   Here `<skill-root>` is the loaded `ui-cliche-audit` directory. From
   `ui-craft`, resolve the sibling `ui-cliche-audit` installation first. If it
   is unavailable, use the existing design checklist and report that limit.

   Exit `2` means P0/P1 patterns were found; it is a completed scan with
   findings. Exit `1` is an error. Exit `0` means no reported P0/P1 patterns;
   inspect `scanned` and the findings too. Zero files is an inconclusive scan.
   The scanner can silently skip unreadable or missing paths and swallow rule
   errors, so its exit status alone cannot establish complete coverage.
3. Read the relevant categories in [the pattern catalog](ai-tells-catalog.md).
   It covers common defaults and the replacement defaults, including cream
   with terracotta, near-black with lime, decorative numbering, and repeated
   mono/all-caps labels. A match identifies source syntax to examine; it does
   not establish that the choice is unjustified or that AI produced the UI.
4. Inspect rendered pages and interactions through the current client's
   permitted browser workflow when available and allowed for the task. Do
   not open a browser contrary to client instructions. Mark visual claims
   without a render as inferred, and untested behavior as unverified.

## Interpret findings

For each actionable finding, give the file/line or visible location, rule ID
when present, observed evidence, product impact, and a specific correction.
Separate scanner priorities P0/P1/P2 from verified accessibility or usability
defects. A deliberate brand color, readable system font, status label, real
sequence, or data table can be correct even when a heuristic flags it.

The scanner honors `avoid-ai-design-ignore: ID` on a line or the preceding
line, and `avoid-ai-design-ignore-file: ID1, ID2` for a file. It skips example
folders and `slop-example` content unless `--include-examples` is passed.
In implementation mode, use narrow ignores only for a documented deliberate
choice. Do not suppress findings merely to obtain a clean score. The
upstream scanner is advisory here; this intake adds no automatic CI gate.

## Implement and check

Use the existing design system as the direction. Where none exists, derive
type, colors, layout, motion, and a distinctive detail from the product's
audience, content, and real artifacts. [Aesthetic directions](aesthetic-directions.md)
supplies vocabulary after that decision, not a preset menu. Check the plan
against both sets of defaults before editing.

Keep the component's props, state, routing, data flow, copy meaning, and
accessibility requirements. For multiple pages, extend the project's existing
design documentation; create a filled-in `DESIGN.md` only when the task needs
one and no contract exists. [The template](design-md-template.md) is optional
reference material; its placeholders must be replaced before delivery. Its
third-party CLI commands are not required and have not been qualified here.

Re-scan the same scope after changes and explain remaining deliberate choices.
Verify the rendered result and main interaction when permitted. Report scan,
visual, interaction, and accessibility evidence separately. A clean scanner
result alone does not prove a good design or working behavior.
