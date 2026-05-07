# PDF Validation

Use this reference before delivering a PDF.

## Structural Checks

```bash
python scripts/pdf_toolkit.py inspect --input output.pdf --out output.inspect.json
```

Confirm:

- file exists and is non-empty
- page count is expected
- page sizes are expected
- PDF is not encrypted unless requested
- form fields were filled if applicable
- text is extractable when the PDF should be searchable

## Visual Checks

```bash
python scripts/pdf_toolkit.py render --input output.pdf --outdir rendered --dpi 160
```

Inspect rendered pages for:

- blank pages
- clipped text
- overlapping text or tables
- missing CJK glyphs
- unreadable small type
- low contrast
- stretched images
- page header/footer collisions
- incorrect page numbering

## Cross-Platform Rendering

Preferred renderer is PyMuPDF (`fitz`) because it is cross-platform and does not
require Poppler. Poppler is also acceptable:

```bash
pdftoppm -png -r 160 output.pdf rendered/page
```

## Reporting

State:

- output PDF path
- source path(s)
- inspect JSON path if generated
- rendered PNG directory
- any remaining limitations
