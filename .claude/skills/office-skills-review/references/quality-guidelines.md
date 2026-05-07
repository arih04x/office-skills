# Quality Guidelines

Use these soft checks during review.

## Skill Scope

- `office-docx` owns Word/DOCX work using .NET and OpenXML SDK.
- `office-pdf` owns PDF creation, inspection, rendering, extraction, filling, merging, and validation.
- `office-ppt` owns PowerPoint/PPTX work using Node.js and PptxGenJS.
- `office-figure` owns editable figures, diagrams, charts, draw.io, TikZ, and insertion assets.
- `office-motion` owns promotional GIFs, PPT-ready animated assets, stickers, and GIF/video conversion.

Avoid moving one-off project files into skill directories.

## Cross-Platform Notes

- Prefer relative paths in docs and examples.
- Include Windows PowerShell and macOS/Linux shell commands when commands differ.
- Use PATH-discovered tools where practical.
- Keep Windows-only helpers clearly labeled, such as PowerPoint COM export scripts.

## Credential Handling

- Read API keys from environment variables or ignored local env files.
- Do not print local env file values.
- Keep checked-in examples as placeholders.

## Assets

- Keep reusable templates, previews, and starter code.
- Avoid generated task debris, local caches, and bulky one-off outputs.
- Binary examples are acceptable when they demonstrate an expected output.

## Documentation Sync

When adding or changing a skill, update:

- `README.md`
- `.codex/INSTALL.md` when installation changes
- `.claude-plugin/plugin.json` keywords/description when repository scope changes
- relevant skill references
