---
name: office-pdf
description: "Create, inspect, extract, render, fill, merge, split, and validate PDF files with cross-platform Python workflows. Use for PDF work: polished report/proposal PDFs, PDF visual QA, form field inspection/filling, text/table extraction, PDF page rendering to PNG, PDF repair diagnostics, combining PDFs, converting structured content to PDF, or checking PDF print/readability quality."
---

# Office PDF

Use this skill when the requested output or source file is a PDF, or when the
task requires PDF rendering, inspection, extraction, form filling, or visual QA.

Prefer a Python-first, cross-platform pipeline. Use browser rendering only when
the task explicitly needs HTML/CSS fidelity. Visual quality matters: render the
result to PNG and inspect the pages before delivery whenever layout matters.

## Operating Model

- Use Python 3.11+ with `reportlab`, `pypdf`, `pdfplumber`, `PyMuPDF` (`fitz`),
  Pillow, and matplotlib when available.
- Copy or adapt `scripts/pdf_toolkit.py` for deterministic repeated operations.
- Preserve the user's source PDF. Write changed output to a separate file.
- Keep reusable source beside rendered PDFs: JSON content, Markdown source,
  input data, or script used to create the PDF.
- For CJK documents, verify font availability and render pages to PNG before
  delivery.

## Task Selection

| Task | Read | Implementation focus |
| --- | --- | --- |
| Create a polished PDF | `references/create-pdf.md` | Build structured content with ReportLab, style tokens, headers/footers, tables, charts, and source data |
| Inspect, extract, or diagnose an existing PDF | `references/edit-existing-pdf.md` | Use `pypdf`, `pdfplumber`, and visual rendering; preserve the original |
| Fill PDF forms | `references/edit-existing-pdf.md` | Inspect exact field names first, then write values with `pypdf` |
| Validate layout or print readiness | `references/validation.md` | Render pages to PNG, inspect text fit, page boxes, metadata, and page count |
| Decide quality bar and visual system | `references/pdf-quality.md` | Choose restrained typography, semantic accent, stable spacing, and output checks |

## Implementation Steps

1. Classify the task: create, inspect, extract, fill, merge, split, render, or
   mixed.
2. Open the matching reference file before writing or running code.
3. Use `scripts/pdf_toolkit.py` when it covers the operation:

   ```bash
   python scripts/pdf_toolkit.py inspect --input input.pdf
   python scripts/pdf_toolkit.py render --input input.pdf --outdir rendered
   python scripts/pdf_toolkit.py create-demo --out out.pdf
   ```

4. For custom documents, create task-local source files and keep them with the
   output.
5. Validate the output with `inspect` and `render`.
6. Report output PDF, source files, rendered previews, and any residual
   limitations.

## Design Rules

- Use PDF when the final artifact is meant for fixed layout or print.
- Use DOCX when the user needs rich Word editing after delivery.
- Avoid bitmap-only PDFs unless the user explicitly wants scans or image-backed
  pages.
- Keep body text readable at normal zoom and printed A4/Letter scale.
- Use one semantic accent color, stable margins, and consistent headers/footers.
- For form filling, never guess field names. Inspect first.
- For extraction, state that text extraction is not layout-perfect unless visual
  review confirms it.

## Resources

- `scripts/pdf_toolkit.py`: cross-platform helper for create-demo, inspect,
  render, extract, merge, and fill.
- `references/create-pdf.md`: creating new PDFs.
- `references/edit-existing-pdf.md`: inspecting, extracting, filling, merging,
  and diagnosing existing PDFs.
- `references/validation.md`: visual and structural PDF checks.
- `references/pdf-quality.md`: quality bar and design rules.
- `examples/`: implementation briefs and showcase outputs.
