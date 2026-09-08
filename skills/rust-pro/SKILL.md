---
name: rust-pro
description: Rust ownership, async execution, errors, concurrency, and systems integration within the existing crate design.
metadata:
  blacktower-pack: engineering
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: language-go-rust,rust,pro
---

# Rust Pro

Use for Rust code that needs safe systems design, async/concurrent behavior, ownership correctness, performance-aware structure, and idiomatic error handling.

## Core routing

- Async Rust, Tokio, async traits, streams, cancellation, and concurrency: use the merged `rust-async-patterns` guidance.
- Ownership, borrowing, lifetimes, RAII, smart pointers, and safe resource management: use the merged `memory-safety-patterns` guidance.
- For non-Rust Go work, use `golang-pro`.

## Resources

Load these only when needed; keep `SKILL.md` as the activation workflow.

## Merged Skills

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/memory-safety-patterns.md` — Memory Safety Patterns guidance.
- `references/curated/rust-async-patterns.md` — Rust Async Patterns guidance.
