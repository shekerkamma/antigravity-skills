---
name: grill-codeex
description: >-
  Multi-model orchestration skill combining a primary agent (planning/review)
  with a secondary model via API (adversarial critique/code generation).
  Runs a 4-phase loop: deep interview, adversarial hardening, high-velocity
  build handoff, and code quality review with remediation. Use when the user
  wants to build a new feature or product from scratch and specifically
  requests "grill-codeex", "multi-model build", or a Fable+Sol orchestrated
  workflow.
category: Development Workflow
license: MIT
---

# Grill Codeex — Multi-Model Orchestration Skill

## Overview

Grill Codeex is a 4-phase development orchestration workflow that leverages
two frontier AI models together instead of choosing one:

- **Primary Agent (You)** — owns planning, discovery, and code review
- **Secondary Model (via API)** — owns adversarial critique and
  high-velocity code generation

The key insight: heavy text generation happens via a background Python script
(`sol_bridge.py`) executed outside the main chat context, preventing context
bloat and optimizing token expenditure.

## Prerequisites

1. The `sol_bridge.py` script is located at `.agents/skills/grill-codeex/sol_bridge.py`
2. **API Keys:** The bridge supports multiple providers. It will auto-detect
   and use the best available key in this order:
   `OPENROUTER_API_KEY` -> `GEMINI_API_KEY` -> `DEEPSEEK_API_KEY` -> `GROQ_API_KEY` -> `OPENAI_API_KEY`.
   The agent does NOT need to configure this; the script handles it.

---

## Execution Phases

### Phase 1: Grill Me (Deep Technical Interview)

**Owner:** Primary Agent (You)
**Goal:** Extract a precise, unambiguous engineering blueprint.

**Process:**
1. Present a welcome message explaining the 4-phase workflow.
2. Conduct an **8–10 turn** deep technical interview.
3. **CRITICAL:** Use the `ask_question` tool for EVERY interview turn.
   - Present 3-4 structured options
   - Label your recommended option with "(Recommended)"
   - The user can use the default write-in option if they want to elaborate.
4. **Questions must progress through:**
   - Turn 1-2: Purpose, audience, scope
   - Turn 3-4: Tech stack, framework, deployment
   - Turn 5-6: Data model, persistence, APIs
   - Turn 7-8: Security, authentication, edge cases
   - Turn 9-10: UX, performance, polish
5. **Dual-write Checkpointing:**
   - Create `ALIGNED_PLAN.md` immediately.
   - After *every* user answer, append the Q&A to a `## Interview Log` section at the bottom of the plan file.
6. After all questions are answered, synthesize the `## Interview Log` into proper plan sections in `ALIGNED_PLAN.md`:
   - Project Summary
   - Architecture Overview
   - Implementation Plan (files, components)
   - Out of Scope
   - Success Criteria

### Phase 2: Adversarial Loop (Critique & Consensus)

**Owner:** Secondary Model (via sol_bridge.py) ↔ Primary Agent (You)
**Goal:** Harden the plan against architectural weaknesses and security flaws.

**Process:**
1. Initialize `PLAN-REVIEW-LOG.md` with a header and timestamp.
2. **Loop (max 5 iterations):**
   - Run the bridge: `python .agents/skills/grill-codeex/sol_bridge.py --mode critique --plan ALIGNED_PLAN.md`
   - Read `PLAN-REVIEW-LOG.md` to see the new critique. (The script writes the critique to the log, NOT the plan).
   - Evaluate findings: agree, disagree, or partially agree.
   - Incorporate accepted changes directly into `ALIGNED_PLAN.md` using native file editing tools.
   - If no critical findings remain, consensus is reached. Exit loop.
3. After consensus, present 3 options via `ask_question`:
   - A. Let the script build it (Phase 3)
   - B. You build it directly (Skip Phase 3)
   - C. Stop here (Keep the hardened plan)

### Phase 3: Build Handoff (High-Velocity Generation)

**Owner:** Secondary Model (via sol_bridge.py)
**Goal:** Deploy code files to disk efficiently in a background process.

**Process:**
1. Determine the output directory based on the project name in the plan (e.g., `./trip-atlas/`). Default to `./build-output/` if unclear.
2. Execute the build bridge in the background:
   `python .agents/skills/grill-codeex/sol_bridge.py --mode build --plan ALIGNED_PLAN.md --output-dir <DIR>`
3. Wait for the task to finish. The script writes code files directly to disk.
4. The script writes `SOL_BUILD_MANIFEST.md` in the output directory.
5. **Truncation Warning:** If the script output indicates no valid file blocks or the generation was truncated (a known risk with context limits), inform the user that v1 does not support batching and they may need to split the plan.

### Phase 4: Code Quality Review & Remediation

**Owner:** Primary Agent (You) → Secondary Model
**Goal:** Validate the generated codebase and patch any issues.

**Process:**
1. Read `SOL_BUILD_MANIFEST.md` and read every file listed.
2. **CRITICAL SECURITY SCAN:** Explicitly check every generated file for:
   - Hardcoded API keys, secrets, or passwords
   - `eval()` or `exec()` in Python
   - `dangerouslySetInnerHTML` in React
   - SQL injection vulnerabilities
   - Unrestricted file access paths
   - Shell injections (`os.system`, `subprocess.run(shell=True)`)
3. Compare files against the `ALIGNED_PLAN.md` spec. Run local syntax checkers if available.
4. **Remediation rounds (max 2):**
   - If issues are found, document them in `PLAN-REVIEW-LOG.md`.
   - Update `ALIGNED_PLAN.md` with fix instructions.
   - Re-run the build bridge.
5. **Takeover:** If issues persist after 2 rounds, take over manual control. Use native file editing tools (`replace_file_content`) to patch the code directly.
6. Present the final codebase to the user for review or commit.
