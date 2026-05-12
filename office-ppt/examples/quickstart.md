# Quickstart

## Create a slide with a mock placeholder image
```bash
cd office-ppt/assets/node-starter && node index.js --title "Hello" --mock
```

## Create a slide with a real image API (GPT-image style)
```bash
cd office-ppt/assets/node-starter && node index.js --title "Hello" --style onij
# Requires OFFICE_SKILLS_ENV or config/office-skills.local.env with API keys
```

## Export PPTX to PNG (Windows, requires PowerPoint)
```powershell
powershell -File office-ppt/scripts/export-pptx-png.ps1 -Path out/deck.pptx -OutDir out/slides
```

## Validate a PPTX file
```bash
python office-ppt/scripts/check-pptx.py out/deck.pptx
```
