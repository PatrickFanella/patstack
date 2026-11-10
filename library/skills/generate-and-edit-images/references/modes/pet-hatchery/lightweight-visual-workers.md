## Lightweight Visual Workers

Use lightweight subagents for image-heavy work by default. This bounds each `$generate-and-edit-images` rollout to one selected image, keeps contact-sheet vision payloads out of the parent thread, and reduces cost while preserving the full v2 contract.
