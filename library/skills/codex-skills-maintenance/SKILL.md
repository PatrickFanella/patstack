---
name: codex-skills-maintenance
description: "Skill catalog audit: inventory and validate personal, repository, system and plugin skills, find trigger collisions and broken references, or run a post-upgrade pass."
---

# Codex Skills Maintenance

Audit the entire catalog while editing only durable user- or repository-owned
sources.

## Workflow

1. **Resolve the live catalog.** Use the task-visible skill list and
   `codex plugin list`; cache contents alone do not prove installation or
   activation.
2. **Inventory structure.** Run:

   ```bash
   python3 scripts/audit_skills.py --format markdown
   ```

3. **Classify ownership.**
   - Edit personal and repository skills at their source of truth.
   - Treat `.system`, plugin cache, and primary-runtime skills as managed.
   - Never patch versioned cache copies; use routing guidance, a distinctly
     named personal overlay, or an upstream report.
4. **Audit semantics.** Review trigger descriptions, routing boundaries,
   progressive disclosure, safety gates, deterministic scripts, dependencies,
   and completion contracts. Read `references/audit-criteria.md`.
5. **Implement narrowly.** Preserve working behavior, move detailed material
   into one-level references, add scripts only for repeated deterministic work,
   and keep `SKILL.md` under 500 lines.
6. **Validate.** Run the current `skill-forge` `quick_validate.py`, parse
   metadata, type-check and execute scripts, and test real runtime contracts
   where safe.
7. **Forward-test complex revisions.** Give independent agents realistic tasks
   without leaking the expected answer. Avoid live production mutations.
8. **Report.** Separate implemented improvements, managed findings, validation,
   and remaining upstream or interactive work.

## Efficiency Rules

- Prefer one precise skill over a broad router plus several overlapping skills.
- Use metadata for triggering, `SKILL.md` for the core workflow, references for
  conditional detail, scripts for deterministic repetition, and assets only
  for output material.
- Do not load large catalogs or references when a summary script can answer the
  question.
- Prioritize active skills and real trigger collisions over stale cache volume.
- Keep personal overlay names distinct from vendor skill names.

## Safety

- Preserve unrelated edits and generated catalogs with a documented source of
  truth.
- Do not modify plugin caches, system skills, primary runtimes, OAuth material,
  or live external data during a skill audit.
- Treat tool-schema changes as application/API changes; audit them separately
  and test compatibility before implementation.
- Ask before forward-tests that are slow, approval-heavy, or production-facing.

## Completion Contract

Finish only when:

- the catalog inventory is reproducible;
- every user-owned skill passes structural validation;
- revised scripts have been executed on representative inputs;
- installed copies match their canonical sources;
- managed findings identify their ownership and safe remediation path;
- the report states active-catalog limits and unverified behavior.
