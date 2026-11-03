---
name: stripe-billing-operations
description: "Use before any Stripe account action: invoices, refunds, subscriptions, customers or prices. Confirms account and test/live mode, prevents duplicate effects, reads back results."
---

# Stripe billing operations

This personal overlay supplies the operation discipline. Keep Stripe's managed skills, tool schemas and current documentation as the provider authority; do not modify plugin caches or assume the old wrapper's tool names and limitations remain current.
Account operations require an authenticated Stripe connector, CLI or Dashboard.

1. Resolve the intended Stripe account, connected-account context if relevant, test/sandbox or live mode, target object, and requested result. Inspect the actual backend's account/mode evidence. A missing mode is not permission to mutate live data; development work defaults to a confirmed test context. Existing explicit live authorization remains valid for its stated scope.
2. Prefer the authenticated connector when it supports the operation. Use its discovery/schema tools to select the exact API operation. An authenticated CLI or Dashboard is a fallback within the same authorized account and mode. Do not silently switch accounts, infer credential values, or dump secret-bearing configuration.
3. Read before writing. Search existing customers, products and prices using stable IDs or project metadata. Preserve the project's existing correlation metadata on newly created objects when supported. An email match alone is not proof of customer or application identity. Verify currency, amount and recurring interval against the actual object. Use current [currency rules](https://docs.stripe.com/currencies); do not multiply every amount by 100.
4. Make the requested mutation concrete. For refunds, subscription changes, dispute submissions, invoice finalization/sending or other financial effects, resolve amount, currency, timing, proration/collection behavior and object ID before execution. Reuse explicit authorization already covering those details; request the unresolved decision only when needed. Draft preparation does not authorize collection or sending an invoice.
5. For retryable POST operations, preserve the backend's supported idempotency mechanism. After an ambiguous timeout, read the object or operation result before retrying. Do not retry with a new key or a newly created object while the first effect remains uncertain. If the backend cannot correlate the prior request or resolve its outcome, report the operation as unresolved and stop. See [idempotent requests](https://docs.stripe.com/api/idempotent_requests).
6. Read back the resulting object. Return account/mode, object type and ID, relevant status, amount/currency/timing, and a provider receipt or Dashboard link when available. A request submission is not payment settlement or customer delivery.

Keep invoice draft, finalized/open, sent, paid and void states distinct. Consult the actual [finalize](https://docs.stripe.com/api/invoices/finalize) and [send](https://docs.stripe.com/api/invoices/send) operations rather than assuming one performs both. Never create a real charge, refund, message or subscription change to test this skill.

Product entitlement, pricing approval and application identity rules remain in the consuming project's guidance. Report missing access or unresolved operation state without switching to another credential owner.
