---
name: operations-vault
description: "Machinum homelab docs. Use to record host or service evidence, update inventory, runbooks or reports, refresh host briefings, or route incident, backup and service-change work. Docs alone authorize no changes."
---

# Machinum Vault

Read root AGENTS.md and 20-operations/Documentation Control/Agent Documentation Policy.md. Identify the host/service and inspect its existing note plus current source/runtime evidence. Preserve historical dates and uncertainty. Put concise durable facts in inventory, recovery steps in runbooks, and detailed observations in a dated report; link them together.

Inspect Git status before editing. Preserve unrelated changes and commit only intended paths. Run the cross-vault documentation audit using `python3 "/home/onnwee/Work/Vaults/Ars Malefica/scripts/documentation.py" audit` on Kvant. This checks registry integrity, not live service health.

For an authorized briefing refresh, commit the relevant host note and policy, then run ~/Documents/Documentation-Hub/scripts/sync-briefings.py in preview mode before --apply. Keep source/hash checks intact; record per-host results and leave conflicting copies untouched. Do not write directly to generated HOMELAB.md or the retired personal-vault tree.

A writing request does not itself authorize deployment, service restart or network changes. Public output remains hash-allowlisted. Report local commit, Sync, per-host refresh and website publication as separate evidence.

For health, alert routing, exposure, storage, GPU or service-change work, read [operational evidence](references/operational-evidence.md) and the relevant maintained host/runbook notes.
