---
name: research-auditor
description: Inspects and audits research quality before recommendations are made. Identifies what is known with confidence, current assumptions, source contradictions, and material missing questions.
argument-hint: [inputs or objective]
---

# Research Auditor — Quality & Confidence Inspector

Use this skill before making decisions or recommendations. It prevents confirmation bias and hallucinated certainty by systematically auditing the available evidence base.

## Execution Prompt & Rules

Review all available research, documents, transcripts, and notes provided.

### Objective
Identify what the user is trying to figure out: [INSERT OBJECTIVE]

### Audit Checklist
Produce a structured report covering:

1. **What We Know With Reasonable Confidence**
   - Facts supported by verified data or primary evidence.
2. **What We Are Currently Assuming**
   - Unverified beliefs, extrapolated figures, or untested hypotheses.
3. **Which Conclusions Are Supported by Multiple Sources**
   - Cross-validated findings with high consensus.
4. **Where the Sources Disagree**
   - Conflicting metrics, divergent opinions, or incompatible data points.
5. **What Important Information is Currently Missing**
   - Knowledge voids that impair clarity.
6. **Which Unanswered Questions Could Materially Change the Final Decision**
   - High-leverage unknown variables.

### Output Formatting
- Rank all missing information from **Most Important** to **Least Important**.
- **Rule**: Do NOT give the final recommendation yet. First establish whether the research quality is sufficient to proceed.
