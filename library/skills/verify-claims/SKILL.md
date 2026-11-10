---
name: verify-claims
description: Check claims in generated text or a public narrative against cited sources
  as a separate verification pass.
license: MIT
metadata:
  blacktower-pack: core
  blacktower-kind: workflow
  blacktower-tier: core
  blacktower-capabilities: fact verification,source checking,citation audit,hallucination
    detection
  author: jwynia
  version: '1.0'
  domain: research
  cluster: methodology
  type: diagnostic
  mode: evaluative
---

# verify-claims

Separate assertions, facts and interpretation. Do not turn a requested fact check into persuasive rewriting or treat absent evidence as proof.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **claim verifier**: Fact check: verify claims in already generated output against sources, as a separate pass after writing. Read [the procedure](references/base-workflow.md).
- **viral claim probe**: Viral claims: investigate a social media claim or narrative, split multi-part assertions, separate fact from interpretation and triangulate sources. Read [the procedure](references/modes/viral-claim-probe/guide.md).
