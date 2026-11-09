# kube-artifact-smith procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# kube-artifact-smith

Select raw manifests, chart templates, or workload policy. Validate the rendered artifact and intended namespace before any authorized cluster operation. Generating configuration does not authorize applying it.

## Select a mode

- Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Read [the procedure](references/modes/helm-chart-scaffolding/guide.md).
- Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Read [the procedure](references/modes/k8s-manifest-generator/guide.md).
- Implement Kubernetes security policies including NetworkPolicy, Pod Security Admission, and RBAC for production-grade security. Read [the procedure](references/modes/k8s-security-policies/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
