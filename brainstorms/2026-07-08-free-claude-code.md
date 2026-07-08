# Free Claude Code: Brainstorm & Discovery Notes
Date: 2026-07-08 · Goal: Design a reusable agent skill/plugin for configuring, running, and troubleshooting the Free Claude Code proxy.

## Structured context
- **Topic type**: product-design
- **Topic string**: Reusable agent instructions for managing the Free Claude Code proxy.

## Brainstorm Decisions & Self-Answers

### 1. Scope & Purpose
* **Goal:** Create a global agent capability that teaches future agents how to configure, launch, troubleshoot, and switch models within the `free-claude-code` proxy.
* **Scope:** Text-only instruction capability describing configuration rules, active ports, startup paths, and model selection.

### 2. Inputs & Outputs
* **Inputs:** Natural language instructions to "switch model to X", "check server status", or "start fcc-claude".
* **Outputs:** 
  * Re-configured `.env` variables in `~/.fcc/.env`.
  * Correct direct execution of wrapper scripts.
  * Verified server status checking.

### 3. Rigidity vs. Flexibility
* **Strict Steps:**
  * Must use direct environment executable paths (`C:\Users\sheke\AppData\Roaming\uv\tools\free-claude-code\Scripts\fcc-*.exe`) instead of global alias wrappers.
  * Modifications to configuration must target `C:\Users\sheke\.fcc\.env`.
* **Flexible Steps:** Any valid model slug can be routed as long as the provider credential keys are verified.

### 4. Implementation Location & Path (Deciding on Skill vs. Plugin)
* **Comparison & Evaluation:**
  * **Option A (Skill):** Keeps everything in a single global `SKILL.md` under `C:\Users\sheke\.gemini\config\skills\free-claude-code\SKILL.md`. Very simple to maintain, but lacks modular grouping for the future.
  * **Option B (Plugin - Recommended):** Packages the capability under a global plugin directory: `C:\Users\sheke\.gemini\config\plugins\free-claude-code-plugin/`. 
    * Structure: Includes a `plugin.json` descriptor file and a nested `skills/free-claude-code/SKILL.md` directory.
    * Benefit: Standardizes this setup. Allows us to easily bundle other tools, scripts, or custom subagents under the same plugin namespace in the future.
* **Final Choice:** Overwhelmingly **Option B (Plugin)**. Standardizing it as a plugin is cleaner and provides future-proof modularity.

## Open flags
*None.*
