---
name: gemini-notebook-playbook
description: Master orchestrator for the Gemini Notebook Playbook for Founders. Turns raw research, messy documents, call recordings, spreadsheets, and market signals into finished business deliverables using chained staged workflows.
argument-hint: [inputs or objective]
---

# Gemini Notebook Playbook for Founders — Master Orchestrator

This skill operationalizes the complete **Gemini Notebook Playbook for Founders** by Lian Lim. It bridges the gap between raw business information and finished, executive-grade business deliverables.

## Core Operating Philosophy

1. **One Notebook = One Job**: Never create a generic 'dump everything' repository. Every run/notebook must be anchored around a single distinct business objective (e.g., US Market Expansion, Sales Call Intelligence, Pricing Restructure, Client Onboarding SOP).
2. **Decide What You Want at the End**: Define the desired artifact before executing:
   - What are we trying to figure out?
   - What information do we already have?
   - What information are we missing?
   - What finished output is needed (Deck, Report, Excel Model, SOP, Decision Memo)?
3. **Chain Everything Into One Complete Workflow**: Rather than treating analysis steps as isolated queries, chain them sequentially so the evidence and context compound.

---

## The 10-Step Chained Execution Pipeline

When invoked with an objective or folder of materials, execute in sequential stages:

`
[1. Raw Ingestion] -> [2. Research Auditor] -> [3. Missing Research Finder]
        |
        v
[4. Devil\'s Advocate] -> [5. Business Data Analysis] -> [6. Strategic Verdict]
        |
        v
[7. Action Recommendations] -> [8. Output Artifact Generation (PPTX/Excel/Report/SOP)]
`

### Stage 1: Ingestion & Baseline Fact Mapping
- Gather and inspect all input documents, call transcripts, notes, and datasets.
- Establish the baseline scope and objective.

### Stage 2: Research Audit (
esearch-auditor)
- What is known with reasonable confidence?
- What are we currently assuming?
- Where do sources agree or conflict?
- What unanswered questions could materially change the decision?

### Stage 3: Gap Discovery (missing-research-finder)
- Categorize missing data into **Critical** (blocks decision), **Important** (increases confidence), and **Nice to Have**.
- Formulate precise queries and recommend primary/secondary source types.

### Stage 4: Counter-Hypothesis & Pre-Mortem (devils-advocate)
- Steelman the counter-case against the current hypothesis.
- Identify failure modes, fragile assumptions, and falsification criteria.

### Stage 5: Data & Unit Economics Validation (usiness-data-analysis / xcel-model-generator)
- Inspect data hygiene (duplicates, missing values, date alignments, anomalies).
- Compute core unit metrics (CAC, LTV, Gross Margin, Conversion, Payback, ROI).
- Model Conservative, Base, and Aggressive scenarios.

### Stage 6: Synthesis & Decision Framing
- Contrast options (e.g., Full Launch vs. Pilot vs. Partner vs. Defer).
- Determine the evidence-backed strategic decision.

### Stage 7: Action & Risk Matrix
- Frame recommendations with: **Action**, **Rationale**, **Supporting Evidence**, **Expected Impact**, and **Key Risks**.

### Stage 8: Deliverable Compilation
Generate the required final output format:
- **Presentation**: powerpoint-builder / randed-pptx-deck (10-slide executive structure)
- **Financial Model**: xcel-model-generator (.xlsx / structured tables)
- **Executive Memo**: xecutive-report (Standalone briefing)
- **Standard Operating Procedure**: sop-builder (9-point operational guide)
- **Sales Intelligence**: sales-intelligence (Win/Loss playbook)

---

## Sub-Skills Directory

You can trigger any individual module directly or let this orchestrator chain them:
- /research-auditor — Inspect evidence quality & assumptions
- /missing-research-finder — Prioritize information gaps
- /devils-advocate — Evidence-based counterarguments
- /business-data-analysis — Quantitative hygiene & metric calculation
- /powerpoint-builder — 10-slide executive pitch/deck
- /excel-model-generator — 3-scenario financial model
- /executive-report — Decision memo & report
- /sop-builder — 9-point SOP from messy company notes
- /sales-intelligence — Win/Loss pattern analysis
- /full-project-workflow — Strict staged execution runner
