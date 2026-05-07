# Existing PDF Work

Use this reference for inspection, extraction, form filling, merging, splitting,
and diagnosis.

## Inspect First

```bash
python scripts/pdf_toolkit.py inspect --input input.pdf --out inspect.json
```

Check:

- page count and page sizes
- encryption
- metadata
- form fields
- text extraction length per page

## Render For Layout

```bash
python scripts/pdf_toolkit.py render --input input.pdf --outdir rendered --dpi 160
```

Rendered PNGs are the fastest way to catch blank pages, glyph problems,
cropping, and overlap.

## Extract Text

```bash
python scripts/pdf_toolkit.py extract --input input.pdf --out extracted.txt
```

Use extracted text for content review, but do not trust it for layout fidelity.
PDF text order may differ from visible order.

## Fill Forms

Always inspect first to get exact field names:

```bash
python scripts/pdf_toolkit.py inspect --input form.pdf
python scripts/pdf_toolkit.py fill --input form.pdf --out filled.pdf --values values.json
```

Use string values for text/dropdowns. Use `true` or `false` for checkboxes.

## Merge PDFs

```bash
python scripts/pdf_toolkit.py merge --out combined.pdf part1.pdf part2.pdf
```

After merging, inspect page count and render boundary pages.

## Editing Limits

PDF is a final-form format. For substantial content edits, prefer editing the
source DOCX/Markdown/HTML and regenerating the PDF. Direct PDF surgery is best
for forms, metadata, page operations, and light annotations.
