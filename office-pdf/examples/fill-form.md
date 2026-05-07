# Fill Form Example

Request:

Inspect a fillable PDF, then write values into the exact form fields while
preserving the original file.

Use:

- `references/edit-existing-pdf.md`
- `scripts/pdf_toolkit.py`

Run:

```bash
python scripts/pdf_toolkit.py inspect --input form.pdf --out fields.json
python scripts/pdf_toolkit.py fill --input form.pdf --out filled.pdf --values values.json
python scripts/pdf_toolkit.py render --input filled.pdf --outdir rendered-filled
```
