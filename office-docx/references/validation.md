# Validation

Use this reference after creating, editing, or formatting a DOCX.

## Build Check

Run the task project:

```powershell
dotnet build
dotnet run -- <task arguments>
```

Resolve compiler warnings when they indicate nullable path or missing part
assumptions.

## OpenXML Validation

Use `OpenXmlValidator` in C#:

```csharp
using DocumentFormat.OpenXml.Validation;

using var doc = WordprocessingDocument.Open(path, false);
var validator = new OpenXmlValidator();
var errors = validator.Validate(doc).ToList();
foreach (var error in errors)
{
    Console.WriteLine($"{error.Path.XPath}: {error.Description}");
}
```

Validation errors should be addressed before delivery. Common causes:

- Element ordering problems.
- Missing required paragraphs in table cells.
- Invalid relationship IDs.
- Section properties in the wrong location.
- Drawing dimensions or required children omitted.

## Structural Sanity Checks

Print or assert expected counts:

- Paragraphs, headings, tables, rows, images.
- Sections and header/footer references.
- Styles used by generated content.
- Placeholder count after filling.

## Word-Openability Check

For important deliverables, open the output in Microsoft Word. On Windows, Word
automation can export to PDF for a visual check:

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open((Resolve-Path ".\out.docx").Path)
$doc.ExportAsFixedFormat((Resolve-Path ".\out.pdf").Path, 17)
$doc.Close($false)
$word.Quit()
```

Use this when the user cares about visible layout, page breaks, headers,
footers, TOC display, or complex tables.

## Output Report

State:

- Output `.docx` path.
- Validation result.
- Visual check result when performed.
- Any remaining manual Word actions, such as updating a TOC field.
