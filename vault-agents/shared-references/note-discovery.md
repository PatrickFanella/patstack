# Note discovery and linking

Use for finding, creating or organizing notes in one of the four vaults. Read the target vault's root AGENTS.md and metadata guide first. Resolve the owning vault before choosing a path; do not impose the old optional skill's Windows path, flat layout or universal filename convention.

For a lookup, search filenames first with `rtk rg --files TARGET_VAULT`, then narrow content with `rtk rg -n` and a specific pattern. Scope searches to relevant folders and return the actual matching source. A file in Archivum can be a snapshot or imported instruction, not current operational authority.

Read the strongest existing note and its nearby index before creating another. Search the intended title, aliases and related concepts to avoid a competing master. For backlinks, use a literal `rtk rg -n -F '[[Note Title' TARGET_VAULT` search as a starting point, then inspect targets, aliases and headings; a text match alone does not prove a link resolves.

Create a note only within the authorized task, using the vault's existing destination, filename, frontmatter and template conventions. Link related notes with vault-local wikilinks and add the new note to the closest maintained index when appropriate. Use an explicit Obsidian URI across vaults; do not create a same-title placeholder in the wrong vault to satisfy a broken link.

After an edit, verify the actual destination, parse authored frontmatter and resolve relevant links against the correct vault. Preserve original source bytes and dates in imported collections. Archive rather than hard-delete when cleanup is authorized, and preserve local dirty state. Filesystem or CLI edits establish local state only; Sync and website publication need their own evidence.

Use an available Obsidian connector or CLI for transport when helpful. Transport choice does not change vault ownership, schemas or authorization. Do not load every vault's workflow for a single lookup.
