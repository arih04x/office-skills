---
name: office-ppt
description: "Create, edit, style, and validate Microsoft PowerPoint .pptx slides and decks with task-specific JavaScript, PptxGenJS, GPT image generation, stored style references, and PowerPoint-native PNG review. Use for PPT/PPTX/PowerPoint work: one-slide visuals, slide decks, presentation figures, image-backed slides, visual style transfer, brand/style references, CJK slides, deck refresh, and slide QA."
---

# Office PPT

Use this skill for PowerPoint `.pptx` tasks. Build with Node.js + PptxGenJS; use GPT image generation for visual backgrounds.

## Operating Model

- Node.js with `pptxgenjs` and OpenAI-compatible image API.
- Copy `assets/node-starter/` as starting point when useful.
- Style references in `assets/styles/` (built-in: `onij.png`).
- Env config from `config/office-skills.local.env`, `OFFICE_SKILLS_ENV`, or `--env`.
- Generated images → slide backgrounds; exact text → native PPT text boxes.

## Core Loop

Styled decks follow a five-stage interactive workflow:

1. **Clarify** — Ask user for theme, audience, slide count, style preference.
2. **Theme image** — Generate a theme/mood image to align visual direction.
3. **Draft deck** — Build an editable PPTX draft with placeholder text on
   generated backgrounds. Discuss structure with user (pages, content, message).
4. **User revision** — User reviews and edits the draft (text, order, emphasis).
5. **Polish** — Based on finalized content, call image API for per-slide
   tailored visuals; rebuild final deck with native text over polished images.

Do not treat style references as palette-only hints. Use the image generator for
high-level visual material; use PowerPoint-native objects for precision and
editability. See `references/interactive-workflow.md` for full details.

## Task Selection

| Task | Read | Focus |
| --- | --- | --- |
| Styled deck (full workflow) | `references/interactive-workflow.md` | Five-stage interactive loop |
| Create slide/deck | `references/create-pptx.md` | PptxGenJS code |
| GPT image / style transfer | `references/gpt-image-style.md` | Generate PNGs first, consume in PPT script |
| Apply visual style | `references/style-assets.md` | Style reference → palette/composition cues |
| Validate output | `references/validation.md` | Export to PNG, inspect rendered result |

Read the matching reference, implement, validate with `scripts/check-pptx.py`.

## Key Rules

- 16:9 default; one message per slide; text always editable.
- No exact text/data/formulas inside generated images.
- CJK: Microsoft YaHei or DengXian; margins 0.45-0.75 in.
- Inspect exported PNGs for cropped text, low contrast, misplaced overlays.
