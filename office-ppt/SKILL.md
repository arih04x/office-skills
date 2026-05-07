---
name: office-ppt
description: "Create, edit, style, and validate Microsoft PowerPoint .pptx slides and decks with task-specific JavaScript, PptxGenJS, GPT image generation, stored style references, and PowerPoint-native PNG review. Use for PPT/PPTX/PowerPoint work: one-slide visuals, slide decks, presentation figures, image-backed slides, visual style transfer, brand/style references, CJK slides, deck refresh, and slide QA."
---

# Office PPT

Use this skill when the requested output or source file is a PowerPoint `.pptx`
or when the user asks for a slide/deck.

Build task-specific JavaScript with PptxGenJS. Use GPT image generation for
visual backgrounds, illustrations, and style-driven imagery. Keep reliable slide
text as native PowerPoint text.

## Core Visual Loop

Styled decks should follow a two-stage loop:

1. Generate advanced visual layers first: cover backgrounds, chapter dividers,
   atmosphere panels, local illustrations, or image-backed figure layers.
2. Build the deck second with PptxGenJS: add generated images as background or
   supporting layers, then place exact titles, labels, arrows, numbers, tables,
   formulas, and speaker-facing copy as native editable PowerPoint objects.

Do not treat style references as palette-only hints when the user asks for a
polished or style-guided deck. Use the image generator for high-level visual
material, then use PowerPoint-native objects for precision and editability.

## Operating Model

- Use Node.js with `pptxgenjs` and the OpenAI-compatible image API.
- Create a small task folder in the user's output/work directory.
- Copy or adapt `assets/node-starter/` when a ready starting point is useful.
- For image-only generation assets, copy or adapt
  `office-figure/assets/node-image-starter/generate-style-image.mjs` when that
  sibling skill is available; otherwise implement the same pattern inside the
  PPT task folder.
- Use style references from `assets/styles/`. The built-in style asset is
  `assets/styles/onij.png`.
- Load local image API configuration from `config/office-skills.local.env` at
  the repository root, from `OFFICE_SKILLS_ENV`, or from a task-specific `--env`
  path. Treat this file as secret material and do not print its values.
- Use generated images as slide backgrounds or supporting visuals. Put titles,
  labels, bullets, and numbers in native PPT text boxes.
- Validate the `.pptx` by opening/exporting with desktop PowerPoint when layout
  quality matters. On macOS/Linux, use manual PowerPoint/Keynote/LibreOffice
  review or `soffice` conversion when available.

## Task Selection

| Task | Read | Implementation focus |
| --- | --- | --- |
| Create a new single slide or deck | `references/create-pptx.md` | Write task-specific PptxGenJS code |
| Use GPT image generation or a style image | `references/gpt-image-style.md` | Generate background/local visual PNGs first, then consume them from the PPT script |
| Apply a visual style | `references/style-assets.md` | Select style reference, extract palette/composition cues, keep text native |
| Validate visual output | `references/validation.md` | Export slides to PNG with PowerPoint and inspect rendered result |

## Implementation Steps

1. Read the user brief, audience, output path, slide count, and style request.
2. Choose the style asset if specified. For `onij`, use
   `assets/styles/onij.png`.
3. Create a task folder and initialize dependencies:

   ```powershell
   npm init -y
   npm install pptxgenjs openai
   ```

4. Generate required visual assets with the OpenAI-compatible image API. Use the
   style reference when style transfer is requested. Save these files under the
   task folder, for example `assets/generated/*.png`.
5. Create the `.pptx` with PptxGenJS, inserting generated images first and
   editable PowerPoint text/shapes/charts second.
6. Export to PNG with PowerPoint for visual review when PowerPoint is available.
   On macOS/Linux, use `soffice` or manual app review if PowerPoint automation
   is unavailable.
7. Report the `.pptx`, generated images, and validation artifacts.

## Design Rules

- Use 16:9 unless the user or source file requires another aspect ratio.
- Keep a single clear message per slide.
- Keep text editable. Avoid rasterizing full slides with embedded text.
- Use generated images for mood, subject matter, texture, illustration, or scene
  composition. Use PPT text for exact wording.
- Use generated image layers for advanced backgrounds and local visual material:
  hero/closing scenes, section dividers, visual metaphors, texture bands,
  method-figure backplates, and other non-exact imagery.
- Do not put exact Chinese/English copy, data values, axis labels, formulas, or
  important callouts inside generated images.
- Respect the style image through palette, lighting, texture, density, and
  composition rather than copying it literally.
- For CJK slides, use Microsoft YaHei, DengXian, or another installed CJK font.
- Keep slide margins stable: about 0.45-0.75 inches for content-heavy slides.
- Before delivery, inspect exported PNGs for cropped text, low contrast,
  misplaced overlays, and unreadable type.

## Resources

- `assets/styles/onij.png`: stored visual style reference.
- `../config/office-skills.local.env.example`: shared local image API configuration template.
- `assets/node-starter/`: minimal GPT image + PptxGenJS starter.
- `scripts/export-pptx-png.ps1`: Windows PowerPoint-native slide PNG export helper.
- `references/`: task-specific PPT guidance.
- `examples/`: concise implementation briefs.
- `examples/showcase/showcase-slide.pptx` and `showcase-slide.png`: editable PPT showcase and exported preview.
