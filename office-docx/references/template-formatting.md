# Template Formatting

Use this reference when the user asks to apply a template, imitate formatting,
repair layout, or make a document match a standard.

## Choose the Template Strategy

| Scenario | Strategy |
| --- | --- |
| Template mainly contains styles, theme, numbering, or fonts | Copy style/theme/numbering parts into the output document |
| Template contains required cover, TOC, headers, footers, or section layout | Use the template as the output base and replace sample body content |
| Source content has important direct formatting | Preserve direct formatting selectively |
| Source content should fully adopt the template style | Strip direct formatting and keep semantic style IDs |

## Style Transfer

Transfer these parts when needed:

- `StyleDefinitionsPart`
- `ThemePart`
- `NumberingDefinitionsPart`
- `FontTablePart`
- document settings that control compatibility

Then map source paragraphs to template style IDs. For example, map detected
headings to `Heading1`, `Heading2`, and `Heading3` or to the template's custom
style IDs.

## Direct Formatting

Direct paragraph and run formatting overrides style definitions. Decide how to
handle it before applying a template:

- Preserve direct formatting for citations, emphasis, code, and intentional
  highlighting.
- Strip direct font, color, spacing, borders, and shading when the template
  should control layout.
- Keep paragraph style IDs whenever they express document structure.

## Sections

Templates with covers, Roman-numbered front matter, body chapters, appendices,
or different headers often depend on multiple sections. Preserve the template's
section layout when it is part of the requested format.

For chaptered documents:

- Chapter headings may require odd-page section breaks.
- Front matter and body may use different page numbering formats.
- Headers and footers can differ per section.

## Headers and Footers

When the template defines headers and footers, copy the corresponding parts and
relationships together. Section properties must reference the correct header and
footer relationship IDs.

## TOC and Fields

If the template has a TOC, keep the field structure and ensure headings have
outline levels. Word can refresh the displayed TOC.

## Final Checks

- Confirm content appears once.
- Confirm heading hierarchy is preserved.
- Confirm page size, margins, and section count match the template intent.
- Confirm headers, footers, and page numbers belong to the correct sections.
