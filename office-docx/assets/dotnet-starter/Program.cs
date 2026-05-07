using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Validation;
using DocumentFormat.OpenXml.Wordprocessing;

var outputPath = args.Length > 0
    ? args[0]
    : Path.Combine(Directory.GetCurrentDirectory(), "office-docx-starter.docx");

Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(outputPath))!);
CreateSampleDocument(outputPath);
ValidateDocument(outputPath);
Console.WriteLine($"Created: {outputPath}");

static void CreateSampleDocument(string outputPath)
{
    using var doc = WordprocessingDocument.Create(outputPath, WordprocessingDocumentType.Document);
    var mainPart = doc.AddMainDocumentPart();
    mainPart.Document = new Document(new Body());
    AddStyles(mainPart);

    var body = mainPart.Document.Body!;
    body.Append(Paragraph("Office DOCX Showcase", "Title"));
    body.Append(Paragraph("A compact Word document generated with .NET and the OpenXML SDK.", "Subtitle"));
    body.Append(Paragraph("Summary", "Heading1"));
    body.Append(Paragraph(
        "This document is fully editable Word content: headings, paragraphs, tables, styles, page setup, and validation are created through OpenXML SDK object APIs.",
        "BodyText"));
    body.Append(Paragraph("Capability Snapshot", "Heading1"));
    body.Append(CapabilityTable());
    body.Append(Paragraph("Quality Rules", "Heading1"));
    body.Append(Paragraph(
        "Keep source documents untouched, write a separate output file, preserve editable Word structures, and validate the package before delivery.",
        "BodyText"));
    body.Append(CreateSectionPropertiesA4());

    mainPart.Document.Save();
}

static Paragraph Paragraph(string text, string styleId)
{
    return new Paragraph(
        new ParagraphProperties(new ParagraphStyleId { Val = styleId }),
        new Run(new Text(text) { Space = SpaceProcessingModeValues.Preserve }));
}

static void AddStyles(MainDocumentPart mainPart)
{
    var stylesPart = mainPart.AddNewPart<StyleDefinitionsPart>();
    stylesPart.Styles = new Styles(
        new Style(
            new StyleName { Val = "Normal" },
            new PrimaryStyle(),
            new StyleRunProperties(
                new RunFonts
                {
                    Ascii = "Aptos",
                    HighAnsi = "Aptos",
                    EastAsia = "Microsoft YaHei",
                    ComplexScript = "Aptos"
                },
                new FontSize { Val = "22" }))
        {
            Type = StyleValues.Paragraph,
            StyleId = "Normal",
            Default = true
        },
        new Style(
            new StyleName { Val = "Title" },
            new BasedOn { Val = "Normal" },
            new PrimaryStyle(),
            new StyleParagraphProperties(
                new SpacingBetweenLines { Before = "0", After = "240" },
                new Justification { Val = JustificationValues.Center }),
            new StyleRunProperties(
                new Bold(),
                new FontSize { Val = "36" }))
        {
            Type = StyleValues.Paragraph,
            StyleId = "Title"
        },
        new Style(
            new StyleName { Val = "Subtitle" },
            new BasedOn { Val = "Normal" },
            new PrimaryStyle(),
            new StyleParagraphProperties(
                new SpacingBetweenLines { Before = "0", After = "240" },
                new Justification { Val = JustificationValues.Center }),
            new StyleRunProperties(
                new Color { Val = "4B5563" },
                new FontSize { Val = "22" }))
        {
            Type = StyleValues.Paragraph,
            StyleId = "Subtitle"
        },
        new Style(
            new StyleName { Val = "heading 1" },
            new BasedOn { Val = "Normal" },
            new NextParagraphStyle { Val = "BodyText" },
            new PrimaryStyle(),
            new StyleParagraphProperties(
                new KeepNext(),
                new SpacingBetweenLines { Before = "240", After = "120" },
                new OutlineLevel { Val = 0 }),
            new StyleRunProperties(
                new Bold(),
                new FontSize { Val = "28" }))
        {
            Type = StyleValues.Paragraph,
            StyleId = "Heading1"
        },
        new Style(
            new StyleName { Val = "Body Text" },
            new BasedOn { Val = "Normal" },
            new StyleParagraphProperties(
                new SpacingBetweenLines { After = "120", Line = "360", LineRule = LineSpacingRuleValues.Auto }))
        {
            Type = StyleValues.Paragraph,
            StyleId = "BodyText"
        });
    stylesPart.Styles.Save();
}

static Table CapabilityTable()
{
    var table = new Table(
        new TableProperties(
            new TableWidth { Width = "5000", Type = TableWidthUnitValues.Pct },
            new TableBorders(
                new TopBorder { Val = BorderValues.Single, Size = 6, Color = "CBD5E1" },
                new LeftBorder { Val = BorderValues.Single, Size = 6, Color = "CBD5E1" },
                new BottomBorder { Val = BorderValues.Single, Size = 6, Color = "CBD5E1" },
                new RightBorder { Val = BorderValues.Single, Size = 6, Color = "CBD5E1" },
                new InsideHorizontalBorder { Val = BorderValues.Single, Size = 4, Color = "E5E7EB" },
                new InsideVerticalBorder { Val = BorderValues.Single, Size = 4, Color = "E5E7EB" })),
        new TableGrid(
            new GridColumn { Width = "2200" },
            new GridColumn { Width = "5200" }));

    table.Append(Row(("Need", true), ("OpenXML implementation", true)));
    table.Append(Row(("Create", false), ("Reports, proposals, memos, manuscripts, and structured formal documents.", false)));
    table.Append(Row(("Edit", false), ("Paragraphs, runs, tables, headers, footers, styles, sections, and fields.", false)));
    table.Append(Row(("Validate", false), ("OpenXML SDK validation plus optional Word visual review for layout-sensitive work.", false)));
    return table;
}

static TableRow Row((string Text, bool Header) left, (string Text, bool Header) right)
{
    return new TableRow(Cell(left.Text, left.Header), Cell(right.Text, right.Header));
}

static TableCell Cell(string text, bool header)
{
    var run = new Run(new Text(text) { Space = SpaceProcessingModeValues.Preserve });
    if (header)
    {
        run.PrependChild(new RunProperties(new Bold()));
    }

    return new TableCell(
        new TableCellProperties(
            new TableCellWidth { Type = TableWidthUnitValues.Pct, Width = "2500" },
            new Shading { Val = ShadingPatternValues.Clear, Fill = header ? "EAF3FB" : "FFFFFF" },
            new TableCellMargin(
                new TopMargin { Width = "80", Type = TableWidthUnitValues.Dxa },
                new LeftMargin { Width = "120", Type = TableWidthUnitValues.Dxa },
                new BottomMargin { Width = "80", Type = TableWidthUnitValues.Dxa },
                new RightMargin { Width = "120", Type = TableWidthUnitValues.Dxa })),
        new Paragraph(
            new ParagraphProperties(new ParagraphStyleId { Val = "BodyText" }),
            run));
}

static SectionProperties CreateSectionPropertiesA4()
{
    return new SectionProperties(
        new PageSize { Width = 11906U, Height = 16838U },
        new PageMargin
        {
            Top = 1440,
            Right = 1440U,
            Bottom = 1440,
            Left = 1440U,
            Header = 720U,
            Footer = 720U,
            Gutter = 0U
        });
}

static void ValidateDocument(string path)
{
    using var doc = WordprocessingDocument.Open(path, false);
    var errors = new OpenXmlValidator().Validate(doc).ToList();
    if (errors.Count == 0)
    {
        Console.WriteLine("OpenXML validation: passed");
        return;
    }

    Console.WriteLine($"OpenXML validation: {errors.Count} error(s)");
    foreach (var error in errors.Take(20))
    {
        Console.WriteLine($"{error.Path?.XPath ?? "(unknown path)"}: {error.Description}");
    }
}
