## Quick Reference

| Intent                               | Default choice                               | Watch for                                                                 |
| ------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------- |
| Page UI, DOM scraping, page patching | Portable `==UserScript==`                    | `@match`, `@grant`, `@run-at`, CSP-sensitive injection                    |
| Cross-origin API access              | `GM_xmlhttpRequest` with explicit `@connect` | Missing hosts, cookie behavior differences, user authorization            |
| Long-running worker                  | ScriptCat `@background`                      | No DOM, must return `Promise` for async work                              |
| Scheduled task                       | ScriptCat `@crontab`                         | Only first `@crontab` counts, prefer 5-field cron, avoid interval overlap |
| User-editable settings               | `==UserConfig==` plus `GM_getValue`          | Block placement and `group.key` naming                                    |
| Silent bundle install and updates    | `==UserSubscribe==`                          | HTTPS, `user.sub.js`, subscription `connect` overrides child scripts      |
