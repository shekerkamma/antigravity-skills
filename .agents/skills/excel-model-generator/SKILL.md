---
name: excel-model-generator
description: Generates structured financial models, unit economics sheets, and 3-scenario forecasts (Conservative, Base, Aggressive) with sensitivity analysis.
argument-hint: [inputs or objective]
---

# Excel & Financial Model Generator

Use this skill to convert pricing hypotheses, customer counts, cost structures, and growth estimates into transparent, formula-driven financial models.

## Structure of the Model

Organize models into clearly delineated sections:

### 1. Inputs & Assumptions Table
- All editable drivers (Pricing, CAC, Conversion Rate, Churn Rate, Capacity, Contractor Rates, Software Overhead).
- *Rule: If any number is missing from source data, do NOT invent it. Mark clearly as INPUT REQUIRED.*

### 2. Revenue Projections
- Monthly Recurring Revenue (MRR) & Annual Run Rate (ARR).
- Expansion revenue and cohort decay.

### 3. Cost Architecture
- **Fixed Costs:** Overhead, foundational SaaS subscriptions, core salaries.
- **Variable Costs:** Contractor fees, API token costs, hosting, payment processing fees per transaction.

### 4. Unit Economics Summary
- Gross Margin & Contribution Margin (%)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (LTV) & LTV:CAC ratio
- Payback Period (in months)
- Average Revenue Per User/Account (ARPU)

### 5. Three-Scenario Analysis
1. **Conservative Case:** Lower conversion (-30%), higher CAC (+25%), elevated churn.
2. **Base Case:** Target plan based on validated historical benchmarks.
3. **Aggressive Case:** Viral adoption / faster sales velocity with stable margins.

### 6. Sensitivity Analysis
- Identify the single driver with the highest leverage on bottom-line profitability (e.g. churn vs CAC vs pricing).
