## Remove with evidence

Classify candidates by purpose rather than filename alone:

- Generated builds, coverage, screenshots, and run logs: remove reproducible output within scope; preserve needed diagnostic evidence outside the checkout and update ignore rules.
- Plans and completion reports: remove obsolete tracked documents when requested, repairing references. Preserve current operational runbooks, migration/recovery procedures, compliance requirements, and machine-consumed evidence schemas. Git history preserves tracked history; it does not preserve untracked files.
- Application code: establish that production has no callers before removal. Include lazy routes, dynamic imports, registries, reflection, framework discovery, scripts, and external/public entry points in that analysis.
- Dependencies: inspect build configuration, plugins, generated code, and scripts before accepting a static analyzer's finding.
- Tests: identify the behavior that each candidate does or does not protect.

Treat analyzer output as candidates, not deletion authority. Whole-file reachability does not prove every export is used. Conversely, a symbol referenced only by its own tests may still be a supported external API. Follow the actual entry-point model.

Remove obsolete implementations, their exclusive tests, unused exports/helpers, and stale documentation references together.

When retiring an external integration, establish outstanding provider and database obligations before removing servicing code. Preserve migration history, audit records, and personal-data export access; an unused billing API does not imply its historical data should disappear. Audit constructors, schedulers, shutdown hooks, configuration, CSP allowances, email dispatch, CLI tools, and generated API contracts as well as ordinary callers. Match complete symbols: similarly named subscription or webhook systems may have unrelated responsibilities.

Update test-runner commands and behavior ownership with the removal. A test-name filter that now matches nothing can exit successfully without exercising a contract. Replace it with a test of the supported boundary, and verify the replacement is actually executed. Regenerate API artifacts through the existing workflow, reviewing unrelated generator drift before committing it.
