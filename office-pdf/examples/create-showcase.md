# Create Showcase Example

Request:

Create a polished PDF capability sheet that demonstrates office-pdf's ability to
generate searchable text, tables, callouts, charts, page numbers, and visual QA
previews.

Use:

- `scripts/pdf_toolkit.py`
- `references/create-pdf.md`
- `references/validation.md`

Run:

```bash
python scripts/pdf_toolkit.py create-demo --out examples/showcase/office-pdf-showcase.pdf
python scripts/pdf_toolkit.py inspect --input examples/showcase/office-pdf-showcase.pdf --out examples/showcase/office-pdf-showcase.inspect.json
python scripts/pdf_toolkit.py render --input examples/showcase/office-pdf-showcase.pdf --outdir examples/showcase/rendered --dpi 160
```
