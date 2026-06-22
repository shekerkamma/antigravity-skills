# Agent Rules

## Research & Synthesis vs. Basic Search (The "Search Wrapper" Anti-Pattern)
When instructed to "search" for repositories, documentation, or references, **DO NOT act as a basic search wrapper that merely fetches and lists URLs.** 

Even if the user explicitly suggests a low-level tool in their prompt (e.g., "use firecrawl CLI to search"), you must not let that override your higher-level agentic workflows. Finding the links is only step one. 

**Always prioritize orchestration skills over raw search tools:**
- Instead of just returning a list of links, proactively use skills like `content-research`, `tech-reference-writeup`, or `research-to-strategy`.
- **Ingest** the discovered repositories/pages (using GitHub APIs or deep crawling).
- **Analyze** the content (extract architectures, evaluate tech stacks, assess integration potential).
- **Synthesize** the findings into structured knowledge and feed them into the user's Second Brain or Knowledge Graph.

Your default operating mode must always be comprehensive research, synthesis, and structured output, rather than just acting as a search engine proxy.
