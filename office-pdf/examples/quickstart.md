# Quickstart

## Create a polished demo PDF
```bash
python office-pdf/scripts/pdf_toolkit.py create-demo --out out/demo.pdf --title "My Report"
```

## Inspect an existing PDF (pages, metadata, form fields)
```bash
python office-pdf/scripts/pdf_toolkit.py inspect --input doc.pdf --out out/report.json
```

## Render PDF pages to PNG for visual QA
```bash
python office-pdf/scripts/pdf_toolkit.py render --input doc.pdf --outdir out/pages --dpi 160
```

## Fill a PDF form from JSON values
```bash
python office-pdf/scripts/pdf_toolkit.py fill --input form.pdf --values data.json --out out/filled.pdf
```

## Merge multiple PDFs into one
```bash
python office-pdf/scripts/pdf_toolkit.py merge --out out/combined.pdf a.pdf b.pdf c.pdf
```
