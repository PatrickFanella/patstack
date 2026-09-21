---
name: vscode-extension-development
description: Implement and review VS Code extension contribution points, commands, menus, when-clause visibility, and localization. Use when changing an extension's package.json contributions or user-facing strings; do not use for ordinary application commands or general translation work outside a VS Code extension.
compatibility: Requires a VS Code extension project; validate against the project's engines.vscode range and current official Extension API documentation.
metadata:
  blacktower-pack: integrations
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: vscode extension,command contribution,menu visibility,when clause,extension localization,package nls,l10n bundle
---

# VS Code Extension Development

Use one workflow for extension manifest contributions and localization so a
new command does not ship with mismatched visibility, enablement, or strings.

## Workflow

1. Inspect `package.json`, `engines.vscode`, activation code, existing command
   IDs, contribution points, localization files, and extension tests.
2. Keep command IDs stable and namespace new IDs to the extension. Declare
   user-facing commands under `contributes.commands` and register their
   implementations in extension code.
3. Put each command only in the intended surfaces. Use menu `when` clauses for
   visibility and command `enablement` for whether the command can execute
   across menus and keybindings.
4. Reuse established context keys and menu groups. Add a custom context key only
   when built-in keys cannot express the state, and update it explicitly.
5. Localize manifest strings through `%key%` entries backed by
   `package.nls.json` and locale variants. Localize runtime strings through
   `vscode.l10n.t` with the extension's configured localization bundles.
6. Check every supported locale for missing or stale keys. Preserve placeholder
   names and argument ordering.
7. Run the extension's compile, lint, unit, and Extension Host tests. Exercise
   Command Palette visibility, target menus, disabled states, and at least one
   non-default locale when localization changed.

## Guardrails

- Do not hide a command only in its handler; commands can be invoked from APIs,
  keybindings, and other extensions.
- Do not use menu visibility as a substitute for execution-time validation of
  security- or trust-sensitive conditions.
- Do not invent naming conventions that conflict with the current project.
- Verify version-sensitive contribution properties against the declared
  `engines.vscode` range.

## Current references

- [Contribution points](https://code.visualstudio.com/api/references/contribution-points)
- [Commands guide](https://code.visualstudio.com/api/extension-guides/command)
- [When-clause contexts](https://code.visualstudio.com/api/references/when-clause-contexts)
- [VS Code localization API](https://code.visualstudio.com/api/references/vscode-api#l10n)
