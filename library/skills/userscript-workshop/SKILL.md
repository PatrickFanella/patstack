---
name: userscript-workshop
description: "Userscripts: build or debug browser userscripts, covering page lifecycle, injection, manager permissions and update behavior. Not for full browser extensions."
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: backend-architecture,develop,userscripts
---

# userscript-workshop

Userscript implementation and debugging: page lifecycle, browser permissions, injection, and update behavior.

Userscript work usually breaks at the runtime and metadata boundary, not in the page logic. Choose the runtime first, declare the minimum permissions up front, then debug in the environment where the script actually runs. This covers Tampermonkey and ScriptCat userscripts, not full browser extensions or browser automation outside userscript managers.

## Preflight

- Confirm the manager and browser. On Manifest V3 browsers, ScriptCat may require `Allow User Scripts` or browser developer mode before scripts run.
- Decide page script versus background script before writing code. ScriptCat background scripts cannot touch the DOM.
- Start with metadata, not implementation: `@match`, `@grant`, `@connect`, `@run-at`, and any update URLs.
- Prefer portable `==UserScript==` patterns for ordinary page scripts. Only switch to ScriptCat-only headers when the requested behavior actually needs them.

## Workflow

1. Choose the runtime and metadata first.
2. Declare the smallest permission surface that fits the task.
3. Implement against the runtime you chose.
4. Debug where the code really runs.
   - Foreground scripts: page console plus manager logs.
   - ScriptCat background scripts: run log first, then `background.html` for real-environment debugging.
5. Publish with the right update model.
   - Normal scripts: keep `@version` accurate and add `@updateURL` or `@downloadURL` only when needed.
   - Subscription bundles: use `==UserSubscribe==`, HTTPS URLs, and subscription-level `@connect`.

## Common Mistakes

- Missing `@grant` for APIs the script actually uses.
- Missing `@connect` for hosts used by `GM_xmlhttpRequest` or `GM_cookie`.
- Treating `@include` as a better default than `@match` for ordinary host targeting.
- Using DOM APIs inside ScriptCat background or cron scripts.
- Returning from a ScriptCat background script before async GM work is truly finished.
- Mixing `==UserScript==` and `==UserSubscribe==` packaging concepts.
- Putting `==UserConfig==` in the wrong place or reading config keys without the `group.key` name.
- Assuming Tampermonkey and ScriptCat storage, notification, or request behavior is identical.

Read only the [task guide](guide.md) entries whose trigger matches the work.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.
