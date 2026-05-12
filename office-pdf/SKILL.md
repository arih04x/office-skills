---
name: office-pdf
description: "Create, inspect, extract, render, fill, merge, split, and validate PDF files with cross-platform Python workflows. Use for PDF work: polished report/proposal PDFs, PDF visual QA, form field inspection/filling, text/table extraction, PDF page rendering to PNG, PDF repair diagnostics, combining PDFs, converting structured content to PDF, or checking PDF print/readability quality."
---

# Office PDF

Use this skill for PDF tasks. Python-first, cross-platform pipeline.

## Operating Model

- Python 3.11+ with `reportlab`, `pypdf`, `pdfplumber`, `PyMuPDF`, Pillow, matplotlib.
- Use `scripts/pdf_toolkit.py` for repeatable operations (inspect, render, create-demo, merge, fill).
- Preserve source PDF; write output to a separate file.
- For CJK: verify font availability and render to PNG before delivery.

## Task Selection

| Task | Read | Focus |
| --- | --- | --- |
| Create polished PDF | `references/create-pdf.md` | ReportLab, style tokens, headers/footers, tables, charts |
| Inspect/extract/diagnose | `references/edit-existing-pdf.md` | pypdf, pdfplumber, visual rendering |
| Fill PDF forms | `references/edit-existing-pdf.md` | Inspect field names first, then write values |
| Validate layout | `references/validation.md` | Render to PNG, check text fit, page boxes, metadata |
| Quality bar | `references/pdf-quality.md` | Typography, accent color, spacing, output checks |

Read the matching reference, implement, validate with `scripts/pdf_toolkit.py inspect` + `render`.

## Key Rules

- PDF for fixed layout/print; DOCX when user needs Word editing.
- No bitmap-only PDFs unless explicitly requested.
- Body text readable at A4/Letter scale; one accent color; stable margins.
- Form filling: never guess field names — inspect first.
- Extraction: state it's not layout-perfect unless visual review confirms.
