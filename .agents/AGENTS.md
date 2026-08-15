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

## Strategy Consulting Skill Pipe (Automated Workflow)
When the user invokes `/strategy-consulting` with an organization name (e.g., `/strategy-consulting TraceHeal`), you MUST act as an automated skill pipe. DO NOT ask the user to write a verbose prompt, and DO NOT immediately hallucinate a text response. You must execute the following chain automatically:

1. **Interactive Routing (The Front Door):** Use the `ask_question` tool to pop up an interactive multiple-choice modal. Ask the user which of the 6 Strategy Domains (or specific frameworks like Situation Assessment, Competitive Intel) they want to apply to the organization.
2. **Automated Fact-Gathering (Deep Research):** Once the framework is selected, DO NOT hallucinate data. Use specialized CLI tools (`hackernews-pp-cli`, `firecrawl-pp-cli`, or `search_web`) to gather raw factual context, market signals, and competitor data for the target organization. 
3. **Template Formatting (The Synthesizer):** Pipe the gathered facts through the logic defined in `strategy-consulting-deck-template.md`. You must enforce the "Accenture Voice": Slide titles are claims, adhere to the Rule of 3, and ensure recommendations have an Action, Owner, Date, and Metric. Output the result in the `### PPTX_READY_DECK` structured format.
4. **Artifact Generation (The Compiler):** Automatically generate a Python script using `python-pptx` to convert the `PPTX_READY_DECK` markdown into a professional `.pptx` file. Execute the script and provide the user with a clickable `file://` link to the generated slide deck.


## Universal Execution Protocol (Consulting Pipelines)
When running any research, consulting, or intelligence sprint, you MUST adhere to the following execution pipeline:

1. **Strict OSINT Enforcement:** NEVER hallucinate data. You must always use real web scraping/OSINT searches (e.g., Reddit, HackerNews, G2) to ground your findings in reality. If the search yields no data, halt and prompt the user.
2. **Review Gate (Deliverables):** Do NOT automatically compile the final .pptx deck. First, generate the Markdown report and the indings.json mapping. Pause and ask the user for approval or edits. ONLY compile the .pptx once the user approves the JSON/Markdown.
3. **Universal Context Mapping:** EVERY consulting artifact (Markdown, JSON, PPTX) must begin with an explicit "OSINT Source Map & Methodology" section/slide. This must explain *why* specific communities or data sources were targeted by mapping them directly to the company's value proposition.
