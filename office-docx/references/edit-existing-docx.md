# Edit Existing DOCX

Use this reference when modifying a user-provided `.docx`.

## Inspection

Start by copying the input file to the target output path. Inspect the output
copy while keeping the source unchanged.

Useful checks in C#:

- Count paragraphs, tables, images, headers, footers, comments, and sections.
- Print paragraph indexes and `InnerText` for locating insertion points.
- Inspect style IDs on relevant paragraphs.
- Inspect table dimensions before editing rows or cells.

## Text Replacement

Simple replacement is reliable when the search text is contained in one
`Text` element:

```csharp
foreach (var text in doc.MainDocumentPart!.Document.Descendants<Text>())
{
    if (text.Text.Contains(searchText, StringComparison.Ordinal))
    {
        text.Text = text.Text.Replace(searchText, replacement, StringComparison.Ordinal);
    }
}
```

For text spanning multiple runs, choose one of these approaches:

| Situation | Approach |
| --- | --- |
| Formatting can follow the paragraph's first run | Replace paragraph content and recreate runs |
| Formatting must be preserved exactly | Map character ranges across runs, then rewrite affected runs |
| Placeholder is controlled, such as `{{Name}}` | Keep placeholders in single runs when generating templates |

## Inserting Paragraphs

Insert after a located paragraph. Preserve style intent:

```csharp
var newPara = new Paragraph(
    new ParagraphProperties(new ParagraphStyleId { Val = "Heading2" }),
    new Run(new Text("New Section")));
targetParagraph.InsertAfterSelf(newPara);
```

## Editing Tables

- Locate tables by index only after confirming the table count.
- Prefer locating by nearby heading text for durable edits.
- Reuse existing row and cell properties when adding similar rows.
- Ensure every new cell contains at least one paragraph.

## Headers and Footers

Headers and footers are section-linked. Inspect section properties before editing
them. For documents with multiple sections, apply changes to the intended
section references only.

## Images

When replacing an image, update the relevant image part or replace the drawing
relationship. Keep dimensions and alt text aligned with the surrounding layout.

## Minimal Change Discipline

After editing, compare before and after:

- Paragraph count changes only where expected.
- Table dimensions match the requested change.
- Styles and section count remain stable unless the task changed them.
