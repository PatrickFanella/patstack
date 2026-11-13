---
name: studio-brand-audit
description: "Studio brand audit. Use to check a SUBCULT product's site or promo assets against its selected Studio brand pack, verify fixes, or repair drift. Not for choosing a new direction (create-subcult-branding)."
---

# Studio brand audit

Check whether an implementation and its artwork agree with the selected system. Work from the active `subcult-tv` checkout and the explicitly targeted product repository or site. Read their project instructions and `studio/AGENTS.md`; inspect Git status before generating evidence or fixes.

## Choose the mode

- **Audit:** inspect and report discrepancies without changing the selected identity.
- **Verify fixes:** revisit specified findings against the changed sources and rendered result.
- **Audit and repair:** apply requested repairs to the owning sources, rebuild the affected exports and verify them.

A review request authorizes inspection and a report. A request to repair authorizes scoped fixes. Selecting a replacement system belongs to `create-subcult-branding`; preparing product integration belongs to `studio-brand-handoff`. Use interface and accessibility review skills where relevant.

## Resolve the baseline

Read `studio/brands/README.md`, the target pack's `GUIDE.md`, tokens, selection records, source provenance and manifest. Resolve whether Studio or the product repository owns interface rules; read `WEBSITE.md` and product design docs where applicable. Use the current selection and preserved masters, not archived proposals. Compare the implemented revision with the documented observation date.

Read `studio/content/VOICE.md` and the claims register when copy is in scope. Do not apply the umbrella's colors or voice to every product. Promotional and interface systems may intentionally differ; report an intentional documented difference separately from a defect. If the baseline conflicts or lacks a decision, record a specification gap and continue.

## Inspect representative surfaces

Choose representative pages, states and asset sizes for the scope. Use the client's browser tools; record URL, viewport, states and captures. Keep local, deployed and screenshot-only observations distinct; source inspection never stands in for rendered proof.

For a deployed site, run [the live-site checks](references/live-site-checks.md). Compare marks and variant selection, font loading and fallback, semantic colors and contrast, hierarchy, spacing, layout, responsive wrapping, image/crop treatment, navigation and relevant focus/error/empty/loading states. Inspect small icons and phone-sized promotional exports. Verify copy against product evidence. Check asset hashes, licenses and obsolete references that affect current consumers.

Report banned-default matches (`create-subcult-branding`, `style-web-ui`): defects in new work, optional in packs selected before 2026-11-13. Measure contrast pairs and keyboard/focus behavior in scope. Avoid blanket defects based on decorative artwork or rules for a different surface. Check generator/master ownership before proposing an export fix; never edit a derivative PNG to hide a generator problem.

## Report or repair

Place a scoped report under `studio/studies/reviews/<dated-audit>/`, or the owning product's review location. Each actionable finding needs: affected file/URL and state, observed behavior, expected rule with source, practical impact, evidence, proposed fix and owning repository. Rank by impact; separate verified defects, specification gaps and optional improvements. Include representative passing behavior so no findings is not mistaken for no inspection.

If repairing, preserve owner-edited masters, change only the affected sources, regenerate their exports and update manifests/provenance together. Run relevant product checks and `make check-studio check-studio-automation` for Studio changes. Verify fixed states and exports again. Do not silently replace the selected direction or deploy a site as an audit step.

Finish with the report, prioritized findings, inspected scope, checks and limitations. An audit is complete when each finding is supported and routed to an owner. A fix is verified only for the source, render and runtime boundaries actually checked.
