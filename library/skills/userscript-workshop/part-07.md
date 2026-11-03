## Common Mistakes

- Missing `@grant` for APIs the script actually uses.
- Missing `@connect` for hosts used by `GM_xmlhttpRequest` or `GM_cookie`.
- Treating `@include` as a better default than `@match` for ordinary host targeting.
- Using DOM APIs inside ScriptCat background or cron scripts.
- Returning from a ScriptCat background script before async GM work is truly finished.
- Mixing `==UserScript==` and `==UserSubscribe==` packaging concepts.
- Putting `==UserConfig==` in the wrong place or reading config keys without the `group.key` name.
- Assuming Tampermonkey and ScriptCat storage, notification, or request behavior is identical.
