# Validation

Use this reference after creating or editing PPTX files.

## PowerPoint PNG Export

When desktop PowerPoint is available, export slides to PNG using the helper:

```powershell
.\scripts\export-pptx-png.ps1 -Pptx .\out.pptx -Out .\png
```

The PNG export uses PowerPoint's own renderer and is the preferred visual QA
surface for this Windows environment.

## macOS / Linux Fallback

If PowerPoint automation is unavailable, do one of these:

- Open the `.pptx` manually in PowerPoint, Keynote, or LibreOffice Impress and
  inspect layout.
- If LibreOffice is installed, convert to PDF and render PNG previews:

  ```bash
  mkdir -p pdf png
  soffice --headless --convert-to pdf --outdir pdf out.pptx
  pdftoppm -png -r 180 pdf/out.pdf png/slide
  ```

Treat this as a compatibility preview. PowerPoint remains the reference
renderer for PowerPoint-native delivery.

## Visual Checks

Inspect exported PNGs for:

- cropped text
- low text contrast
- text overlap
- background image covering title areas
- warped or stretched images
- accidental readable text inside generated images
- missing assets

## File Checks

- Confirm `.pptx` exists and is non-empty.
- Confirm generated image files exist.
- Confirm output PNG count matches slide count when PNG export is run.

## Reporting

State:

- `.pptx` path
- generated asset path
- PNG export path if used
- style file used
- any limitations, such as PowerPoint being unavailable
