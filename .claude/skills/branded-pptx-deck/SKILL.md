---
name: branded-pptx-deck
description: >
  Compile a branded PPTX presentation from structured JSON findings.
  This skill is the LAST MILE of the skill pipe. It does NOT generate content.
  It receives a fully synthesized JSON payload and injects it into the
  24-slide corporate template (template-branded.pptx).
  Upstream skills (ai-analyst, strategy-consulting) are responsible for
  content quality, narrative arc, and Accenture Voice formatting.
---
# Branded PPTX Deck — Compilation Skill

This skill is a **compiler**, not a content generator. It takes a structured JSON file and injects it into the pre-designed shapes of `template-branded.pptx`.

## When to Use
- Called by `strategy-consulting` at Step 4 (Artifact Generation)
- Called by `ai-analyst` at the "Present" stage after full synthesis

## Input: JSON Schema

The JSON input must be a **single object** (not an array) with these keys:

```json
{
  "company": "TraceHeal",
  "domain": "SITUATION ASSESSMENT",
  "headline": "Assertion-style claim (not a label)",
  "executive_read": "2-3 sentence executive summary paragraph",
  "key_findings": [
    "Finding 1 — specific, evidence-backed",
    "Finding 2 — quantified where possible",
    "Finding 3 — actionable implication",
    "Finding 4 — risk or opportunity call"
  ],
  "table_rows": [
    {"area": "Dimension", "evidence": "Data point", "interpretation": "So what", "confidence": "High|Medium|Low"},
    {"area": "...", "evidence": "...", "interpretation": "...", "confidence": "..."},
    {"area": "...", "evidence": "...", "interpretation": "...", "confidence": "..."},
    {"area": "...", "evidence": "...", "interpretation": "...", "confidence": "..."}
  ]
}
```

### Domain Values
The `domain` field must exactly match a framework suffix in the template's slide titles:
- SITUATION ASSESSMENT, GROWTH BARRIERS, ASSUMPTION AUDIT
- MARKET MAPPING, COMPETITIVE INTEL, CUSTOMER SEGMENTATION, PROFIT POOL ANALYSIS
- STRATEGIC OPTIONS, BUSINESS CASE BUILDER, PORTFOLIO REVIEW, PRICING STRATEGY
- OPERATING MODEL DESIGN, TRANSFORMATION ROADMAP, INITIATIVE PRIORITIZER
- KPI ARCHITECT, RISK & MITIGATION, VALUE REALIZATION, WAR GAMING
- DECISION MEMO, NARRATIVE BUILDER, STAKEHOLDER ALIGNMENT

## Template
The canonical template is `template-branded.pptx` in the workspace root. Do NOT use the generic `resources/template.pptx`.

## Execution

```bash
uv run --with python-pptx python .agents/skills/branded-pptx-deck/scripts/compile.py findings.json template-branded.pptx Output_Deck.pptx
```

## What the Compiler Does
1. **Modifies Slide 1 (Title):** Injects company name, domain, and branding
2. **Finds the target framework slide:** Matches `domain` to the slide whose title contains `· DOMAIN_SUFFIX`
3. **Injects all content:** Headline (shape 5), executive read (shape 7), 4 key findings (shapes 11/13/15/17), and table rows (shapes 28+, stride of 5)
4. **Prunes unused slides:** Keeps only Slide 1, Slide 2 (Executive Overview), and the target framework slide. Deletes the rest.
5. **Saves the output:** Clean 3-slide branded deck

## Quality Gate
This skill does NOT validate content quality. The upstream skill (ai-analyst or strategy-consulting) is responsible for ensuring:
- Headlines are **assertion-style claims**, not labels
- Findings are **evidence-backed**, not opinions
- Table rows have **specific data points**, not vague phrases
- The narrative follows **situation → complication → resolution** arc
