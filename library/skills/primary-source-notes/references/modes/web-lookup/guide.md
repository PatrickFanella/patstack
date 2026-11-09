# web-lookup procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# Web Search

Use one web-lookup skill for current information lookup.

## Preferred Backend

1. The client's built-in search (WebSearch in Claude Code, web search in Codex, `websearch` in OpenCode) or the Exa `websearch` MCP for general web search.
2. Brave only when a configured Brave API key is available and localized/freshness search is required.
3. Tavily only when a configured Tavily API key is available and AI-optimized summary/domain filtering is required.

## Workflow

1. Restate the exact fact/current-info need.
2. Search with the default available backend.
3. Fetch primary sources when snippets are insufficient.
4. Prefer official docs, primary sources, and recent dated material.
5. Cite or name sources in the answer when factual precision matters.

## Do Not Use

- For codebase search; use repo search tools.
- For library docs when Context7 or official docs are available.
- For private/authenticated pages unless user explicitly provides access path.

## Resources

### Curated references

Former merged-skill dumps were distilled into these lookup files:

- `references/curated/web-search-brave.md` — Web Search Brave guidance.
- `references/curated/web-search-tavily.md` — Web Search Tavily guidance.


### Extracted resource directories

- `references/` — curated resources extracted from prior merged skill material.
- `scripts/` — curated resources extracted from prior merged skill material.
