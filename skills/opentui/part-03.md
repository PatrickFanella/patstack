## How to Use This Skill

### Reference File Structure

Framework references follow a 5-file pattern. Cross-cutting concepts are single-file guides.

Each framework in `./references/<framework>/` contains:

| File | Purpose | When to Read |
|------|---------|--------------|
| `REFERENCE.md` | Overview, when to use, quick start | **Always read first** |
| `api.md` | Runtime API, components, hooks | Writing code |
| `configuration.md` | Setup, tsconfig, bundling | Configuring a project |
| `patterns.md` | Common patterns, best practices | Implementation guidance |
| `gotchas.md` | Pitfalls, limitations, debugging | Troubleshooting |

Cross-cutting concepts in `./references/<concept>/` have `REFERENCE.md` as the entry point.

### Reading Order

1. Start with `REFERENCE.md` for your chosen framework
2. Then read additional files relevant to your task:
   - Building components -> `api.md` + `components/<category>.md`
   - Setting up project -> `configuration.md`
   - Layout/positioning -> `layout/REFERENCE.md`
   - Keyboard/input handling -> `keyboard/REFERENCE.md`
   - Animations -> `animation/REFERENCE.md`
   - Troubleshooting -> `gotchas.md` + `testing/REFERENCE.md`

### Example Paths

```
./references/react/REFERENCE.md           # Start here for React
./references/react/api.md              # React components and hooks
./references/solid/configuration.md    # Solid project setup
./references/components/inputs.md      # Input, Textarea, Select docs
./references/core/gotchas.md           # Core debugging tips
```

### Runtime Notes

OpenTUI runs on Bun and uses Zig for native builds. Read `./references/core/gotchas.md` for runtime requirements and build guidance.
