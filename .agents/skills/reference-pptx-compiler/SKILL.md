---
name: reference-pptx-compiler
description: >
  Ingest any reference PPTX deck, map its text shape layouts, and compile new
  strategy/analytical findings into that reference style. This skill acts as a
  reusable "Reference In -> Styled Deck Out" style compiler.
---
# Reference PPTX Compiler Skill

This skill operates as a dynamic PowerPoint style-transfer engine. It extracts layout mappings from any reference presentation (like `template-superdesign.pptx` or any corporate deck) and injects dynamic findings into those layouts without hardcoding shape coordinates or indexes.

## The Fable Style Loop

### Step 1: Layout Mapping & Analysis (Ingestion)
Point the extractor script at a reference PPTX file. It generates a layout map JSON detailing all slides, shapes, text elements, and potential placeholders.

```bash
uv run --with python-pptx python .agents/skills/reference-pptx-compiler/scripts/map.py reference-deck.pptx layout-map.json
```

The script will auto-detect common consulting text areas (like headlines, executive summary paragraphs, and lists) and write a draft mapping schema. If needed, the user or agent can refine the mapping coordinates in `layout-map.json` manually.

### Step 2: Content Preparation
Prepare a findings payload matching the universal schema. Example:

```json
{
  "company": "TraceHeal",
  "domain": "SITUATION ASSESSMENT",
  "headline": "Active interception blocks agent failure states before execution",
  "executive_read": "Incumbent AI observability layers fail to intercept destructive action states. TraceHeal closes this gap by implementing real-time boundary evaluation.",
  "key_findings": [
    "90% of enterprises report silent AI failures as a blocker",
    "Current agents can trace but cannot block actions dynamically",
    "First-mover advantage exists in the active governance layer",
    "Standard integrations ensure zero lock-in for clients"
  ],
  "table_rows": [
    {"area": "Competitor Gaps", "evidence": "LangSmith/Datadog offer log trace only", "interpretation": "No interception layer exists", "confidence": "High"},
    {"area": "Market Size", "evidence": "$1.23B observability market value", "interpretation": "Massive enterprise addressable area", "confidence": "High"}
  ]
}
```

### Step 3: Style Token Extraction (Theme Transfer)
Run the style token extractor to programmatically inspect the reference PPTX template and map out background colors, borders, neon accent highlights, and font metrics to dynamic tokens:

```bash
uv run python .agents/skills/reference-pptx-compiler/scripts/extract_brand.py reference-deck.pptx style-tokens.json
```

### Step 4: Programmatic Assembly (pptxkit.py integration)
Use the official `branded-pptx-deck` toolkit (`pptxkit.py`) to build the dynamic slide layouts (e.g., Cover, OSINT Map, Metrics Grid, Action Takeaways) programmatically. Import the extracted style tokens to instantiate the reskinned `Brand` config and construct the deck using slide primitives:

```python
sys.path.insert(0, r"C:\Users\sheke\.gemini\config\skills\branded-pptx-deck\scripts")
from pptxkit import Deck, Brand
d = Deck(brand=custom_brand, footer="...")
```

### Step 5: Visual QA Verification (preview_pptx.py)
Perform a downstream QA verification loop using the preview generator to render each slide as a PNG and check for text overlaps or height overflows:

```bash
uv run python "C:\Users\sheke\.gemini\config\skills\branded-pptx-deck\scripts\preview_pptx.py" output-deck.pptx previews/
```

Verify that all text height boxes fit comfortably inside shape coordinates, and adjust font sizes or shape dimensions to resolve any overflows.

