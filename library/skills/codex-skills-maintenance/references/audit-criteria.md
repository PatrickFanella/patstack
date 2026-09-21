# Skill Audit Criteria

## Contents

- [Ownership](#ownership)
- [Triggering](#triggering)
- [Progressive disclosure](#progressive-disclosure)
- [Resources](#resources)
- [Metadata and dependencies](#metadata-and-dependencies)
- [Validation](#validation)
- [Ecosystem routing](#ecosystem-routing)

## Ownership

- Personal or repository source: safe to edit within the request.
- Installed snapshot with a known source repository: edit the source, validate,
  then reinstall.
- `.system`, plugin cache, or primary runtime: managed; do not edit in place.
- Cache-only presence does not mean a skill is active.

## Triggering

- Frontmatter contains only `name` and `description`.
- Description states capability plus concrete trigger contexts.
- Adjacent skills have explicit routing boundaries.
- Exact duplicate names are safe only when the plugin namespace remains intact.
- Personal overlays use unique names and avoid generic vendor identities.

## Progressive Disclosure

- Keep `SKILL.md` below 500 lines and focused on essential procedure.
- Put optional, variant-specific, or lengthy detail in directly linked
  `references/`.
- Give references longer than 100 lines a table of contents.
- Avoid duplicate instructions across the body and references.

## Resources

- Use scripts for deterministic repeated work and execute representative tests.
- Use references for schemas, runbooks, policies, and conditional details.
- Use assets only when they are copied or transformed into outputs.
- Avoid README, changelog, installation guide, and other auxiliary files inside
  skill folders.
- Resolve resource paths relative to the skill directory.

## Metadata and Dependencies

- Provide `agents/openai.yaml` for user-facing skills.
- Keep `short_description` between 25 and 64 characters.
- Make `default_prompt` one sentence that explicitly includes `$skill-name`.
- Declare a stable MCP dependency only when the actual server identifier and
  transport are known.
- Omit decorative metadata unless the user supplied it.

## Validation

- Run `quick_validate.py` on every changed skill.
- Parse every YAML/JSON/TOML resource.
- Type-check scripts and execute representative safe paths.
- Check Markdown links after stripping fenced examples.
- Forward-test complicated behavioral changes with minimal leaked context.

## Ecosystem Routing

- Private external data: connector or MCP before browser automation.
- Existing authenticated browser state: Chrome.
- Isolated/local web testing: in-app Browser.
- Native application without a better connector: Computer Use.
- Local file deliverables: Documents, Spreadsheets, Presentations, PDF, or
  Sites based on the requested artifact.
- Google-native deliverables: Google Drive's Docs, Sheets, or Slides workflows.
- Quantitative evidence-backed analysis: Data Analytics; do not trigger it for
  a generic prose report.
- Brand or campaign creative: Canva or Creative Production; do not trigger both
  unless the workflow explicitly hands off between them.
