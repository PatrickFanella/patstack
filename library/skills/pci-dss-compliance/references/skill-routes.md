# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `integrate-stripe-payments` | optional | When scope reduction relies on Stripe-hosted Checkout or tokenization. |
| `secure-web-code` | optional | When the user also asks for a security review of the payment code. |
