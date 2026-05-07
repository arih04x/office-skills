# OpenXML Rules

Use these rules for every DOCX task.

## Package Model

A `.docx` file is a ZIP package with typed parts. Prefer SDK objects from:

```csharp
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
```

Common parts:

| Part | Purpose |
| --- | --- |
| `MainDocumentPart` | Body, sections, paragraphs, tables |
| `StyleDefinitionsPart` | Paragraph, character, table, and numbering styles |
| `NumberingDefinitionsPart` | Bullets and numbering |
| `HeaderPart` / `FooterPart` | Section-linked headers and footers |
| `ImagePart` | Images referenced by drawing elements |
| `DocumentSettingsPart` | Compatibility and document settings |

## Element Order

OpenXML is order-sensitive. Keep properties before content.

| Parent | Required order |
| --- | --- |
| `w:p` | `pPr` before runs |
| `w:r` | `rPr` before text, breaks, tabs, fields |
| `w:tbl` | `tblPr`, `tblGrid`, then rows |
| `w:tr` | `trPr`, then cells |
| `w:tc` | `tcPr`, then block content; include at least one paragraph |
| `w:body` | block content, then final `sectPr` |

## Styles

- Assign content through style IDs such as `Title`, `Heading1`, `BodyText`,
  `TableText`.
- Heading styles require `OutlineLevel` values: heading 1 uses `0`, heading 2
  uses `1`, and so on.
- Set CJK fonts explicitly:

```csharp
new RunFonts
{
    Ascii = "Aptos",
    HighAnsi = "Aptos",
    EastAsia = "Microsoft YaHei",
    ComplexScript = "Aptos"
}
```

## Units

| Unit | Meaning |
| --- | --- |
| DXA | 1/20 point; 1 inch = 1440 DXA |
| EMU | Drawing unit; 1 inch = 914400 EMU |
| `w:sz` | Half-points; 12 pt = `24` |

## Sections

- The final section properties element is the last child of `w:body`.
- Section breaks inside the document live on the paragraph properties of the
  paragraph before the new section.
- Headers and footers are linked through relationship IDs in each section.

## Tables

- Define grid columns when column width matters.
- Use table styles for repeated visual patterns.
- Add one paragraph to every table cell.
- For formal reports, prefer border and spacing consistency over direct cell
  formatting scattered through the document.

## Fields

TOC, PAGE, DATE, REF, and SEQ fields can be represented with complex field runs.
Word updates field results when the user opens or refreshes the document. Use
field instructions as semantic placeholders instead of hard-coded page numbers.

## Tracked Changes

- Insertions use `w:ins` containing runs with `w:t`.
- Deletions use `w:del` containing runs with `w:delText`.
- Track-change author and date values should be explicit and consistent.

## Images

- Add images through an `ImagePart`, then reference the relationship ID in a
  drawing.
- Set meaningful alt text on drawing properties.
- Use EMU dimensions derived from intended physical size.
