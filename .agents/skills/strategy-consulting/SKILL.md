---
name: strategy-consulting
description: >
  Automated skill pipe for running Accenture-style strategy frameworks
  and generating branded PPTX decks. Routes the user's question to one
  of 21 consulting frameworks, synthesizes through the AI Analyst, formats via the specific
  sub-skill template, and compiles into a fully branded client-ready presentation.
---
# Strategy Consulting Skill Pipe

When the user invokes `/strategy-consulting <organization>`, you must act as a fully automated skill pipe. Do not bypass the sub-skills or hallucinate raw JSON. Follow this exact 5-step pipeline:

### Step 1: Interactive Routing (The Front Door)
Use the `ask_question` tool to pop up a multiple-choice modal asking the user which of the 6 Strategy Domains (or specific frameworks) they want to apply to the organization:

**Domain 1: Diagnosis & Framing** — Situation Assessment, Growth Barriers, Assumption Audit
**Domain 2: Market & Competitive Intel** — Market Mapping, Competitive Intel, Customer Segmentation, Profit Pool Analysis
**Domain 3: Strategic Choice & Economics** — Strategic Options, Business Case Builder, Portfolio Review, Pricing Strategy
**Domain 4: Operating Model & Execution** — Operating Model Design, Transformation Roadmap, Initiative Prioritizer
**Domain 5: Risk, Performance & Value** — KPI Architect, Risk & Mitigation, Value Realization, War Gaming
**Domain 6: Alignment & Exec Communication** — Decision Memo, Narrative Builder, Stakeholder Alignment

### Step 2: Automated Fact-Gathering (Deep Research)
Gather raw factual context, market signals, and competitor data for the target organization using your search tools.

### Step 3: Synthesis (AI Analyst Narrative)
Act as the AI Analyst (or invoke the `ai-analyst` skill) to structure the raw data into a coherent analytical narrative. Extract the **Context**, the **Tension** (the problem/gap), and the **Resolution** (the strategic wedge). Validate the numbers—do not just list facts.

### Step 4: Formatting (The Sub-Skill & Universal JSON Schema)
1. Read the specific sub-skill `.md` file for the chosen framework (e.g., `situation-assessment.md` or `growth-barriers.md`) to understand its exact required **Output Format**.
2. Translate the AI Analyst narrative into that specific markdown structure.
3. Map that markdown into the Universal JSON Schema (`findings.json`) required by the compiler.

The `findings.json` MUST support the Universal Branded Compiler schema:
```json
{
  "company": "TargetCompany",
  "domain": "NAME OF FRAMEWORK",
  "headline": "Declarative claim here",
  "executive_read": "2-3 sentence executive summary",
  "key_findings": ["Finding 1", "Finding 2"],
  "slides": [
    {
      "type": "table",
      "title": "Dynamic Table Title (e.g., Fact Base)",
      "headers": ["Col 1", "Col 2", "Col 3"],
      "rows": [ ["R1C1", "R1C2", "R1C3"] ]
    },
    {
      "type": "split",
      "title": "Dynamic Split Layout Title",
      "left_title": "LEFT HEADING",
      "left_bullets": ["Point 1"],
      "right_title": "RIGHT HEADING",
      "right_bullets": ["Point A"]
    },
    {
      "type": "bullets",
      "title": "Dynamic Bullets Title",
      "bullets": ["Point 1", "Point 2", "Point 3"]
    },
    {
      "type": "quotes_grid",
      "title": "Raw OSINT Quotes",
      "quotes": ["Quote 1", "Quote 2", "Quote 3", "Quote 4", "Quote 5", "Quote 6"]
    }
  ]
}
```

### Step 5: Artifact Generation (The Universal Compiler)
Call the `branded-pptx-deck` universal skill compiler to generate client-ready slides dynamically from scratch:

```bash
uv run --with python-pptx python .agents/skills/branded-pptx-deck/scripts/compile.py findings.json template-branded.pptx <CompanyName>-<Domain>-Deck.pptx
```

Provide the user the full Windows path to the output `.pptx` file.
