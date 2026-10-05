# Master Slide Template Design Spec

This specification dictates the visual language for any slide deck generated via the `master-template-slides` skill. It translates the modern, dark-mode, glassmorphism UI aesthetic into a `python-pptx` executable format.

## 1. Color Palette (RGB Values for PPTX)

When using `python-pptx`, colors must be defined in RGB format. Use these exact values:

* **Backgrounds**
  * `BG_BASE`: RGB `(5, 11, 20)` - Represents the deep, rich navy/black base (`hsl(222, 47%, 4%)`).
  * `BG_CARD`: RGB `(15, 23, 42)` - Represents the glass panel background (`hsl(222, 47%, 11%)`).
  
* **Text Colors**
  * `TEXT_PRIMARY`: RGB `(248, 250, 252)` - Crisp white for titles and primary data (`hsl(210, 40%, 98%)`).
  * `TEXT_MUTED`: RGB `(148, 163, 184)` - Soft blue-grey for subtitles and body (`hsl(215, 20%, 65%)`).

* **Accents (Shapes & Lines)**
  * `ACCENT_PRIMARY`: RGB `(59, 130, 246)` - Neon blue for active states/highlights (`hsl(217, 100%, 60%)`).
  * `ACCENT_GLOW`: RGB `(168, 85, 247)` - Purple for gradients/premium elements (`hsl(267, 100%, 68%)`).
  * `BORDER_SUBTLE`: RGB `(43, 62, 85)` - For slide borders or dividers.

## 2. Typography & Sizing

Ensure all text frames in the PPTX are configured properly:
* **Font Family:** `Arial` or `Helvetica` (System safe sans-serif fallbacks for `Inter`/`Outfit`).
* **Title Slide Main Header:** 44pt, Bold, `TEXT_PRIMARY`.
* **Slide Header (Top):** 36pt, Bold, `TEXT_PRIMARY`.
* **Subtitle/Sub-header:** 24pt, `TEXT_MUTED`.
* **Body Text / Bullets:** 18pt or 20pt, `TEXT_MUTED`.

## 3. Layout Blueprint Rules

When generating `python-pptx` code, follow these layout structures:

1. **Global Background:**
   Every slide must have its background color set to `BG_BASE`.
   ```python
   background = slide.background
   fill = background.fill
   fill.solid()
   fill.fore_color.rgb = RGBColor(5, 11, 20)
   ```

2. **The "Glass Panel" Effect:**
   For content sections, draw a rounded rectangle (shape type: `MSO_SHAPE.ROUNDED_RECTANGLE`) behind the text.
   * Fill: `BG_CARD`
   * Line: `BORDER_SUBTLE`
   * This acts as the "card" holding the data, simulating the web UI component.

3. **Accent Lines:**
   Draw a thin rectangle (2pt to 4pt height) across the top of the slide or above key headers using `ACCENT_PRIMARY` or `ACCENT_GLOW` to mimic a dynamic UI highlight.

4. **Consistency:**
   Do not use default PowerPoint themes. Apply the RGB colors explicitly to all text, lines, and backgrounds to guarantee the master aesthetic is preserved.
