# Office Integration

Use this reference when the figure will be inserted into Word or PowerPoint.

## Word

Preferred delivery:

- editable source: `.drawio` or `.tex`
- insertion asset: `.svg` for vector figures or `.png` for hybrid bitmap figures

If the user needs the document itself updated, use the DOCX skill to insert the
asset and keep the source file beside the document.

For small fully editable Word-native diagrams, use OpenXML DrawingML shapes.
This is useful for simple boxes, arrows, and labels. For complex figures,
maintain a `.drawio` source.

## PowerPoint

Preferred delivery:

- editable source: `.drawio`, `.svg`, or native PPT shapes
- insertion asset: `.svg` or `.png`

If the figure is part of a slide, use the PPT skill for native PPT composition.

## SVG vs PNG

| Asset | Use |
| --- | --- |
| SVG | clean vector diagrams, charts, text-light figures |
| PNG | generated imagery, textures, complex bitmap panels |
| PDF | LaTeX manuscript figure asset |

## Deliverable Set

For Office work, deliver at least:

- source file
- insertion asset
- generated image assets if used
- short note describing which file is editable
