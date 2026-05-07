# Example: Create a Report

User request:

> Create a Word report from these notes, with a title page, executive summary,
> three sections, one comparison table, and A4 layout.

Implementation:

1. Create a task project with `dotnet new console --framework net8.0`.
2. Add `DocumentFormat.OpenXml`.
3. Define styles for title, heading levels, body text, caption, and table text.
4. Build the body in semantic order: title, summary, sections, table, closing.
5. Add A4 section properties as the final body child.
6. Run OpenXML validation.

Reference files:

- `references/create-docx.md`
- `references/openxml-rules.md`
- `references/validation.md`
