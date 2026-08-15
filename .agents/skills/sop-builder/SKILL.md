---
name: sop-builder
description: Reconstructs actual vs documented processes from messy company notes, identifies bottlenecks, and creates production-ready 9-point SOPs.
argument-hint: [inputs or objective]
---

# SOP Builder — Process Reverse-Engineer

Use this skill to turn messy Slack threads, Loom transcripts, scattered Google Docs, and meeting notes into standard operating procedures (SOPs).

## Step 1: Process Forensic Reconstruction

Analyze the raw materials and split the workflow into:
1. **Documented Process:** What official manuals, wikis, or legacy SOPs claim should happen.
2. **Actual Process:** What conversations, tickets, and meeting recordings reveal actually happens.
3. **Contradictions:** Direct conflicts between official policy and daily reality.
4. **Missing Steps:** Shadow workflows the team executes that are documented nowhere.
5. **Bottlenecks:**
   - Repeated manual data entry
   - Duplicate tasks across team members
   - Unclear ownership / orphan steps
   - Approval delays and waiting queues
   - Unnecessary tool handoffs

## Step 2: The 9-Point Standard Operating Procedure

Synthesize into an operational SOP:

1. **Trigger:** What event initiates this process?
2. **Owner:** Single accountable role.
3. **Required Inputs:** Checklists, assets, or data required before starting.
4. **Step-by-Step Execution:** Sequential, numbered actions with clear verb-first instructions.
5. **Tools & Systems Used:** Exact software, URLs, templates, or scripts.
6. **Decision Points:** Clear branching logic (If X -> do Y; If A -> do B).
7. **Exceptions & Escalation:** How to handle non-standard cases and who to notify.
8. **Quality Checks:** Verification gate before mark as done.
9. **Completion Criteria:** Observable definition of done.

*Rule: If any step cannot be determined from available data, flag with HUMAN INPUT REQUIRED rather than inventing procedures.*
