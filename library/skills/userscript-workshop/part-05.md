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
