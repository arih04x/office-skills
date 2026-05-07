# Example: Apply a Template

User request:

> Make this manuscript match the university thesis template, including heading
> styles, page size, margins, headers, footers, and page numbering.

Implementation:

1. Inspect the source and template document structures.
2. Decide whether the template is a style source or a structural base.
3. Preserve the template's section, header, footer, and numbering structure when
   those elements define the required format.
4. Move source content into the template structure, mapping headings and body
   paragraphs to template style IDs.
5. Validate section properties, headers, footers, and heading outline levels.
6. Open in Word or export to PDF for a visual layout check.

Reference files:

- `references/template-formatting.md`
- `references/openxml-rules.md`
- `references/validation.md`
