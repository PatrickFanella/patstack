---
name: fleet-ops-router
description: Operate homelab services or use the matching infrastructure, repository-administration
  or host-runtime runbook.
---

# fleet-ops-router

Read current Machinum inventory and the target host briefing first. Load only the matching platform or host runbook. Authoring infrastructure, certificates or configuration does not authorize applying it; preserve unrelated host state, credentials and recovery evidence.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **fleet ops router**: Homelab operations: route fleet health checks, incidents, backups and service changes to Machinum inventory and runbooks before acting on a host. Read [the procedure](references/base-workflow.md).
- **cf edge deploy**: Use when deploying or configuring a project on Cloudflare Workers, Pages or related services (D1, R2, KV, Durable Objects), including wrangler auth and checking the deployed result. Read [the procedure](references/modes/cf-edge-deploy/guide.md).
- **web host hardening**: Set up or harden a Linux web server: DNS, SSH, firewall, Nginx, static sites, reverse proxy, ACME HTTPS, redirects, BBR. Use for cloud or self-hosted servers. Homelab ingress stays on Almaz. Read [the procedure](references/modes/web-host-hardening/guide.md).
- **kube artifact smith**: Kubernetes artifacts: raw manifests, Helm charts, workload security (NetworkPolicy, Pod Security Admission, RBAC). Use to author or validate them; generating YAML does not authorize applying it. Read [the procedure](references/modes/kube-artifact-smith/guide.md).
- **terraform module smith**: Terraform modules: create or refactor reusable modules with typed inputs, provider constraints, examples, and validation or Terratest checks. Read [the procedure](references/modes/terraform-module-smith/guide.md).
- **gitea fleet tidy**: Use when auditing or normalizing Gitea/Forgejo repositories in bulk: settings, labels, issues, wiki, branch protection, default branches, workflows, releases. Read [the procedure](references/modes/gitea-fleet-tidy/guide.md).
- **mtls trust chain**: Use when configuring or debugging mutual TLS between services: client certificates, trust chains, mesh or proxy policy, rotation. Read [the procedure](references/modes/mtls-trust-chain/guide.md).
- **setup wizard script**: Use when setup or migration needs human steps in dashboards or browsers: generate a bash wizard that walks each stage, hides secret entry, writes .env and Gitea or GitHub CI secrets. Read [the procedure](references/modes/setup-wizard-script/guide.md).
- **codex desktop audit**: Codex Desktop on Sputnik: audit the Arch/Omarchy openai-codex-desktop install after an update, or when the desktop app or codex launcher fails, before proposing any repair. Read [the procedure](references/modes/codex-desktop-audit/guide.md).
- **switchyard runtime desk**: Switchyard runtime on Kvant: managed OpenCode container, Open Pilot runs, native model broker, workflow executor and their compatibility APIs. Use when changing or debugging Switchyard runtime code. Read [the procedure](references/modes/switchyard-runtime-desk/guide.md).
- **t3 repo onboard**: Use when onboarding a repository into T3 dev environments: launcher recipe, isolated worktree previews, tests and project actions. Read [the procedure](references/modes/t3-repo-onboard/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
