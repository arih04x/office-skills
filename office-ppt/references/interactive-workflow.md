# Interactive PPT Workflow

This is the standard workflow for styled PowerPoint decks. Follow all five
stages in order. Do not skip the draft/revision cycle.

## Stage 1: Clarify

Ask the user before generating anything:

- Theme / subject matter
- Audience (internal team, client, conference, class)
- Approximate slide count
- Style preference (reference image, brand, mood keywords)
- Output path and language

Do not assume answers. Wait for explicit confirmation.

## Stage 2: Theme Image

Generate a single theme/mood image that captures the visual direction:

- Use the style reference (`assets/styles/onij.png` or user-provided) as input
- Prompt should describe the overall atmosphere, not specific slide content
- Share the theme image with the user for approval before proceeding
- If rejected, regenerate with adjusted direction

This image sets the palette, texture, and density for the entire deck.

## Stage 3: Draft Deck

Build an editable PPTX draft:

- Use the theme image (or a simple solid/gradient) as background for all slides
- Place native PPT text boxes with placeholder/draft content
- Structure: cover → agenda/outline → content slides → closing
- Each slide has a clear single message
- Text is fully editable — user can open in PowerPoint and modify directly

Present the draft structure to the user:

- List each slide: number, title, key message, notes
- Ask: "Does this structure work? Any slides to add/remove/reorder?"
- Ask: "Any text changes before I generate final visuals?"

## Stage 4: User Revision

Wait for user feedback. Common changes:

- Reorder slides
- Add/remove slides
- Rewrite titles or bullet points
- Adjust emphasis or messaging
- Change slide count

Apply all requested changes to the draft. Confirm the final structure is locked
before proceeding to Stage 5.

## Stage 5: Polish

Generate per-slide tailored visuals:

- Each slide gets its own background image matching its specific content/message
- Use the theme image as style reference for consistency across slides
- Prompt each image with the slide's topic, not generic atmosphere
- Rebuild the final PPTX: generated images as backgrounds, finalized native text
  on top
- Validate: export to PNG, check for cropped text, low contrast, misplaced
  overlays

Deliver: final `.pptx`, generated images folder, and validation PNGs if
available.

## Key Principles

- Never put exact text, data values, or formulas inside generated images.
- The draft stage exists so the user controls content before expensive image
  generation.
- Style references guide palette/texture/density — not literal copying.
- Each stage requires user confirmation before advancing to the next.
- For simple one-slide requests, stages 3-4 can be compressed (ask "is this
  text correct?" before generating the final image).
