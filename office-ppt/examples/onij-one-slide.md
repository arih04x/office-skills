# Example: One Onij-Style Slide

User request:

> Create one PowerPoint slide using the `onij` style.

Implementation:

1. Load `assets/styles/onij.png`.
2. Load image API configuration from `config/office-skills.local.env`,
   `OFFICE_SKILLS_ENV`, or a task-specific `--env` path.
3. Generate a 16:9 background image with the style reference.
4. Create a one-slide `.pptx` with PptxGenJS.
5. Put the title and short body text in native PPT text boxes.
6. Export to PNG with PowerPoint and inspect the render.

Reference files:

- `references/gpt-image-style.md`
- `references/create-pptx.md`
- `references/validation.md`
