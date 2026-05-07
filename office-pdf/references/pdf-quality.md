# PDF Quality Rules

The goal is a PDF that survives both screen reading and print review.

## Quality Bar

- Page count, page size, and metadata are intentional.
- Text is searchable unless the user asked for scanned/image-only output.
- Margins, headers, footers, page numbers, and section spacing are consistent.
- Tables do not clip text.
- Images and charts render sharply.
- Body text remains readable at normal A4/Letter print scale.
- A rendered PNG preview has no overlap, cropped text, missing glyphs, or blank
  pages.

## Design System

- Choose one semantic accent color from the document purpose.
- Use restrained typography: one display face and one body face if custom fonts
  are available, otherwise standard PDF-safe fonts.
- Keep accent usage limited to rules, callout borders, table headers, and small
  metadata marks.
- Avoid gradients, decorative shadows, heavy backgrounds, and card-heavy pages
  unless the PDF is explicitly presentation-like.
- Use stable spacing tokens rather than ad hoc coordinates.

## Better Than A One-Off Generator

This skill should improve on a single create pipeline by adding:

- visual rendering as a validation gate
- text extraction checks
- form field inspection and filling
- merge/extract workflows for existing PDFs
- cross-platform Python defaults
- clear source artifact retention

## CJK Notes

- Confirm that chosen fonts contain required CJK glyphs.
- If ReportLab built-in fonts cannot render CJK text, register a local TTF/TTC
  font in the task script.
- Always render at least the first page to PNG and inspect glyph output.
