## Workflow

### Step 1: Check for Existing State

**First, check if `.blacktower/codemap.json` exists in the repo root.**

If it does not exist, check for legacy state at `.blacktower/cartography.json`.

If legacy state exists: move `.blacktower/cartography.json` to `.blacktower/codemap.json`, then continue with change detection.

If `.blacktower/codemap.json` exists: Skip to Step 3 (Detect Changes) - no need to re-initialize.

If neither file exists: Continue to Step 2 (Initialize).

### Step 2: Initialize (Only if no state exists)

1. **Analyze the repository structure** - List files, understand directories
2. **Infer patterns** for **core code/config files ONLY** to include:
   - **Include**: `src/**/*.ts`, `package.json`, etc.
   - **Exclude (MANDATORY)**: Do NOT include tests, documentation, or translations.
     - Tests: `**/*.test.ts`, `**/*.spec.ts`, `tests/**`, `__tests__/**`
     - Docs: `docs/**`, `*.md` (except root `README.md` if needed), `LICENSE`
     - Build/Deps: `node_modules/**`, `dist/**`, `build/**`, `*.min.js`
   - Respect `.gitignore` automatically
3. **Run codemap.mjs init**:

```bash
node <skill-root>/scripts/codemap.mjs init \
  --root ./ \
  --include "src/**/*.ts" \
  --exclude "**/*.test.ts" --exclude "dist/**" --exclude "node_modules/**"
```

This creates:
- `.blacktower/codemap.json` - File and folder hashes for change detection
- Empty `codemap.md` files in all relevant subdirectories

4. **Delegate codemap writing to Fixer agents** - Spawn one fixer per folder to read code and create or update its specific `codemap.md` file.

### Step 3: Detect Changes (If state already exists)

1. **Run codemap.mjs changes** to see what changed:

```bash
node <skill-root>/scripts/codemap.mjs changes \
  --root ./
```

2. **Review the output** - It shows:
   - Added files
   - Removed files
   - Modified files
   - Affected folders

3. **Only update affected codemaps** - Spawn one fixer per affected folder to update its `codemap.md`.
4. **Run update** to save new state:

```bash
node <skill-root>/scripts/codemap.mjs update \
  --root ./
```

### Step 4: Finalize Repository Atlas (Root Codemap)

Once all specific directories are mapped, the Orchestrator must create or update the root `codemap.md`. This file serves as the **Master Entry Point** for any agent or human entering the repository.

1.  **Map Root Assets**: Document the root-level files (e.g., `package.json`, `index.ts`, `plugin.json`) and the project's overall purpose.
2.  **Aggregate Sub-Maps**: Create a "Repository Directory Map" section. For every folder that has a `codemap.md`, extract its **Responsibility** summary and include it in a table or list in the root map.
3.  **Cross-Reference**: Ensure that the root map contains the absolute or relative paths to the sub-maps so agents can jump directly to the relevant details.

### Step 5: Register Codemap in AGENTS.md

**OpenCode auto-loads `AGENTS.md` into agent context on every session.** To ensure agents automatically discover and use the codemap, update (or create) `AGENTS.md` at the repo root:

1. If `AGENTS.md` already exists and already contains a `## Repository Map` section, **skip this step** — the reference is already set up.
2. If `AGENTS.md` exists but has no `## Repository Map` section, **append** the section below.
3. If `AGENTS.md` doesn't exist, **create** it with the section below.

```markdown
## Repository Map

A full codemap is available at `codemap.md` in the project root.

Before working on any task, read `codemap.md` to understand:
- Project architecture and entry points
- Directory responsibilities and design patterns
- Data flow and integration points between modules

For deep work on a specific folder, also read that folder's `codemap.md`.
```

This is idempotent — repeated codemap runs will detect the existing section and skip. No duplication.
