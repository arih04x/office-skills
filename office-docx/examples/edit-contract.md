# Example: Edit a Contract

User request:

> In this contract, replace the client name, update the effective date, add a
> new confidentiality paragraph after section 4, and save a new file.

Implementation:

1. Copy the source `.docx` to the requested output path.
2. Inspect paragraph text and styles to locate section 4.
3. Replace client name and date in `Text` elements when each token is contained
   in a single run.
4. Insert the new paragraph after the located section paragraph or after the
   final paragraph in that section.
5. Validate the output and compare paragraph counts.

Reference files:

- `references/edit-existing-docx.md`
- `references/openxml-rules.md`
- `references/validation.md`
