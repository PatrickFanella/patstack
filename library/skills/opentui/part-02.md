## Critical Rules

**Follow these rules in all OpenTUI code:**

1. **Use `create-tui` for new projects.** See framework `REFERENCE.md` quick starts.
2. **`create-tui` options must come before arguments.** `bunx create-tui -t react my-app` works, `bunx create-tui my-app -t react` does NOT.
3. **Never call `process.exit()` directly.** Use `renderer.destroy()` (see `core/gotchas.md`).
4. **Text styling requires nested tags in React/Solid.** Use modifier elements, not props (see `components/text-display.md`).
