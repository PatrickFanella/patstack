# Browser diagnosis

Use for an actual rendered-state claim, an existing debugging session, or a failure that a static fetch cannot explain. For ordinary public document retrieval, use the available search/fetch tools.

**Choose the existing owner.** Prefer a purpose-built connector or API for semantic operations on its resources. For page work, follow the active client's browser instructions. In T3, try preview_status, open the preview if needed, and use snapshot locators. A closed preview or an actionable argument error is not proof that the browser is unavailable. Use another browser system only under the client's stated fallback conditions. Reuse authenticated Chrome state when specifically required and permitted by those conditions. Do not launch a new backend merely because an optional CLI is installed.

**Preserve debugging context.** When the user already has a broken page, selected element or selected request, inspect that session first. Use the selection only if the tool actually exposes it. Otherwise re-anchor from a fresh page snapshot; do not invent access to DevTools state. Reproduce only the smallest transition needed when the selection is stale or the current evidence is insufficient.

**Inspect the rendered failure.** A static soft 404, login wall, rate limit or anti-automation response may differ from the user's browser. Verify the final URL, visible error, authentication state and affected action. Do not infer working controls from a successful page-open call. If the tool lacks the needed capability, report that specific limit.

**Find the actual interactive element.** Start with accessible names and snapshot-provided refs. For missing controls, inspect whether an iframe, Shadow DOM, collapsed region or lazy loading owns them. Expand or wait for the relevant state and refresh the snapshot. Use supported DOM inspection to identify a candidate when necessary, then use the tool's supported interaction path. Do not infer a selector-to-ref bridge, inject event handlers, or mutate the DOM as a substitute for the action being tested. Refresh stale refs after navigation or rerendering; bound retries and report persistent failure.

**Separate action from outcome.** For a Dashboard or CMS task, read current state, execute the authorized change, wait for the visible response, and reopen/read back the saved object. A click, toast or preview does not establish publication. Report saved, scheduled, published and delivered separately, with the relevant provider/object evidence. Reuse existing approval; ask only when the actual action or destination remains unresolved or requires new authority.

**Keep observations scoped.** Use console or network evidence when the visible state cannot explain the failure and the host exposes those surfaces. Do not collect unrelated tabs, requests, credentials or personal data. Coordinate browser ownership when another authorized worker uses the same session; do not close their tabs or navigate their active page.

Finish with the observed page/action, expected and actual result, evidence location, and remaining capability or environment limits. Media loading requires actual rendering or playback evidence, not only a URL or HTTP status.
