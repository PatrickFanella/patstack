# Control UI

Use local browser automation to verify UI behavior with evidence. First reuse the repo's own Playwright, browser, or Electron harness if it exists; otherwise assemble a temporary local harness around the app's dev server or Chromium debug port.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Setup Pattern

1. Start the app locally using the repo's documented dev command.
2. Discover existing local harnesses: Playwright tests, Cypress specs, Storybook, browser scripts, Electron launch scripts, or snapshot tools.
3. For a web app, connect to the local URL with the existing browser tooling.
4. For Electron/Chromium, enable a remote debugging port when supported.
5. Select the correct page by stable app markers, not by tab order alone.
6. Prefer accessibility roles, labels, and stable `data-*` selectors over coordinates.

## Interaction Loop

1. Capture a page snapshot or screenshot before acting.
2. Choose a target from the latest page structure.
3. Perform exactly one structural action: click, type, keypress, drag, scroll, navigate, or resize.
4. Capture a fresh snapshot/screenshot.
5. Verify the expected state change.
6. Save artifacts for before/after comparisons when the user asked for proof.

## Guardrails

- Do not rely on stale element references after navigation or structural changes.
- Avoid coordinate clicks unless a fresh screenshot was captured immediately before the click.
- Keep test data local and disposable.
- Do not store screenshots or heap snapshots from privacy-sensitive workspaces unless the user explicitly agrees.
- Do not hard-code selectors, ports, or script paths from another repository. Discover the current repo's local app markers.
- Do not add Playwright or other browser tooling as a project dependency for a probe unless the user asks. Prefer existing dev dependencies or browser tools already in the environment.
- Clean up dev servers, debug sessions, and temp profiles when done.

## Read when needed

- [Generic web harness](part-04.md): read when the repo has Playwright but no reusable probe for a web app.
- [Generic CDP harness](part-05.md): read when driving Electron or a Chromium app through `--remote-debugging-port`.
- [CDP capabilities](part-07.md): read when higher-level browser APIs cannot do the performance, memory, network, rendering or debugging work.
- [Page selection](part-08.md): read when several windows or tabs share one debug port.
