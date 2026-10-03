---
name: operations-vault
description: "Maintain Machinum homelab evidence and route authorized host operations, incidents, backups and service changes through current inventory and runbooks. Documentation alone does not authorize infrastructure changes."
---

# Machinum Vault

Read root AGENTS.md and 20-operations/Documentation Control/Agent Documentation Policy.md. Identify the host/service and inspect its existing note plus current source/runtime evidence. Preserve historical dates and uncertainty. Put concise durable facts in inventory, recovery steps in runbooks, and detailed observations in a dated report; link them together.

Inspect Git status before editing. Preserve unrelated changes and commit only intended paths. Run the cross-vault documentation audit using `rtk proxy python "/home/onnwee/Work/Vaults/Ars Malefica/scripts/documentation.py" audit`. This checks registry integrity, not live service health.

For an authorized briefing refresh, commit the relevant host note and policy, then run ~/Documents/Documentation-Hub/scripts/sync-briefings.py in preview mode before --apply. Keep source/hash checks intact; record per-host results and leave conflicting copies untouched. Do not write directly to generated HOMELAB.md or the retired personal-vault tree.

A writing request does not itself authorize deployment, service restart or network changes. Public output remains hash-allowlisted. Report local commit, Sync, per-host refresh and website publication as separate evidence.

For health, alert routing, exposure, storage, GPU or service-change work, read [operational evidence](references/operational-evidence.md) and the relevant maintained host/runbook notes.
