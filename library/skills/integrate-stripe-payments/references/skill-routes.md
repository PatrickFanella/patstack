# Companion procedures

Load a companion only under its stated condition. Current authorization and client-native tool contracts remain authoritative. Read the source once; avoid cycles and do not switch the active profile for a one-off reference.

| Skill | Relationship | When to load it |
|---|---|---|
| `manage-stripe-account` | optional | When the integration needs Stripe products, prices or webhook endpoints created or changed. |
| `pci-dss-compliance` | optional | When the flow handles card data outside Stripe-hosted fields. |
| `verify-implementation` | optional | Before claiming a payment or webhook flow works. |
