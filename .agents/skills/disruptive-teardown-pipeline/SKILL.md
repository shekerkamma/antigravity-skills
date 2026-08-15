---
name: disruptive-teardown-pipeline
description: End-to-end pipeline to map 25 agentic use cases against legacy competitors. Runs the Competitor Product Teardown (Prompt #6) to identify pricing, feature gaps, and positioning strategy. Outputs a deep-dive market research dossier for each use case to prove our disruptive strategy.
---

# Disruptive Competitor Teardown Pipeline

This skill acts as the **Market Research & Disruptive Strategy Engine**. Its goal is to prove our deep market knowledge by mapping out the legacy incumbents for our 25 Agentic Use Cases, tearing down their products, and defining exactly how our disruptive AI-native approach wins.

## The Goal
For every use case defined in the scorecard (`resources/Agent_Use_Cases.md`), identify the top 5-10 legacy competitors/incumbents (e.g., Zendesk, BambooHR, Salesforce CPQ, etc.) and run a deep competitor teardown.

## The Execution Loop

1. **Read the Target:** Pick the next use case from `resources/Agent_Use_Cases.md`.
2. **Discover Competitors:** Use `search_web` to find the 5-10 legacy incumbents that currently dominate this specific workflow. (Look for the expensive, bloated platforms that require "human middleware").
3. **Execute the Teardown (Prompt #6 Logic):**
   Gather the following for the competitors:
   - **Company Overview:** Name, approximate stage/size, primary positioning.
   - **Product Teardown:** Top 3 features, pricing tiers (look for expensive per-seat models), and onboarding friction.
   - **Where they are strong:** What makes them sticky (e.g., integrations, system of record).
   - **Where they are weak:** The bloated, manual workflows that frustrate users.
4. **Formulate the Disruptive Strategy:**
   - Which 2 competitors are the most direct threat?
   - Which features are table stakes?
   - What must we deliberately NOT do (e.g., don't build a new database, just sit on top of theirs)?
   - What are the 3 specific gaps our Agentic Wedge exploits to destroy their $100K/9-month model?
5. **Output:** Compile a `[UseCaseName]_Competitor_Teardown.md` dossier in the workspace.

## When to Stop
Run this loop autonomously until all 25 use cases have a corresponding Competitor Teardown dossier. Do not hallucinate pricing or features; if you cannot find exact public pricing, explicitly state that it is hidden behind enterprise sales walls (which is itself a point of friction we disrupt).
