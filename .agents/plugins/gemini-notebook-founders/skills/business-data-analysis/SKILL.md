---
name: business-data-analysis
description: Performs code-driven business data validation, hygiene checks, unit economic calculations, and strategic insight extraction.
argument-hint: [inputs or objective]
---

# Business Data Analysis & Hygiene Engine

Use this skill to inspect raw business datasets (ad spend, CRM exports, sales logs, web analytics, invoices) and compute validated unit economics.

## Phase 1: Data Hygiene & Validation (Pre-Check)

Before running calculations, run code to verify:
- **Missing Values:** Unpopulated critical fields (dates, amounts, customer IDs).
- **Duplicate Records:** Duplicate transactions or leads.
- **Inconsistent Naming:** Case mismatches, conflicting channel tags (e.g. cpc vs Google_Ads).
- **Date Matching:** Timezone discrepancies, mismatched date ranges between spend and revenue.
- **Suspicious Values / Outliers:** Negative costs, extreme spikes,  conversions.
- **Comparability:** Explicitly flag if any datasets should NOT be directly compared.

*Rule: Do not silently drop or impute questionable information. Explicitly report data quality anomalies.*

## Phase 2: Core Metric Calculation

Compute standard unit economics where data permits:
- Total Spend & Total Revenue
- Total Leads, MQLs, SQLs, and Paying Customers
- Cost per Lead (CPL) & Customer Acquisition Cost (CAC)
- Conversion Rate across funnel stages
- Return on Ad Spend (ROAS) / Revenue vs. Spend
- Customer Lifetime Value (LTV) & LTV:CAC Ratio
- Payback Period & Gross Margin

## Phase 3: Strategic Takeaways

Deliver clear analytical conclusions:
- **Best-Performing Areas:** Channels, campaigns, cohorts with strongest ROI.
- **Worst-Performing Areas:** Drain on resources / negative unit economics.
- **Unexpected Patterns & Anomalies:** Notable shifts in retention, seasonality, or ticket size.
- **Supported Decisions:** What actions the numbers definitively validate.
- **Unsupported Decisions:** What popular assumptions the data completely refutes.
