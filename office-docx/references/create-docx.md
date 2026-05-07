# Create DOCX

Use this reference when creating a new Word document from content or a brief.

## Planning

Decide these items before coding:

- Document type: report, memo, manuscript, contract, proposal, meeting notes, or
  custom.
- Page size and margins: A4 is common for Chinese and formal reports; Letter is
  common for US work.
- Structure: title, metadata, abstract/summary, sections, tables, figures,
  appendices, references.
- Style set: title, subtitle, heading levels, body, caption, table text,
  footnote, code, quote.
- CJK requirements: East Asian font, line spacing, punctuation behavior, heading
  hierarchy.

## Minimal Creation Pattern

```csharp
using var doc = WordprocessingDocument.Create(outputPath, WordprocessingDocumentType.Document);
var mainPart = doc.AddMainDocumentPart();
mainPart.Document = new Document(new Body());
AddStyles(mainPart);

var body = mainPart.Document.Body!;
body.Append(Paragraph("Report Title", "Title"));
body.Append(Paragraph("Executive Summary", "Heading1"));
body.Append(Paragraph("This paragraph is editable Word text.", "BodyText"));
body.Append(CreateSectionPropertiesA4());

mainPart.Document.Save();
```

## Content Rules

- Build real Word paragraphs, runs, lists, and tables.
- Keep titles and headings as text, not as images.
- Use table structures for tabular content. Use captions for figures and tables
  when the document is academic or formal.
- Add document properties such as title and author when requested.
- Use semantic styles early. Avoid setting every paragraph manually.

## Lists and Numbering

Create numbering definitions when the document needs stable bullets or legal
numbering. For short informal documents, simple bullet paragraph properties are
acceptable.

## Tables

For a standard table:

1. Create `TableProperties`.
2. Create `TableGrid` with explicit widths.
3. Add a header row when appropriate.
4. Add cells with `TableCellProperties` and at least one paragraph.
5. Apply borders and shading through table or cell properties.

## Images

Use `ImagePart` and drawing elements. Store the source image beside the task
project or pass its full path. Set width and height in EMUs, and include alt
text.

## TOC

For documents with multiple heading levels, add a TOC field and heading styles
with outline levels. Word can update the TOC when opened.
