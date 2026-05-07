# Create PPTX

Use this reference when creating a PowerPoint slide or deck.

## PptxGenJS Setup

```javascript
import pptxgen from "pptxgenjs";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "ARIHOAX Office";
pptx.subject = "Generated PowerPoint";
pptx.title = "Slide Title";
```

## Slide Construction

- Use a 13.333 x 7.5 inch canvas for 16:9.
- Add generated background or local visual images first.
- Add translucent overlays only when needed for text contrast.
- Add all exact text as native PowerPoint text.
- Use consistent positions across related slides.
- Add charts, arrows, tables, formulas, legends, numeric values, and important
  callouts as native PowerPoint objects, not inside generated images.
- Keep generated images as editable/replaceable image objects, not flattened
  full-slide screenshots with baked-in copy.

Example:

```javascript
const slide = pptx.addSlide();
slide.background = { color: "0F172A" };
slide.addImage({ path: "assets/background.png", x: 0, y: 0, w: 13.333, h: 7.5 });
slide.addShape(pptx.ShapeType.rect, {
  x: 0, y: 0, w: 13.333, h: 7.5,
  fill: { color: "000000", transparency: 38 },
  line: { color: "000000", transparency: 100 }
});
slide.addText("Title", {
  x: 0.75, y: 0.65, w: 8.2, h: 0.75,
  fontFace: "Microsoft YaHei",
  fontSize: 30,
  bold: true,
  color: "FFFFFF",
  margin: 0
});
```

## Text Rules

- Use short titles.
- Keep body copy compact.
- Keep all labels outside generated images.
- Use consistent font face and color hierarchy.

## Output

Use:

```javascript
await pptx.writeFile({ fileName: outputPptx });
```

After writing the `.pptx`, export slides to PNG with desktop PowerPoint when
available and inspect the rendered images for cropped text, low contrast,
misplaced overlays, unreadable type, and image/text alignment. Include the
exported PNG paths with the final `.pptx` deliverable.
