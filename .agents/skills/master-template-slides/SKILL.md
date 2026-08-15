---
name: master-template-slides
description: Generate premium, editable PPTX slide decks locally using the branded-pptx-deck toolkit's compile.py. Acts as an orchestrated pipeline replacing Genspark AI by leveraging upstream AI analyst skills and downstream visual rendering through rich compile.py layouts (split, table, quotes_grid).
---

# Master Template Slides Workflow

Use this skill when the user wants to generate an editable presentation (PPTX) with a high-end, premium design aesthetic (Genspark Master Design Spec) and rich layouts (tables, splits, quotes grids), entirely locally without external dependencies. 

**CRITICAL:** Do NOT hand-roll `python-pptx` scripts or use raw `pptxkit.py` calls to build plain bullet slides. You MUST use the existing `compile.py` compiler from `branded-pptx-deck`!

## 1. Content Generation (Upstream)
You must **never** manually parse or draft slide content into plain text slides. 
1. Use `ai-analyst` or `presentation-content-writer` to generate structured findings into a `findings.json` file.
2. Ensure the JSON strictly adheres to the `compile.py` schema (tables, split views, quotes_grid, and bullets), mapping the strategic analysis to rich visual containers, rather than flat lists.

## 2. PPTX Compilation (Downstream)
Do NOT call Genspark. Do NOT write your own `build_deck.py` script.
1. Use the existing compiler: `.agents/skills/branded-pptx-deck/scripts/compile.py`.
2. Generate a blank template PPTX if one is not provided.
3. Run `python .agents/skills/branded-pptx-deck/scripts/compile.py findings.json blank.pptx Output.pptx`
4. The output will automatically feature the premium visual aesthetic encoded in the compiler.

## 3. Quality Assurance (Review Gate)
1. Run `python "C:\Users\sheke\.gemini\config\skills\branded-pptx-deck\scripts\preview_pptx.py" <Output.pptx> previews/` to generate visual contact sheets.
2. Provide the user with a clickable `file://` link to the generated `.pptx` file.
