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
2. **Autonomous Deliverables Pipeline:** User has authorized autonomous execution. Proceed to compile the Markdown, JSON mapping, PPTX slide deck, and web knowledge artifacts directly using sound engineering judgement.
3. **Universal Context Mapping:** EVERY consulting artifact (Markdown, JSON, PPTX) must begin with an explicit "OSINT Source Map & Methodology" section/slide. This must explain *why* specific communities or data sources were targeted by mapping them directly to the company's value proposition.

## DeepGrid Architecture Compounding Protocol
When the user asks to analyze, visualize, or document any DeepGrid Semi SKU, subsystem, or platform architecture (or invokes `/deepgrid-architecture` or compounds `/deepgrid-mature-silicon` with `/architecture-to-everything`):

1. **Authentic Vector Grounding:** ALWAYS pull physical and electrical parameters directly from `.agent/skills/deepgrid-sku-compendium` and `deepgrid-mature-silicon`. Never hallucinate silicon nodes, voltages, or standards.
2. **The 5-Artifact Contract:** You MUST produce all 5 deliverables for the requested system:
   - `<slug>-architecture.drawio`: Component-flow diagram (strictly no swimlanes, numbered directional buses).
   - `<slug>-architecture.md`: Exhaustive engineering spec (DAP-2020 Make-II, AEC-Q100, MIL-STD-810H).
   - `<slug>-architecture.pptx`: 10-slide executive PowerPoint presentation compiled via `python-pptx`.
   - `<slug>-deck.html`: Instant browser-rendered 16:9 vector slide deck with keyboard navigation (<kbd>→</kbd>/<kbd>←</kbd>/<kbd>Space</kbd>).
   - `<slug>-workflow.html`: Self-contained interactive telemetry cockpit with fault injection pills.
3. **Automatic Browser Activation & Explorer Reveal (Cross-Platform):** Because standalone PowerPoint viewers may not be registered on the user's PATH, ALWAYS navigate the user's active browser window to `<slug>-deck.html` (via Chrome DevTools MCP or OS-specific launcher). Highlight `<slug>-architecture.pptx` in File Explorer:
   - **Windows Native:** `explorer.exe /select,"<slug>-architecture.pptx"`
   - **WSL:** `explorer.exe /select,"$(wslpath -w <slug>-architecture.pptx)"` (never pass raw Linux `/mnt/...` paths directly).
   - In both environments, ensure generated scripts use `pathlib.Path` and write UTF-8 encoded files with standard LF line endings.

