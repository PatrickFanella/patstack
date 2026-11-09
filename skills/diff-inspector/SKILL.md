---
name: diff-inspector
description: Review a working-tree, branch, commit or PR diff for defects, downstream
  impact or a requested review walkthrough.
---

# diff-inspector

Default to a read-only, single-reviewer defect review. Delegated reviews remain read-only. Strict, multi-model and parallel review modes require the corresponding explicit request; a review does not authorize fixes or posting.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **diff inspector**: Use when reviewing a diff, branch, PR or working tree for defects, blast radius, or explicitly requested maintainability depth. Read [the procedure](references/base-workflow.md).
- **diff auditor**: Review a delegated code change read-only and return every actionable defect with priority. Use when another agent hands off uncommitted changes, a base-branch diff or a commit. Read [the procedure](references/modes/diff-auditor/guide.md).
- **diff walkthrough**: Use when asked for a PR review canvas or diff walkthrough: regroup a pull request diff by reviewer importance and flag tricky code. Cursor Canvas output; HTML or Markdown fallback elsewhere. Read [the procedure](references/modes/diff-walkthrough/guide.md).
- **change blast check**: Use for blast radius of X or what could this break: find breakage beyond the diff and prove the one fact that makes the change safe by running real code. Read [the procedure](references/modes/change-blast-check/guide.md).
- **thermo twin audit**: Thermos: run both thermo-nuclear reviews (bugs/security and code quality) in parallel on one branch, then merge their findings. Use for thermos or a double thermo review. Read [the procedure](references/modes/thermo-twin-audit/guide.md).
- **model crossfire**: Multi-model adversarial code review on explicit request: "interrogate", "challenge this", "stress test this code", "find blind spots. Read [the procedure](references/modes/model-crossfire/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
