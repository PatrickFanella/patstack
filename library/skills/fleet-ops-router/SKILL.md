---
name: fleet-ops-router
description: "Homelab operations: route fleet health checks, incidents, backups and service changes to Machinum inventory and runbooks before acting on a host."
---

# Homelab operations

Resolve the current Machinum vault root from global host context; on Kvant it is ~/Work/Vaults/Machinum. Read its AGENTS.md, then .agents/skills/operations-vault/SKILL.md and the relevant operational-evidence reference. Other devices must resolve their actual root or canonical source before relying on local paths. Do not recreate retired .nuc, docs/almaz or Ars Malefica operations trees.

Machinum owns maintained host facts and runbooks. The current checkout owns executable changes. Reuse existing authorization, preserve active work and connectivity, and distinguish documentation edits from infrastructure changes. Missing vault transport is a specific limitation; historical library skills are not a substitute for current operational authority.
