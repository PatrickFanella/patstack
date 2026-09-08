## Preflight

- Confirm the manager and browser. On Manifest V3 browsers, ScriptCat may require `Allow User Scripts` or browser developer mode before scripts run.
- Decide page script versus background script before writing code. ScriptCat background scripts cannot touch the DOM.
- Start with metadata, not implementation: `@match`, `@grant`, `@connect`, `@run-at`, and any update URLs.
- Prefer portable `==UserScript==` patterns for ordinary page scripts. Only switch to ScriptCat-only headers when the requested behavior actually needs them.
