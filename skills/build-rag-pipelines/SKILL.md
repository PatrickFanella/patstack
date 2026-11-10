---
name: build-rag-pipelines
description: "Use when building or tuning retrieval for LLM answers: ingestion and chunking, vector, keyword or hybrid search, reranking, citations, retrieval evaluation."
---

# build-rag-pipelines

Treat ingestion, retrieval, ranking, and grounded answers as separately measurable stages. Preserve source provenance and access boundaries; evaluate retrieval results before attributing answer defects to the model.

## Select a mode

- Combine vector and keyword search for improved retrieval. Read [the procedure](references/modes/hybrid-search-implementation/guide.md).
- Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Read [the procedure](references/modes/rag-implementation/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.

Load [companion procedures](references/skill-routes.md) only when their stated condition applies.
