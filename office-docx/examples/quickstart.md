# Quickstart

## Create a report from the dotnet starter
```bash
cd office-docx/assets/dotnet-starter && dotnet run
```

## Edit/replace text in an existing DOCX
```bash
# Use OpenXML SDK — open, find-replace in body paragraphs, save
dotnet add package DocumentFormat.OpenXml
# In code: WordprocessingDocument.Open(path, true) → body.Descendants<Text>()
```

## Apply a template (styles + layout from a reference DOCX)
```bash
# Copy styles.xml and settings.xml from template.docx into target.docx ZIP
# Then rebuild relationships — see references/create-docx.md
```

## Validate output
```bash
python office-docx/scripts/check-docx.py out/report.docx
```
