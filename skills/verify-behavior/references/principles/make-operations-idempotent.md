# Make Operations Idempotent

For operations retried after interruption, identify durable state and a stable operation identity. Repeated execution should converge without duplicating externally visible effects; test partial completion and retries.
