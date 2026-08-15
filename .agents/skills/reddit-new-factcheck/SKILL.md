---
name: reddit-new-factcheck
description: Validate business hypotheses, identify real pain points, and discover AI agent use cases by deeply analyzing niche Reddit communities. Use when the user wants to fact-check an AI startup idea, discover real business challenges in a vertical, or position a product against actual market complaints.
---

# Reddit Market Fact-Check & Pain Point Discovery

This skill uses Reddit as a ground-truth signal to validate whether an assumed business challenge actually exists, how painful it is, and how an Agentic AI solution should be positioned to solve it uniquely.

## Trigger Scenarios
- "Fact-check this startup idea on Reddit"
- "What are property managers actually complaining about?"
- "Find pain points in the accounts receivable space"
- "Run the reddit fact-check pipeline for [Vertical]"

## Execution Pipeline

When invoked, run the following steps sequentially:

### Step 1: Subreddit & Query Identification
1. Ask the user for their target vertical or business hypothesis (if not already provided).
2. Identify the top 2-3 hyper-niche subreddits where these professionals hang out (e.g., `r/realtors`, `r/sysadmin`, `r/bookkeeping`).
3. Formulate search queries targeting high-friction keywords: "hate", "takes forever", "worst part", "software sucks", "manual entry", "exhausting".

### Step 2: Thread Extraction (Ground Truth Collection)
1. Use the **`firecrawl-pp-cli`** or the existing `scripts/reddit_thread_extractor.py` (from `reddit-seo-pipeline`) to extract the top 5-10 threads matching the friction queries in those subreddits.
2. Pull the raw comment data into your context. You are looking for visceral, emotional complaints about existing workflows or legacy software.

### Step 3: Pain Point & Solution Mapping (The "Fact-Check")
Analyze the extracted threads to build the following mapping:
1. **The Stated Problem (Hypothesis):** What we thought the problem was.
2. **The Actual Problem (Ground Truth):** What the practitioners actually complain about. (e.g., *Hypothesis:* "Therapists need better note-taking apps." *Ground Truth:* "Therapists spend 3 hours a day fighting insurance claim rejections.")
3. **The Current Workaround:** How they solve it today (usually Excel, offshore VAs, or brute-force manual labor).
4. **The Agentic AI Solution:** How an autonomous agent solves this deterministically.

### Step 4: Output & Differentiated Positioning
Compile the findings into a **Market Validation Brief** (Markdown artifact) or a **MARP slide deck** (`marp` skill). The output MUST include:

*   **Executive Summary:** Is the vertical a viable target for Agentic AI? (Fact-check verdict: TRUE / FALSE / PIVOT).
*   **The "Bleeding Neck" Pain Points:** Direct quotes from Reddit proving the pain exists and is severe enough that people would pay to make it go away.
*   **Legacy Tool Failures:** Why existing SaaS or generic AI (like ChatGPT) is failing these users.
*   **Differentiated Positioning Strategy:** How to pitch the Agentic AI solution. (e.g., "Don't sell 'AI', sell 'Zero-Touch Claims Processing'").

## Constraints & Safety
- **Avoid Surface-Level Trends:** Do not use `r/startups` or `r/artificialintelligence`. You must go to the practitioner subreddits where the actual work happens.
- **Focus on Workflow, Not Content:** Look for complaints about repetitive, high-stakes tasks, not complaints about general industry trends. Agentic AI thrives on replacing repetitive workflows.
