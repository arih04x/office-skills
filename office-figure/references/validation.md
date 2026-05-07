# Validation

Use this reference before delivering figures.

## Source Checks

- Confirm the editable source file exists.
- Confirm rendered assets exist.
- Confirm generated bitmap assets exist when used.
- Confirm labels and exact data are editable in source, not baked into a
  generated image.

## Visual Checks

Inspect the rendered asset:

- no clipped labels
- no overlapping arrows and text
- readable text at intended insertion size
- sufficient contrast
- consistent spacing and alignment
- no accidental generated readable text

## LaTeX Checks

When TeX is available:

```powershell
pdflatex figure.tex
pdftoppm -png -r 300 figure.pdf figure
```

Check the PDF and PNG preview for overfull labels, cropped content, font
mismatches, and inconsistent series colors. If TeX or Poppler is unavailable,
record that rendering is pending and keep the `.tex` source complete.

## Draw.io Checks

Open the `.drawio` in diagrams.net when possible, or inspect the XML for
expected labels and image references. Export SVG or PNG when an exporter is
available.

On Windows PowerShell, read Chinese `.drawio` files as UTF-8 when doing XML
checks:

```powershell
[xml](Get-Content -Raw -Encoding UTF8 .\figure.drawio)
```

## Office Checks

When inserted into Word or PowerPoint, verify:

- size and aspect ratio
- text readability
- no unexpected raster blur
- source file retained beside the Office file
